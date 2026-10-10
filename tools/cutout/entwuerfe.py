"""Sprites aus den bewegten Imagegen-Entwürfen (assets/animationen/).

Jedes Entwurfsbild liegt auf einer Arbeitsfläche von 720 x 600 mit dem
Fußpunkt der Figur bei (360, 520). Pro Animation wird die ganze Fläche um
einen festen Faktor verkleinert, sodass die Figur so groß ist wie in den
übrigen Sprites. Danach: harte Transparenz, eine gemeinsame Palette mit
höchstens 32 Farben für alle Bilder, Zuschnitt auf das gemeinsame Rechteck.
Der Fußpunkt steht als "anker" im JSON und wird von tools/psp/assets_bauen.py
übernommen.

    python tools/cutout/entwuerfe.py
"""

import json
import os

import numpy as np
from PIL import Image

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


def palette_von(bilder):
    """Palette nur aus den deckenden Pixeln, damit der leere Hintergrund nicht mitzählt."""
    pixel = np.concatenate([a[a[:, :, 3] > 0][:, :3] for a in map(np.asarray, bilder)])
    streifen = Image.fromarray(pixel.reshape(1, -1, 3).astype(np.uint8), "RGB")
    return streifen.quantize(colors=FARBEN, method=Image.Quantize.MEDIANCUT)


def hoehe_deckend(bild):
    """Höhe der Figur ohne halbtransparente Randpixel."""
    kasten = bild.getchannel("A").point(lambda a: 255 if a > 110 else 0).getbbox()
    return kasten[3] - kasten[1]


def verkleinern(bild, faktor):
    w, h = round(bild.width / faktor), round(bild.height / faktor)
    klein = bild.resize((w, h), Image.Resampling.BOX)
    alpha = klein.getchannel("A").point(lambda a: 255 if a > 110 else 0)
    klein.putalpha(alpha)
    return klein


def bauen(name, entwurf, bezug, zielhoehe, anker_dx):
    meta, gross = lade(entwurf)
    hoehe = [hoehe_deckend(gross[i]) for i in bezug]
    faktor = sum(hoehe) / len(hoehe) / zielhoehe
    klein = [verkleinern(b, faktor) for b in gross]
    palette = palette_von(klein)
    bilder = []
    for b in klein:
        q = b.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
        # Transparente Pixel einheitlich (0, 0, 0, 0)
        bilder.append(Image.composite(q, Image.new("RGBA", q.size), b.getchannel("A")))
    # Gemeinsames Rechteck aller Bilder, 1 Pixel Rand
    kasten = [b.getbbox() for b in bilder if b.getbbox()]
    x0 = max(0, min(k[0] for k in kasten) - 1)
    y0 = max(0, min(k[1] for k in kasten) - 1)
    x1 = min(bilder[0].width, max(k[2] for k in kasten) + 1)
    y1 = min(bilder[0].height, max(k[3] for k in kasten) + 1)
    fw, fh = x1 - x0, y1 - y0
    anker = (round(meta["anchor"]["x"] / faktor) - x0 + anker_dx, round(meta["anchor"]["y"] / faktor) - y0)
    dauer = [f["durationTicks"] for f in meta["frames"]]

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
             "quelle": "animationen/entwuerfe-2026-10-10/" + entwurf,
             "frames": [{"x": i * fw, "y": 0, "w": fw, "h": fh} for i in range(len(bilder))]}
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=1)
    vorschau[0].save(os.path.join(OUT, name + "_vorschau.gif"), save_all=True, append_images=vorschau[1:],
                     duration=[round(1000 * t / 12) for t in dauer], loop=0)
    a = np.asarray(sheet)
    farben = len(np.unique(a[a[:, :, 3] > 0][:, :3], axis=0))
    print(f"{name}: {len(bilder)} Bilder, {fw} x {fh}, Faktor {faktor:.2f}, Anker {anker}, {farben} Farben")


def main():
    for a in ANIMATIONEN:
        bauen(*a)


if __name__ == "__main__":
    main()
