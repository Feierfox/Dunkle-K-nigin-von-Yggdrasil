"""Angriffe als Cut-out-Animation direkt aus den Konzeptbildern.

Aus dem Entwurf wird ein bewegliches Teil ausgeschnitten (Sense mit Hand
und Unterarm). Die Lücke am Körper wird mit den angrenzenden Farben
aufgefüllt. Pro Animationsbild werden Körper und Teil verschoben bzw. um
ein Gelenk gedreht, auf Sprite-Größe verkleinert und auf die Palette der
Figur gebunden.

    python tools/cutout/angriffe.py
"""

import json
import os

import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KONZEPT = os.path.join(REPO, "assets", "konzept")
OUT = os.path.join(REPO, "assets", "sprites", "cutout")
# Maßstab: 16 Bildpixel des Entwurfs ergeben 1 Sprite-Pixel (wie verformen.py)
MASSSTAB = 16


def lade(name):
    return Image.open(os.path.join(KONZEPT, name)).convert("RGBA")


def maske(groesse, polygone):
    m = Image.new("L", groesse, 0)
    d = ImageDraw.Draw(m)
    for p in polygone:
        d.polygon(p, fill=255)
    return m


def zerlege(bild, teil_polygone, fuell_polygone):
    """Trennt Teil und Körper. Fuell_polygone: Stellen am Körper, die das Teil verdeckt."""
    teil_m = maske(bild.size, teil_polygone)
    teil = Image.new("RGBA", bild.size)
    teil.paste(bild, (0, 0), teil_m)
    koerper = bild.copy()
    leer = Image.new("RGBA", bild.size)
    koerper.paste(leer, (0, 0), teil_m)
    # Lücke im Körper zeilenweise von rechts mit der Rüstungsfarbe auffüllen
    a = np.array(koerper)
    fm = np.array(maske(bild.size, fuell_polygone)) > 0
    ys, xs = np.nonzero(fm)
    for y in np.unique(ys):
        zeile = xs[ys == y]
        for x in sorted(zeile, reverse=True):
            if a[y, x, 3] == 0 and x + 1 < a.shape[1] and a[y, x + 1, 3] > 0:
                a[y, x] = a[y, x + 1]
    return Image.fromarray(a), teil


def palette_von(bild, groesse, farben=24):
    klein = bild.resize(groesse, Image.Resampling.BOX).convert("RGB")
    return klein.quantize(colors=farben, method=Image.Quantize.MEDIANCUT)


def zu_sprite(bild, palette):
    w, h = bild.size
    klein = bild.resize((w // MASSSTAB, h // MASSSTAB), Image.Resampling.BOX)
    alpha = klein.getchannel("A").point(lambda a: 255 if a > 110 else 0)
    q = klein.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
    q.putalpha(alpha)
    return q


def bild_zusammensetzen(leinwand, ursprung, koerper, teil, gelenk, pose):
    """pose: (winkel, koerper_dx, koerper_dy, teil_dx, teil_dy).

    Winkel in Grad, positiv = gegen den Uhrzeigersinn. Das Teil dreht sich um
    das Gelenk und wird danach zusätzlich verschoben (Arm heben/senken).
    """
    winkel, kdx, kdy, tdx, tdy = pose
    fl = Image.new("RGBA", leinwand)
    ox, oy = ursprung[0] + kdx, ursprung[1] + kdy
    fl.alpha_composite(koerper, (ox, oy))
    gx, gy = gelenk
    # Teil auf eine größere Fläche legen, damit beim Drehen nichts abgeschnitten wird
    rand = 1200
    gross = Image.new("RGBA", (teil.width + 2 * rand, teil.height + 2 * rand))
    gross.alpha_composite(teil, (rand, rand))
    gedreht = gross.rotate(winkel, resample=Image.Resampling.BICUBIC, center=(gx + rand, gy + rand))
    _sicher(fl, gedreht, ox - rand + tdx, oy - rand + tdy)
    return fl


def _sicher(ziel, quelle, x, y):
    """alpha_composite mit negativen Koordinaten."""
    sx, sy = max(0, -x), max(0, -y)
    quelle = quelle.crop((sx, sy, min(quelle.width, sx + ziel.width - max(0, x)),
                          min(quelle.height, sy + ziel.height - max(0, y))))
    ziel.alpha_composite(quelle, (max(0, x), max(0, y)))


def speichere(name, bilder, palette, quelle):
    w, h = bilder[0].size
    sw, sh = w // MASSSTAB, h // MASSSTAB
    sheet = Image.new("RGBA", (sw * len(bilder), sh))
    frames = []
    for i, b in enumerate(bilder):
        spr = zu_sprite(b, palette)
        sheet.paste(spr, (i * sw, 0))
        bg = Image.new("RGBA", spr.size, (28, 24, 44, 255))
        bg.alpha_composite(spr)
        frames.append(bg.resize((sw * 4, sh * 4), Image.Resampling.NEAREST).convert("P"))
    os.makedirs(OUT, exist_ok=True)
    sheet.save(os.path.join(OUT, name + ".png"))
    meta = {"name": name, "frame_w": sw, "frame_h": sh, "fps": 12, "quelle": quelle,
            "frames": [{"x": i * sw, "y": 0, "w": sw, "h": sh} for i in range(len(bilder))]}
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    frames[0].save(os.path.join(OUT, name + "_vorschau.gif"), save_all=True, append_images=frames[1:],
                   duration=1000 // 12, loop=0)


# --- Königin -----------------------------------------------------------------
# Koordinaten im Entwurf koenigin-idle-sense-helm-v5 (1024 x 1536)
SENSE_ARM = [
    [(0, 0), (395, 0), (395, 1536), (0, 1536)],          # Sense links vom Körper
    [(395, 0), (462, 0), (462, 310), (395, 310)],          # Astgabel und Kristall oben
    [(360, 690), (452, 690), (458, 790), (360, 790)],      # Unterarm bis zum Ellbogen
]
UNTERARM = [SENSE_ARM[2]]
ELLBOGEN = (450, 740)


def richtschlag():
    quelle = "koenigin-idle-sense-helm-v5.webp"
    bild = lade(quelle)
    koerper, teil = zerlege(bild, SENSE_ARM, UNTERARM)
    palette = palette_von(bild, (bild.width // MASSSTAB, bild.height // MASSSTAB))
    leinwand = (2048, 2048)
    ursprung = (820, leinwand[1] - bild.height - 32)
    # (Winkel, Körper dx/dy, Teil dx/dy) je Bild in Entwurfspixeln.
    # Negativer Winkel: Sense kippt nach hinten; negatives Teil-dy: Arm hebt sich.
    posen = [
        (0, 0, 0, 0, 0),            # 1 Ruhe
        (-20, 4, -6, 30, -110),     # 2 Ausholen
        (-38, 8, -12, 60, -190),    # 3
        (-48, 10, -14, 70, -220),   # 4 höchster Punkt
        (-50, 10, -14, 70, -220),   # 5 halten
        (55, -14, 10, -40, 40),     # 6 Schlag
        (72, -18, 16, -55, 60),     # 7 Blatt im Boden
        (66, -16, 14, -50, 50),     # 8
        (32, -8, 6, -20, 20),       # 9 Erholung
        (8, -2, 0, 0, 0),           # 10
    ]
    bilder = [bild_zusammensetzen(leinwand, ursprung, koerper, teil, ELLBOGEN, p) for p in posen]
    speichere("koenigin_p1_atk_richtschlag", bilder, palette, quelle)


if __name__ == "__main__":
    richtschlag()
