"""Sprites aus den bewegten Imagegen-Entwürfen (assets/animationen/).

Jedes Entwurfsbild liegt auf einer Arbeitsfläche von 720 x 600 mit dem
Fußpunkt der Figur bei (360, 520). Pro Animation wird die ganze Fläche um
einen festen Faktor verkleinert, sodass die Figur so groß ist wie in den
übrigen Sprites. Danach: harte Transparenz, eine gemeinsame Palette mit
höchstens 32 Farben für alle Bilder, Zuschnitt auf das gemeinsame Rechteck.
Der Fußpunkt steht als "anker" im JSON und wird von tools/psp/assets_bauen.py
übernommen.

Dazu kommt alles, was die Umarmung braucht, damit der Ablauf ohne Sprung
zusammenpasst:

    held_tod                  Der Held sackt nach vorn zur Königin hin zusammen.
                              Das letzte Bild ist genau der liegende Körper aus
                              dem ersten Bild der Umarmung.
    held_schwert_boden        Sein Schwert, das ihm beim Fallen aus der Hand rutscht.
    koenigin_sense_boden      Die Sense, die sie für die Umarmung ablegt.
    koenigin_p1_umarmung_stehend
                              Erstes Umarmungsbild ohne den Helden: Sie steht nach
                              dem Ritual auf, bevor sie die Sense wieder aufnimmt.
    koenigin_p1_umarmung_umhang
                              Nur der grüne Umhang des Helden in der Umarmung, für
                              die Farbtabellen der Ausrüstungsstufen (Gruppe "held").

    python tools/cutout/entwuerfe.py
"""

import colorsys
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402
import held as H  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENTWURF = os.path.join(REPO, "assets", "animationen", "entwuerfe-2026-10-10")
OUT = os.path.join(REPO, "assets", "sprites", "cutout")
FARBEN = 32

# (Ausgabe, Entwurf, Bezugsbilder, Zielhöhe in Sprite-Pixeln, Anker-Korrektur x)
# Zielhöhe = mittlere Höhe der Figur in den Bezugsbildern, gemessen wie in den Ruheposen:
# Königin 91 px mit Krone, Held 44 px mit Kapuze.
# Anker-Korrektur: verschiebt den Fußpunkt, damit die Füße im ersten Bild dort stehen,
# wo sie in der Ruhepose stehen (sonst springt die Figur beim Wechsel).
ANIMATIONEN = [
    ("koenigin_p1_atk_richtschlag", "p1_atk_richtschlag", [0, 9], 91, 4),
    ("held_atk_hieb", "held_atk_hieb", [0, 7], 44, 3),
    # Bild 1: Die Königin steht neben dem liegenden Helden.
    ("koenigin_p1_umarmung", "p1_ritual_umarmung_feuer", [0], 91, 0),
]


