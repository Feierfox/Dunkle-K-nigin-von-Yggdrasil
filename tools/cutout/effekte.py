"""Effekte in nativer PSP-Auflösung und Vorschau-Szenen im Thronsaal.

Effekte (assets/sprites/effekte/):
    fx_impuls1_ring   10 Bilder  Ringwelle über den Boden (Wechsel zu Phase 2), 480 x 48
    fx_nebel_kachel    1 Bild    kachelbare Nebeltextur 64 x 64 (Wechsel zu Phase 3)
    fx_feuer_eisblau   8 Bilder  eisblaues Feuer des Totenrituals, 40 x 48
    fx_portal         12 Bilder  lila Portal am Boden: öffnen, kreisen, schließen, 64 x 24

Vorschau-Szenen (GIF, zweifach vergrößert):
    szene_impuls1_sprung, szene_impuls2_amulett, szene_ritual_feuer, szene_ritual_portal

    python tools/cutout/effekte.py
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FX = os.path.join(REPO, "assets", "sprites", "effekte")
CUT = os.path.join(REPO, "assets", "sprites", "cutout")
PSP = os.path.join(REPO, "assets", "konzept", "psp")
W, H = 480, 272
BODEN = 240

EIS = [(0, 0, 0, 0), (20, 40, 70, 255), (42, 143, 154, 255), (89, 195, 195, 255), (168, 255, 244, 255), (232, 255, 251, 255)]
LILA = [(58, 6, 64), (96, 16, 140), (122, 24, 190), (204, 50, 242), (238, 32, 251), (240, 200, 255)]


def streifen(bilder):
    w, h = bilder[0].size
    s = Image.new("RGBA", (w * len(bilder), h))
    for i, b in enumerate(bilder):
        s.paste(b, (i * w, 0))
    return s


def speichere_fx(name, bilder):
    os.makedirs(FX, exist_ok=True)
    streifen(bilder).save(os.path.join(FX, name + ".png"))


def gif(name, bilder, dauer=83, faktor=2):
    frames = [b.convert("RGB").resize((b.width * faktor, b.height * faktor), Image.Resampling.NEAREST) for b in bilder]
    frames[0].save(os.path.join(PSP, name + ".gif"), save_all=True, append_images=frames[1:], duration=dauer, loop=0)


# --- Effekte -------------------------------------------------------------------

def impuls1_ring(n=10, w=480, h=48, cx=240):
    bilder = []
    for i in range(n):
        t = (i + 1) / n
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        rx = 10 + t * (w / 2 + 20)
        ry = max(3, rx * 0.11)
        cy = h - 10
        for dicke, farbe in ((5, EIS[2]), (3, EIS[4]), (1, EIS[5])):
            a = int(255 * (1 - t * 0.6))
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(*farbe[:3], a), width=dicke)
        # Funken auf der Welle
        rnd = random.Random(i)
        for _ in range(int(12 * (1 - t) + 4)):
            ang = rnd.uniform(0, 2 * math.pi)
            x, y = cx + math.cos(ang) * rx, cy + math.sin(ang) * ry - rnd.randint(1, 6)
            d.point((x, y), fill=EIS[5])
        bilder.append(b)
    return bilder


def nebel_kachel(g=64):
    """Kachelbare Nebeltextur aus überlagerten Sinuswellen, in 2x2-Blöcken."""
    b = Image.new("RGBA", (g, g))
    px = b.load()
    for y in range(0, g, 2):
        for x in range(0, g, 2):
            u, v = 2 * math.pi * x / g, 2 * math.pi * y / g
            n = 0.5 + 0.2 * math.sin(u + 2 * v) + 0.15 * math.sin(3 * u - v) + 0.15 * math.cos(2 * u + 3 * v)
            n = min(1, max(0, n))
            c = (round(100 + 40 * n), round(18 + 14 * n), round(160 + 40 * n), round(110 + 80 * n))
            for dy in (0, 1):
                for dx in (0, 1):
                    px[x + dx, y + dy] = c
    return b


def feuer(n=8, w=40, h=48):
    """Eisblaues Feuer nach dem klassischen Glut-Verfahren, deterministisch."""
    rnd = random.Random(3)
    glut = np.zeros((h, w), np.int32)
    glut[-1, 6:w - 6] = len(EIS) * 6 - 1
    bilder = []
    for schritt in range(n + 12):
        for x in range(w):
            for y in range(1, h):
                src = glut[y, x]
                r = rnd.randint(0, 3)
                nx = min(w - 1, max(0, x - r + 1))
                glut[y - 1, nx] = max(0, src - (r & 1) * 2)
        if schritt >= 12:
            b = Image.new("RGBA", (w, h))
            px = b.load()
            for y in range(h):
                for x in range(w):
                    k = glut[y, x] // 6
                    if k > 0:
                        px[x, y] = EIS[min(k, len(EIS) - 1)]
            bilder.append(b)
    return bilder


def portal(n=12, w=64, h=24):
    bilder = []
    for i in range(n):
        if i < 4:
            s = (i + 1) / 4
        elif i < 8:
            s = 1.0
        else:
            s = 1 - (i - 7) / 5
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        cx, cy = w / 2, h / 2
        rx, ry = (w / 2 - 2) * s, (h / 2 - 2) * s
        if rx < 1:
            bilder.append(b)
            continue
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(*LILA[0], 255))
        d.ellipse((cx - rx * 0.8, cy - ry * 0.75, cx + rx * 0.8, cy + ry * 0.75), fill=(10, 2, 14, 255))
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(*LILA[3], 255), width=2)
        # kreisende Punkte
        for k in range(10):
            ang = k / 10 * 2 * math.pi + i * 0.6
            x, y = cx + math.cos(ang) * rx * 0.7, cy + math.sin(ang) * ry * 0.6
            d.point((x, y), fill=(*LILA[4], 255))
        bilder.append(b)
    return bilder


# --- Effekte für Phase 2 und 3 ---------------------------------------------------

TUERKIS = [(42, 143, 154), (89, 195, 195), (168, 255, 244), (232, 255, 251)]
MAGENTA = [(58, 6, 64), (150, 20, 170), (238, 32, 251), (255, 190, 255)]


def ring_markierung(n=4, w=30, h=10, farben=TUERKIS):
    """Leuchtender Kreis am Boden (Vorwarnung)."""
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        k = 1 + (i % 2)
        d.ellipse((1, 1, w - 2, h - 2), fill=(*farben[0], 90))
        d.ellipse((1, 1, w - 2, h - 2), outline=(*farben[k + 1], 255), width=1)
        bilder.append(b)
    return bilder


def stern(n=4, w=8, h=18):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        for j in range(h - 4):
            a = int(255 * j / (h - 4))
            d.point((w // 2, j), fill=(*TUERKIS[2], a))
        d.rectangle((w // 2 - 2, h - 5, w // 2 + 1, h - 2), fill=(*TUERKIS[3], 255))
        d.point((w // 2 - 3 + (i % 3), h - 6), fill=(255, 255, 255, 255))
        bilder.append(b)
    return bilder


def einschlag(n=4, w=28, h=18):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        r = 4 + i * 3
        a = 255 - i * 50
        d.ellipse((w / 2 - r, h - 4 - r * 0.6, w / 2 + r, h - 4 + r * 0.3), outline=(*TUERKIS[2], a), width=2)
        for k in range(6):
            ang = k / 6 * math.pi + 0.3
            d.point((w / 2 + math.cos(ang) * r * 1.2, h - 5 - math.sin(ang) * r), fill=(*TUERKIS[3], a))
        bilder.append(b)
    return bilder


def sichel(n=2, w=40, h=20):
    """Lichtsichel der Windklinge, fliegt bodennah nach links (wird im Spiel gespiegelt)."""
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        d.pieslice((2, 0, w + 14, h * 2 - 2), 180, 270, fill=(*TUERKIS[2], 230))
        d.pieslice((8 + i * 2, 4, w + 18, h * 2 - 2), 180, 270, fill=(0, 0, 0, 0))
        d.arc((2, 0, w + 14, h * 2 - 2), 180, 270, fill=(*TUERKIS[3], 255), width=2)
        bilder.append(b)
    return bilder


def rune(n=4, w=56, h=16):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        hell = MAGENTA[2] if i % 2 else MAGENTA[1]
        d.ellipse((1, 1, w - 2, h - 2), fill=(*MAGENTA[0], 120))
        d.ellipse((1, 1, w - 2, h - 2), outline=(*hell, 255), width=2)
        d.ellipse((10, 4, w - 11, h - 5), outline=(*hell, 200), width=1)
        for k in range(6):
            x = 8 + k * (w - 16) / 5
            d.line((x, h / 2 - 2, x + 2, h / 2 + 2), fill=(*MAGENTA[3], 255))
        bilder.append(b)
    return bilder


def boden_riss(n=2, w=30, h=8):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        pts = [(1, 4), (7, 2), (12, 5), (18, 3), (23, 6), (28, 4)]
        d.line(pts, fill=(18, 6, 22, 255), width=4)
        d.line(pts, fill=(*TUERKIS[1 + i], 255), width=1)
        bilder.append(b)
    return bilder


def wurzel_aus_dem_boden(n=6, w=16, h=56):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        hoehe = [10, 26, 44, 52, 40, 20][i]
        for y in range(hoehe):
            t = y / max(1, hoehe)
            breite = max(1, round(6 * (1 - t)))
            x = w / 2 + 2 * math.sin(t * 4)
            d.line((x - breite, h - 1 - y, x + breite, h - 1 - y), fill=(30, 14, 22, 255))
            if y % 6 == 3:
                d.point((x - breite, h - 1 - y), fill=(*TUERKIS[1], 255))
        bilder.append(b)
    return bilder


def erinnerungswelle(n=4, w=24, h=34):
    """Welle in Brusthöhe mit flackernden Bildern vergangener Reiche."""
    bilder = []
    rnd = random.Random(11)
    for i in range(n):
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        for y in range(h):
            x = 4 + 4 * math.sin(y / 5 + i)
            d.line((x, y, x + 10, y), fill=(*TUERKIS[2], 120))
        for _ in range(10):
            d.point((rnd.randint(2, w - 3), rnd.randint(2, h - 3)), fill=(*MAGENTA[3], 255))
        bilder.append(b)
    return bilder


def lichtkugel(n=4, g=26):
    bilder = []
    for i in range(n):
        b = Image.new("RGBA", (g, g))
        d = ImageDraw.Draw(b)
        r = 6 + i * 2
        d.ellipse((g / 2 - r - 2, g / 2 - r - 2, g / 2 + r + 2, g / 2 + r + 2), fill=(*MAGENTA[2], 90))
        d.ellipse((g / 2 - r, g / 2 - r, g / 2 + r, g / 2 + r), fill=(*TUERKIS[3], 230))
        d.ellipse((g / 2 - r / 2, g / 2 - r / 2, g / 2 + r / 2, g / 2 + r / 2), fill=(255, 255, 255, 255))
        bilder.append(b)
    return bilder


def phase23_effekte():
    for name, bilder in (("fx_kreis", ring_markierung()), ("fx_rune", rune()), ("fx_stern", stern()),
                         ("fx_einschlag", einschlag()), ("fx_sichel", sichel()), ("fx_riss", boden_riss()),
                         ("fx_wurzel", wurzel_aus_dem_boden()), ("fx_welle", erinnerungswelle()),
                         ("fx_kugel", lichtkugel())):
        speichere_fx(name, bilder)


# --- Vorschau-Szenen -------------------------------------------------------------

def saal(datei="thronsaal-p2.png"):
    if datei == "p1":
        im = Image.open(os.path.join(REPO, "assets", "konzept", "thronsaal-pixel-v2.webp")).convert("RGB")
        return im.resize((W, H), Image.Resampling.BOX).quantize(colors=48).convert("RGBA")
    return Image.open(os.path.join(PSP, datei)).convert("RGBA")


def sprite_bild(name, i):
    s = Image.open(os.path.join(CUT, name + ".png")).convert("RGBA")
    import json
    meta = json.load(open(os.path.join(CUT, name + ".json"), encoding="utf-8"))
    fw = meta["frame_w"]
    n = s.width // fw
    return s.crop(((i % n) * fw, 0, (i % n) * fw + fw, s.height))


def setze_anim(bild, name, i, x_mitte, fuss_y):
    """Bild i einer Animation setzen, ausgerichtet wie Bild 0 (Sprung- und Schwebehöhe bleiben erhalten)."""
    erstes = sprite_bild(name, 0)
    unten = erstes.getbbox()[3]
    spr = sprite_bild(name, i)
    bild.alpha_composite(spr, (round(x_mitte - spr.width / 2), round(fuss_y - unten)))


def setze(bild, spr, x_mitte, fuss_y):
    """Sprite so setzen, dass seine unterste deckende Zeile auf fuss_y liegt."""
    bb = spr.getbbox()
    if not bb:
        return
    bild.alpha_composite(spr, (round(x_mitte - spr.width / 2), round(fuss_y - bb[3])))


def szene_impuls1(ring):
    bilder = []
    for i in range(10):
        b = saal("p1")
        setze_anim(b, "koenigin_p2_idle", i, 300, BODEN)
        # Held springt, wenn die Welle ihn erreicht
        j = max(0, min(7, i - 2))
        setze_anim(b, "held_sprung", j, 170, BODEN)
        r = ring[i]
        b.alpha_composite(r, (300 - 240, BODEN - r.height + 10))
        bilder.append(b)
    gif("szene_impuls1_sprung", bilder, 120)


def szene_impuls2(kachel):
    bilder = []
    for i in range(12):
        b = saal()
        setze_anim(b, "koenigin_p2_idle", i, 300, BODEN)
        t = min(1, i / 5)  # Nebel rollt von der Königin heran
        if t > 0.3:
            # goldener Schein um den Helden, solange der Schild steht
            held = sprite_bild("held_idle", i)
            schein = Image.new("RGBA", held.size)
            schein.paste((246, 217, 126, 255), (0, 0), held.getchannel("A"))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                tmp = Image.new("RGBA", b.size)
                setze_anim(tmp, "held_idle", 0, 170 + dx, BODEN + dy)
                gold = Image.new("RGBA", b.size, (246, 217, 126, 255))
                gold.putalpha(tmp.getchannel("A"))
                b.alpha_composite(gold)
        setze_anim(b, "held_idle", i, 170, BODEN)
        nebel = Image.new("RGBA", (W, H))
        for ty in range(0, H, 64):
            for tx in range(0, W, 64):
                nebel.alpha_composite(kachel, ((tx + i * 3) % (W + 64) - 64 + 0, ty))
        maske = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(maske)
        md.ellipse((300 - 600 * t, 136 - 400 * t, 300 + 600 * t, 136 + 400 * t), fill=255)
        md.ellipse((170 - 30, BODEN - 64, 170 + 30, BODEN + 8), fill=0)
        nebel.putalpha(Image.composite(nebel.getchannel("A"), Image.new("L", (W, H), 0), maske))
        b.alpha_composite(nebel)
        if t > 0.3:
            sd = ImageDraw.Draw(b)
            sd.ellipse((140, BODEN - 64, 200, BODEN + 8), outline=(246, 217, 126, 255), width=2)
        bilder.append(b)
    gif("szene_impuls2_amulett", bilder, 120)


def szene_feuer(flammen):
    bilder = []
    tod = sprite_bild("held_tod", 7)
    for i in range(16):
        b = saal()
        setze(b, tod, 175, BODEN)
        if i >= 3:
            f = flammen[(i - 3) % len(flammen)]
            setze(b, f, 175, BODEN + 2)
        setze_anim(b, "koenigin_p1_idle", i, 235, BODEN)
        bilder.append(b)
    gif("szene_ritual_feuer", bilder, 120)


def szene_portal(tor):
    bilder = []
    tod = sprite_bild("held_tod", 7)
    for i in range(12):
        b = saal()
        setze_anim(b, "koenigin_p2_idle", i, 245, BODEN)
        p = tor[i]
        b.alpha_composite(p, (175 - p.width // 2, BODEN - p.height // 2 - 2))
        # Körper sinkt ab Bild 4 ins Portal und wird dabei abgeschnitten
        sink = max(0, i - 3) * 3
        if sink < 20:
            koerper = tod.crop((0, 0, tod.width, max(1, tod.getbbox()[3] - sink)))
            setze(b, koerper, 175, BODEN)
        bilder.append(b)
    gif("szene_ritual_portal", bilder, 120)


def main():
    phase23_effekte()
    ring = impuls1_ring()
    speichere_fx("fx_impuls1_ring", ring)
    kachel = nebel_kachel()
    os.makedirs(FX, exist_ok=True)
    kachel.save(os.path.join(FX, "fx_nebel_kachel.png"))
    flammen = feuer()
    speichere_fx("fx_feuer_eisblau", flammen)
    tor = portal()
    speichere_fx("fx_portal", tor)
    szene_impuls1(ring)
    szene_impuls2(kachel)
    szene_feuer(flammen)
    szene_portal(tor)


if __name__ == "__main__":
    main()
