"""Ausrüstungsstufen des Helden als Farbtausch und Mockup des Amulett-Schilds.

Auf der PSP kostet ein Farbtausch fast nichts: dasselbe Sprite, nur eine
andere Palette (CLUT). Dieses Skript zeigt die fünf Stufen:

    1 Herz   Waldgrün (Start)
    2 Herzen Tannengrün, Saum silbergrau
    3 Herzen Smaragd, kräftiger
    4 Herzen Smaragd mit Goldsaum, Amulett
    5 Herzen Tiefes Königsgrün mit Goldsaum, legendäres goldenes Schwert

    python tools/cutout/ausruestung.py
"""

import colorsys
import os

from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SPRITES = os.path.join(REPO, "assets", "sprites", "cutout")
PSP = os.path.join(REPO, "assets", "konzept", "psp")

# (Farbton-Verschiebung in Grad, Sättigung ×, Helligkeit ×, Saum, Schwert)
STUFEN = [
    ("1_waldgruen", 0, 1.0, 1.0, None, None),
    ("2_tannengruen", 22, 0.85, 1.05, "silber", None),
    ("3_smaragd", 8, 1.45, 1.25, "silber", None),
    ("4_smaragd_gold", 8, 1.45, 1.25, "gold", None),
    ("5_koenigsgruen_gold", 18, 1.6, 1.15, "gold", "gold"),
]
GOLD = [(0x5a, 0x3d, 0x12), (0x9a, 0x6e, 0x22), (0xd4, 0xa2, 0x38), (0xf6, 0xd9, 0x7e)]
SILBER = [(0x4a, 0x50, 0x58), (0x8a, 0x92, 0x9c), (0xc8, 0xcd, 0xd4)]
SCHWERT_AB_X = 16
# Lage des Amuletts im Sprite (40 x 60)
AMULETT = [(17, 22), (18, 22), (17, 23), (18, 23)]  # Graue Pixel rechts davon gehören zum Schwert, links zu den Armschienen


def hsv(c):
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))


def rampe(farben, helligkeit):
    i = min(len(farben) - 1, int(helligkeit * len(farben)))
    return farben[i]


def faerbe(sprite, stufe):
    _, dh, ds, dv, saum, schwert = stufe
    im = sprite.copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = hsv((r, g, b))
            gruen = 0.25 < h < 0.5 and s > 0.15
            if gruen and s < 0.26 and v > 0.29 and saum:
                # heller, entsättigter Saum
                c = rampe(GOLD if saum == "gold" else SILBER, min(0.999, v * 2.2))
                px[x, y] = (*c, a)
            elif gruen:
                nh = (h + dh / 360) % 1.0
                nr, ng, nb = colorsys.hsv_to_rgb(nh, min(1, s * ds), min(1, v * dv))
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
            elif schwert and s < 0.12 and v > 0.35 and x >= SCHWERT_AB_X:
                px[x, y] = (*rampe(GOLD, min(0.999, v)), a)
    if saum == "gold":
        # Amulett auf der Brust ab Stufe 4
        for (x, y), c in zip(AMULETT, (GOLD[3], GOLD[2], GOLD[2], GOLD[1])):
            if px[x, y][3]:
                px[x, y] = (*c, 255)
    return im


def stufen_bild():
    quelle = Image.open(os.path.join(SPRITES, "held_idle.png"))
    w, h = 40, 60
    sprite = quelle.crop((0, 0, w, h)).convert("RGBA")
    bogen = Image.new("RGBA", (w * len(STUFEN), h))
    for i, st in enumerate(STUFEN):
        bogen.paste(faerbe(sprite, st), (i * w, 0))
    bogen.save(os.path.join(SPRITES, "held_stufen.png"))
    bg = Image.new("RGBA", bogen.size, (28, 24, 44, 255))
    bg.alpha_composite(bogen)
    bg.resize((bogen.width * 4, bogen.height * 4), Image.Resampling.NEAREST).save(
        os.path.join(SPRITES, "held_stufen_vorschau.png"))
    return [faerbe(sprite, st) for st in STUFEN]


def mockup_impuls(held_stufe4):
    """Impuls beim Wechsel zu Phase 3: lila Nebel überall, außer im Schild des Helden."""
    saal = Image.open(os.path.join(REPO, "assets", "konzept", "thronsaal-pixel-v2.webp")).convert("RGB")
    saal = saal.resize((480, 272), Image.Resampling.BOX).quantize(colors=48).convert("RGBA")
    koenigin = Image.open(os.path.join(PSP, "koenigin-p2-helmbruch-64x96.png")).convert("RGBA")
    boden = 240
    hx, kx = 170, 262
    saal.alpha_composite(koenigin, (kx, boden - koenigin.height - 5))
    # goldener Schein um den Helden
    glanz = Image.new("RGBA", held_stufe4.size)
    a = held_stufe4.getchannel("A")
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        glanz.paste((246, 217, 126, 255), (dx, dy), a)
    saal.alpha_composite(glanz, (hx, boden - held_stufe4.height))
    saal.alpha_composite(held_stufe4, (hx, boden - held_stufe4.height))
    # Nebel mit Aussparung für den Schild
    cx, cy, rx, ry = hx + 18, boden - 28, 30, 36
    nebel = Image.new("RGBA", saal.size, (122, 24, 190, 0))
    nd = ImageDraw.Draw(nebel)
    import math
    for y in range(0, 272, 4):
        for x in range(0, 480, 4):
            # weiche Schwaden in 4x4-Blöcken
            n = 0.5 + 0.25 * math.sin(x / 37 + y / 23) + 0.25 * math.sin(x / 13 - y / 29)
            nd.rectangle((x, y, x + 3, y + 3), fill=(round(100 + 40 * n), round(18 + 14 * n), round(160 + 40 * n),
                                                     round(120 + 60 * n)))
    loch = Image.new("L", saal.size, 255)
    ImageDraw.Draw(loch).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=0)
    nebel.putalpha(Image.composite(nebel.getchannel("A"), Image.new("L", saal.size, 0), loch))
    saal.alpha_composite(nebel)
    # Schild: goldener Rand und schwacher goldener Schimmer innen
    schild = Image.new("RGBA", saal.size)
    sd = ImageDraw.Draw(schild)
    sd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(246, 217, 126, 40))
    sd.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(246, 217, 126, 255), width=2)
    sd.ellipse((cx - rx + 3, cy - ry + 3, cx + rx - 3, cy + ry - 3), outline=(212, 162, 56, 160), width=1)
    saal.alpha_composite(schild)
    # Die Königin bleibt über dem Nebel sichtbar, von ihr geht der Impuls aus
    schein = Image.new("RGBA", koenigin.size)
    schein.paste((223, 128, 255, 255), (0, 0), koenigin.getchannel("A"))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        saal.alpha_composite(schein, (kx + dx, boden - koenigin.height - 5 + dy))
    saal.alpha_composite(koenigin, (kx, boden - koenigin.height - 5))
    saal.convert("RGB").save(os.path.join(PSP, "mockup-impuls2-amulett.png"))
    saal.convert("RGB").resize((960, 544), Image.Resampling.NEAREST).save(os.path.join(PSP, "mockup-impuls2-amulett-2x.png"))


if __name__ == "__main__":
    stufen = stufen_bild()
    mockup_impuls(stufen[3])