def lade(entwurf):
    ordner = os.path.join(ENTWURF, entwurf)
    meta = json.load(open(os.path.join(ordner, "animation.json"), encoding="utf-8"))
    bogen = Image.open(os.path.join(ordner, meta["image"])).convert("RGBA")
    bilder = []
    for f in meta["frames"]:
        r = f["frame"]
        bilder.append(bogen.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"])))
    return meta, bilder


def palette_von(bilder, farben=FARBEN):
    """Palette nur aus den deckenden Pixeln, damit der leere Hintergrund nicht mitzählt.

    Median-Cut allein verliert kleine Farbflächen (braune Stiefel, Hautton); die
    k-means-Nachbesserung hält sie.
    """
    pixel = np.concatenate([a[a[:, :, 3] > 0][:, :3] for a in map(np.asarray, bilder)])
    streifen = Image.fromarray(pixel.reshape(1, -1, 3).astype(np.uint8), "RGB")
    return streifen.quantize(colors=farben, method=Image.Quantize.MEDIANCUT, kmeans=3)


def binden(bilder, palette):
    aus = []
    for b in bilder:
        q = b.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
        # Transparente Pixel einheitlich (0, 0, 0, 0)
        aus.append(Image.composite(q, Image.new("RGBA", q.size), b.getchannel("A")))
    return aus


def hoehe_deckend(bild):
    """Höhe der Figur ohne halbtransparente Randpixel."""
    kasten = bild.getchannel("A").point(lambda a: 255 if a > 110 else 0).getbbox()
    return kasten[3] - kasten[1]


def hart(bild):
    alpha = bild.getchannel("A").point(lambda a: 255 if a > 110 else 0)
    bild.putalpha(alpha)
    return bild


def verkleinern(bild, faktor):
    w, h = round(bild.width / faktor), round(bild.height / faktor)
    return hart(bild.resize((w, h), Image.Resampling.BOX))


def speichere(name, bilder, anker, dauer, quelle, extra=None):
    """bilder: gleich große Bilder; anker: Fußpunkt darin. Schneidet auf das gemeinsame Rechteck zu."""
    kasten = [b.getbbox() for b in bilder if b.getbbox()]
    x0 = max(0, min(k[0] for k in kasten) - 1)
    y0 = max(0, min(k[1] for k in kasten) - 1)
    x1 = min(bilder[0].width, max(k[2] for k in kasten) + 1)
    y1 = min(bilder[0].height, max(k[3] for k in kasten) + 1)
    fw, fh = x1 - x0, y1 - y0
    anker = (anker[0] - x0, anker[1] - y0)

    sheet = Image.new("RGBA", (fw * len(bilder), fh))
    vorschau = []
    for i, b in enumerate(bilder):
        stueck = b.crop((x0, y0, x1, y1))
        sheet.paste(stueck, (i * fw, 0))
        bg = Image.new("RGBA", stueck.size, (28, 24, 44, 255))
        bg.alpha_composite(stueck)
        vorschau.append(bg.resize((fw * 4, fh * 4), Image.Resampling.NEAREST).convert("P"))
    os.makedirs(OUT, exist_ok=True)
    sheet.save(os.path.join(OUT, name + ".png"))
    daten = {"name": name, "frame_w": fw, "frame_h": fh, "fps": 12, "anker": list(anker), "dauer": dauer,
             "quelle": quelle}
    daten.update(extra or {})
    daten["frames"] = [{"x": i * fw, "y": 0, "w": fw, "h": fh} for i in range(len(bilder))]
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=1)
    if len(vorschau) > 1:
        vorschau[0].save(os.path.join(OUT, name + "_vorschau.gif"), save_all=True, append_images=vorschau[1:],
                         duration=[round(1000 * t / 12) for t in dauer], loop=0)
    a = np.asarray(sheet)
    farben = len(np.unique(a[a[:, :, 3] > 0][:, :3], axis=0))
    print(f"{name}: {len(bilder)} Bilder, {fw} x {fh}, Anker {anker}, {farben} Farben")


def bauen(name, entwurf, bezug, zielhoehe, anker_dx):
    meta, gross = lade(entwurf)
    hoehe = [hoehe_deckend(gross[i]) for i in bezug]
    faktor = sum(hoehe) / len(hoehe) / zielhoehe
    klein = [verkleinern(b, faktor) for b in gross]
    bilder = binden(klein, palette_von(klein))
    anker = (round(meta["anchor"]["x"] / faktor) + anker_dx, round(meta["anchor"]["y"] / faktor))
    dauer = [f["durationTicks"] for f in meta["frames"]]
    speichere(name, bilder, anker, dauer, "animationen/entwuerfe-2026-10-10/" + entwurf)
    return {"gross": gross, "faktor": faktor, "bilder": bilder, "anker": anker, "dauer": dauer}


# --- Umarmung: liegender Held, Umhang-Ebene ---------------------------------------

def held_maske_gross(bild):
    """Pixel des liegenden Helden im ersten Umarmungsbild (Entwurfsauflösung).

    Der Held liegt links, die Königin steht rechts; nur am Stiefel der Königin
    berühren sie sich (x 310-345). Dort entscheidet die Farbe: grüne und
    braune Pixel gehören zum Helden, graue und violette zur Königin, dunkle
    Umrisspixel zum nächsten eindeutig zugeordneten Nachbarn.
    """
    a = np.asarray(bild).astype(np.int32)
    deckend = a[:, :, 3] > 20
    h, w = deckend.shape
    yy, xx = np.mgrid[0:h, 0:w]
    bereich = deckend & (yy > 420)
    held = bereich & (xx < 310)
    naht = bereich & (xx >= 310) & (xx < 350)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gruen = (g > r + 6) & (g > b)
    braun = (r > g + 12) & (g > b) & (r > 70)
    dunkel = np.maximum(np.maximum(r, g), b) < 45
    held |= naht & (gruen | braun)
    koenigin = naht & ~(gruen | braun) & ~dunkel
    offen = naht & dunkel
    for _ in range(12):
        if not offen.any():
            break
        hn = np.zeros_like(held)
        kn = np.zeros_like(held)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            hn |= np.roll(np.roll(held, dy, 0), dx, 1)
            kn |= np.roll(np.roll(koenigin, dy, 0), dx, 1)
        neu_h = offen & hn & ~kn
        neu_k = offen & kn
        held |= neu_h
        koenigin |= neu_k
        offen &= ~(neu_h | neu_k)
    return held


