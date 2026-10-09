"""Thronsaal-Varianten für Phase 2 und 3 aus dem Entwurf thronsaal-pixel-v2.

Phase 2: Die Fackeln brennen türkis statt orange (Farbtausch).
Phase 3: dunkler und violetter (Platzhalter bis zum Bild nach Prompt thronsaal-p3-v1).

Alles in nativer PSP-Auflösung 480 x 272.

    python tools/cutout/thronsaal.py
"""

import colorsys
import os

from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
QUELLE = os.path.join(REPO, "assets", "konzept", "thronsaal-pixel-v2.webp")
OUT = os.path.join(REPO, "assets", "konzept", "psp")
W, H = 480, 272
BODEN = 236  # Oberkante des Bodenstreifens


def basis():
    im = Image.open(QUELLE).convert("RGB").resize((W, H), Image.Resampling.BOX)
    return im.quantize(colors=48, method=Image.Quantize.MEDIANCUT).convert("RGB")


def fackeln_tuerkis(im):
    px = im.load()
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            # Fackelschein ist rosa-orange; nur in Fackelhöhe und in den Spiegelungen am Boden
            warm = (h > 0.86 or h < 0.14) and s > 0.2 and v > 0.4
            thron = x >= 415 and v < 0.75  # Holz des Throns behält seine Farbe, nur die Kerzen wechseln
            if warm and not thron and (110 <= y <= 190 or y >= BODEN):
                # warmes Fackellicht -> eisblau-türkis, etwas heller
                nr, ng, nb = colorsys.hsv_to_rgb(0.53, min(1, s * 1.1), min(1, v * 1.15))
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255))
    return im


def phase3(im):
    """Nur Stimmung: dunkler und violetter, Fackeln türkis.

    Risse, Wurzeln und die geöffnete Decke werden nicht per Skript gezeichnet,
    das wirkte fremd im Bild. Dafür gibt es einen Prompt (assets/PROMPTS.md,
    thronsaal-p3-v1).
    """
    im = fackeln_tuerkis(im)
    dunkel = Image.new("RGB", (W, H), (40, 8, 70))
    return Image.blend(im, dunkel, 0.28)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("thronsaal-p2", lambda: fackeln_tuerkis(basis())), ("thronsaal-p3", lambda: phase3(basis()))):
        im = fn()
        im.save(os.path.join(OUT, name + ".png"))
        im.resize((W * 2, H * 2), Image.Resampling.NEAREST).save(os.path.join(OUT, name + "-2x.png"))


if __name__ == "__main__":
    main()
