"""Thronsaal-Varianten für Phase 2 und 3 aus dem Entwurf thronsaal-pixel-v2.

Phase 2: Die Fackeln brennen türkis statt orange (Farbtausch).
Phase 3: dunkler und violetter, leuchtende Risse im Boden, Wurzeln brechen
durch, die Decke zeigt Risse mit Nachthimmel dahinter.

Alles in nativer PSP-Auflösung 480 x 272.

    python tools/cutout/thronsaal.py
"""

import colorsys
import math
import os
import random

from PIL import Image, ImageDraw

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
    im = fackeln_tuerkis(im)
    # dunkler und violetter
    dunkel = Image.new("RGB", (W, H), (40, 8, 70))
    im = Image.blend(im, dunkel, 0.28)
    d = ImageDraw.Draw(im)
    rnd = random.Random(7)
    # Deckenrisse mit Nachthimmel
    for x0 in (120, 250, 360):
        pts = [(x0, 0)]
        x, y = x0, 0
        while y < 46:
            x += rnd.randint(-6, 6)
            y += rnd.randint(4, 8)
            pts.append((x, y))
        for i in range(len(pts) - 1):
            breite = max(1, 5 - i)
            d.line([pts[i], pts[i + 1]], fill=(8, 10, 32), width=breite)
        for _ in range(4):
            sx, sy = pts[rnd.randint(0, len(pts) - 2)]
            d.point((sx + rnd.randint(-1, 1), sy), fill=(220, 230, 255))
    # leuchtende Risse im Boden
    for x0 in (60, 150, 300, 410):
        x, y = x0, BODEN + 4
        pts = [(x, y)]
        for _ in range(6):
            x += rnd.randint(6, 12) * (1 if x0 < 240 else -1)
            y += rnd.randint(-1, 3)
            pts.append((x, min(H - 2, y)))
        d.line(pts, fill=(18, 6, 22), width=5)
        d.line(pts, fill=(42, 143, 154), width=3)
        d.line(pts, fill=(168, 255, 244), width=1)
    # Wurzeln brechen durch den Boden
    def wurzel(x0, y0, hoehe, neig, breite, tiefe=0):
        pts = []
        for i in range(12):
            t = i / 11
            pts.append((x0 + neig * hoehe * t + 5 * math.sin(t * 4 + x0), y0 - hoehe * t))
        for i in range(len(pts) - 1):
            w = max(1, round(breite * (1 - i / 11)))
            d.line([pts[i], pts[i + 1]], fill=(26, 12, 20), width=w)
            if w >= 3:
                # schwacher türkiser Rand auf der Lichtseite
                d.point((pts[i][0] - w // 2, pts[i][1]), fill=(42, 143, 154))
        if tiefe == 0:
            for k in (4, 7):
                wurzel(pts[k][0], pts[k][1], hoehe * 0.45, -neig * 1.6, breite * 0.45, 1)

    for x0, hoehe, neig, breite in ((30, 110, 0.35, 14), (85, 60, -0.25, 9), (445, 120, -0.4, 15),
                                    (395, 70, 0.3, 10), (240, 35, 0.1, 6)):
        wurzel(x0, BODEN + 8, hoehe, neig, breite)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("thronsaal-p2", lambda: fackeln_tuerkis(basis())), ("thronsaal-p3", lambda: phase3(basis()))):
        im = fn()
        im.save(os.path.join(OUT, name + ".png"))
        im.resize((W * 2, H * 2), Image.Resampling.NEAREST).save(os.path.join(OUT, name + "-2x.png"))


if __name__ == "__main__":
    main()