def umhang_ebene(bilder):
    """Nur die grünen Pixel (Umhang des Helden); türkise Augen und Kristalle bleiben draußen."""
    aus = []
    for b in bilder:
        a = np.array(b)
        rgb = a[:, :, :3].astype(np.float32) / 255
        hsv = np.array([colorsys.rgb_to_hsv(*p) for p in rgb.reshape(-1, 3)]).reshape(rgb.shape)
        gruen = (a[:, :, 3] > 0) & (hsv[:, :, 0] > 0.2) & (hsv[:, :, 0] < 0.43) & (hsv[:, :, 1] > 0.15)
        a[~gruen] = 0
        aus.append(Image.fromarray(a))
    return aus


# --- Tod des Helden --------------------------------------------------------------

HUEFTE_Y = 1100        # im Konzeptbild: darunter Beine und Stiefel


def tod_bild(koerper, schwert, groesse, anker, winkel, knie, k, weiss=0.0, dx=0, mit_schwert=True):
    """Ein Bild des Zusammensackens in Sprite-Auflösung.

    knie: 1.0 = Beine gestreckt, kleiner = Knie geben nach (Beine gestaucht).
    winkel: Oberkörper nach vorn (im Uhrzeigersinn) um die Hüfte gekippt.
    k: Vergrößerung (zum Maßstab des liegenden Körpers aus der Umarmung).
    """
    m = H.MASSSTAB / k
    bild = koerper.copy()
    if mit_schwert:
        bild.alpha_composite(schwert)
    if weiss:
        hell = Image.new("RGBA", bild.size, (255, 255, 255, 255))
        hell.putalpha(bild.getchannel("A"))
        bild = Image.blend(bild, hell, weiss)
    oben = bild.crop((0, 0, bild.width, HUEFTE_Y))
    unten = bild.crop((0, HUEFTE_Y, bild.width, bild.height))
    beinhoehe = H.FUESSE_Y - HUEFTE_Y
    neu_h = max(1, round(beinhoehe * knie))
    unten = unten.crop((0, 0, unten.width, beinhoehe)).resize((unten.width, neu_h), Image.Resampling.BOX)
    gross = Image.new("RGBA", (3600, 2400))
    fx, fy = 1300, 2000                       # Fußpunkt (Anker) auf der großen Fläche
    ox = fx - 500 + dx * H.MASSSTAB           # Konzept-x 500 = Körpermitte = Anker
    gross.alpha_composite(unten, (ox, fy - neu_h))
    huefte = (ox + 520, fy - neu_h)           # Drehpunkt vorn an der Hüfte
    rand = Image.new("RGBA", gross.size)
    rand.alpha_composite(oben, (ox, fy - neu_h - HUEFTE_Y))
    rand = rand.rotate(-winkel, resample=Image.Resampling.BICUBIC, center=huefte)
    gross.alpha_composite(rand)
    # Nichts unter den Boden
    a = np.array(gross)
    a[fy:, :, 3] = 0
    gross = Image.fromarray(a)
    klein = gross.resize((round(gross.width / m), round(gross.height / m)), Image.Resampling.BOX)
    klein = hart(klein)
    ax, ay = round(fx / m), round(fy / m)
    flaeche = Image.new("RGBA", groesse)
    A._sicher(flaeche, klein, anker[0] - ax, anker[1] - ay)
    return flaeche


def schwert_boden(palette_quelle):
    """Das Schwert flach am Boden, aus dem Konzeptbild gedreht und verkleinert."""
    bild = A.lade(H.QUELLE)
    _, teil = H.zerlege_held(bild)
    a = np.array(teil)
    # Hand und Handschuh (braun) entfernen, Stahl, Parierstange und Knauf bleiben
    rgb = a[:, :, :3].astype(np.int32)
    braun = (rgb[:, :, 0] > rgb[:, :, 2] + 30) & (rgb[:, :, 0] > 80)
    a[braun] = 0
    teil = Image.fromarray(a)
    (ax, ay), (bx, by) = H.KLINGE_A, H.KLINGE_B
    winkel = math.degrees(math.atan2(by - ay, bx - ax))
    rand = 600
    gross = Image.new("RGBA", (teil.width + 2 * rand, teil.height + 2 * rand))
    gross.alpha_composite(teil, (rand, rand))
    gross = gross.rotate(winkel, resample=Image.Resampling.BICUBIC, center=(ax + rand, ay + rand))
    gross = gross.crop(gross.getbbox())
    klein = verkleinern(gross, H.MASSSTAB / 1.2)
    klein = binden([klein], palette_quelle)[0]
    return klein.crop(klein.getbbox())


def sense_boden():
    """Die Sense der Königin flach am Boden, Klinge nach oben gebogen (aus der Ruhepose)."""
    bild = A.lade("koenigin-idle-sense-helm-v5.webp")
    m = A.maske(bild.size, A.SENSE_ARM[:2])
    teil = Image.new("RGBA", bild.size)
    teil.paste(bild, (0, 0), m)
    a = np.array(teil)
    # Hand am Stiel (y 695-800) durch den Stiel darüber ersetzen
    zeile = a[690, :400].copy()
    for y in range(695, 805):
        a[y, :400] = zeile
    teil = Image.fromarray(a)
    teil = teil.crop(teil.getbbox())
    klein = verkleinern(teil, 16)
    klein = binden([klein], palette_von([klein], 24))[0]
    # Im Uhrzeigersinn flachlegen: Klinge zeigt nach oben, Stielende nach links
    return klein.transpose(Image.Transpose.ROTATE_270)


def tod_und_umarmung(umarmung):
    gross0 = umarmung["gross"][0]
    faktor = umarmung["faktor"]
    u_anker = umarmung["anker"]
    u0 = umarmung["bilder"][0]

    # Liegender Held: genau die Pixel aus dem Umarmungs-Sprite
    maske_g = Image.fromarray((held_maske_gross(gross0) * 255).astype(np.uint8))
    maske_k = maske_g.resize(u0.size, Image.Resampling.BOX).point(lambda v: 255 if v >= 128 else 0)
    liegend = Image.composite(u0, Image.new("RGBA", u0.size), maske_k)
    kasten = liegend.getbbox()
    # Fußpunkt des Toten: an den Fersen, wo er vorher stand (vorn kippt er zur Königin hin)
    tod_anker_u = (kasten[0] + 6, u_anker[1])
    abstand = u_anker[0] - tod_anker_u[0]
    mitte = (kasten[0] + kasten[2]) // 2 - tod_anker_u[0]

    # Zusammensacken aus dem Konzeptbild (ohne Schwert, das rutscht ihm aus der Hand)
    bild = A.lade(H.QUELLE)
    koerper, schwert = H.zerlege_held(bild)
    groesse = (110, 72)
    anker = (30, 68)
    # (Oberkörper-Winkel, Knie, Vergrößerung, Weiß, dx, Schwert in der Hand)
    posen = [
        (0, 1.0, 1.0, 0.5, -1, True),     # Treffer: Aufblitzen
        (-6, 0.97, 1.0, 0.0, -2, True),   # taumelt zurück
        (8, 0.86, 1.05, 0.0, -1, False),  # Knie geben nach, Schwert fällt
        (30, 0.70, 1.1, 0.0, 0, False),
        (58, 0.55, 1.15, 0.0, 0, False),  # auf den Knien, kippt nach vorn
        (80, 0.42, 1.2, 0.0, 0, False),
    ]
    bilder = [tod_bild(koerper, schwert, groesse, anker, w, kn, k, ws, dx, s) for w, kn, k, ws, dx, s in posen]
    lieg = Image.new("RGBA", groesse)
    lieg.alpha_composite(liegend, (anker[0] - tod_anker_u[0], anker[1] - tod_anker_u[1]))
    bilder += [lieg, lieg.copy()]
    pal = palette_von(bilder[:6] + [lieg])
    bilder = binden(bilder[:6], pal) + bilder[6:]
    speichere("held_tod", bilder, anker, [1] * 8, "held-idle-hood-v3 und animationen/entwuerfe-2026-10-10",
              {"konstanten": {"UMARM_ABSTAND": abstand, "TOD_MITTE": mitte, "TOD_SCHWERT_BILD": 2}})

    # Schwert am Boden: liegt hinter seinen Fersen, Spitze von der Königin weg
    s = schwert_boden(pal).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    speichere("held_schwert_boden", [s], (s.width - 4, s.height - 1), [1], H.QUELLE)

    # Sense am Boden: beginnt unter der knienden Königin und liegt hinter ihr, unter dem Mantel
    sb = sense_boden()
    speichere("koenigin_sense_boden", [sb], (12, sb.height - 1), [1], "koenigin-idle-sense-helm-v5")

    # Aufstehen nach dem Ritual: erstes Bild ohne den liegenden Helden
    stehend = Image.composite(Image.new("RGBA", u0.size), u0, maske_k)
    speichere("koenigin_p1_umarmung_stehend", [stehend], u_anker, [8], "koenigin_p1_umarmung")

    # Umhang-Ebene der Umarmung für die Farbtabellen des Helden
    speichere("koenigin_p1_umarmung_umhang", umhang_ebene(umarmung["bilder"]), u_anker, umarmung["dauer"],
              "koenigin_p1_umarmung")


def main():
    erg = {a[0]: bauen(*a) for a in ANIMATIONEN}
    tod_und_umarmung(erg["koenigin_p1_umarmung"])


if __name__ == "__main__":
    main()
