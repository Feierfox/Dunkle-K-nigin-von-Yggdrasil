"""Bewegungen des Helden direkt aus dem Entwurf held-idle-hood-v3.

    held_sprung     8 Bilder  Sprung (über bodennahe Angriffe und den ersten Impuls)
    held_rolle      8 Bilder  Ausweichrolle auf der Stelle; die Engine bewegt ihn dabei vorwärts
    held_atk_hieb   8 Bilder  Schwerthieb, Schwert mit Hand ausgeschnitten
    held_treffer    4 Bilder  Treffer: Aufblitzen und Zurückweichen
    held_tod        8 Bilder  Tod: kippt nach hinten, letztes Bild ist der liegende Körper

    python tools/cutout/held.py
"""

import colorsys
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402

QUELLE = "held-idle-hood-v3.webp"
# 28 Entwurfspixel = 1 Sprite-Pixel (wie held_idle aus verformen.py)
MASSSTAB = 28
LEINWAND = (64 * MASSSTAB, 80 * MASSSTAB)  # 64 x 80 Sprite-Pixel
FUESSE_Y = 1422                            # Unterkante der Stiefel im Entwurf
HAND = (300, 880)                          # Griff des Schwerts
MITTE = (500, 900)                         # Körpermitte

# Schwert: Band entlang der Klinge plus Hand und Knauf
KLINGE_A, KLINGE_B = (330, 885), (985, 1200)


def _schwert_maske(bild):
    w, h = bild.size
    m = Image.new("L", bild.size, 0)
    d = ImageDraw.Draw(m)
    d.rectangle((200, 835, 352, 935), fill=255)  # Knauf, Hand, Parierstange
    ax, ay = KLINGE_A
    bx, by = KLINGE_B
    nx, ny = -(by - ay), (bx - ax)
    ln = math.hypot(nx, ny)
    nx, ny = nx / ln * 50, ny / ln * 50
    d.polygon([(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], fill=128)
    a = np.array(bild)
    mm = np.array(m)
    # Im Klingenband nur graue, weiße und schwarze Pixel (Stahl und Umriss), nicht Umhang oder Hose
    rgb = a[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    band = (mm == 128) & (a[..., 3] > 0) & ((sat < 0.38) | (mx < 0.2))
    return (mm == 255) & (a[..., 3] > 0) | band


def zerlege_held(bild):
    a = np.array(bild)
    sm = _schwert_maske(bild)
    teil = np.zeros_like(a)
    teil[sm] = a[sm]
    koerper = a.copy()
    koerper[sm] = 0
    # Lücke im Umhang von den Rändern her schließen: ein Lochpixel bekommt die Farbe
    # eines deckenden Nachbarn, sobald mindestens 5 seiner 8 Nachbarn deckend sind.
    # Nur Lochpixel innerhalb der Silhouette: in derselben Zeile links und rechts Körper
    deckend0 = koerper[..., 3] > 0
    links = np.maximum.accumulate(deckend0, axis=1)
    rechts = np.maximum.accumulate(deckend0[:, ::-1], axis=1)[:, ::-1]
    loch = sm & links & rechts
    for _ in range(200):
        deckend = koerper[..., 3] > 0
        nachbarn = np.zeros(deckend.shape, np.int32)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    nachbarn += np.roll(np.roll(deckend, dy, 0), dx, 1)
        neu = loch & ~deckend & (nachbarn >= 3)
        if not neu.any():
            break
        ys, xs = np.nonzero(neu)
        for y, x in zip(ys, xs):
            for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                if koerper[y + dy, x + dx, 3] > 0:
                    koerper[y, x] = koerper[y + dy, x + dx]
                    break
    return Image.fromarray(koerper), Image.fromarray(teil)


def ursprung(bild):
    return (300, LEINWAND[1] - FUESSE_Y - 2 * MASSSTAB)


def ganz(bild, winkel=0.0, pivot=MITTE, dx=0, dy=0, sx=1.0, sy=1.0, weiss=0.0):
    """Ganzer Körper verschoben, gedreht und gestaucht (Stauchung zu den Füßen hin)."""
    fl = Image.new("RGBA", LEINWAND)
    b = bild
    if sx != 1.0 or sy != 1.0:
        nw, nh = round(b.width * sx), round(b.height * sy)
        b2 = b.resize((nw, nh), Image.Resampling.BICUBIC)
        b = Image.new("RGBA", bild.size)
        b.alpha_composite(b2, ((bild.width - nw) // 2, FUESSE_Y - round(FUESSE_Y * sy)))
    if weiss:
        hell = Image.new("RGBA", b.size, (255, 255, 255, 255))
        hell.putalpha(b.getchannel("A"))
        b = Image.blend(b, hell, weiss)
    rand = 900
    gross = Image.new("RGBA", (b.width + 2 * rand, b.height + 2 * rand))
    gross.alpha_composite(b, (rand, rand))
    gross = gross.rotate(winkel, resample=Image.Resampling.BICUBIC, center=(pivot[0] + rand, pivot[1] + rand))
    ox, oy = ursprung(bild)
    A._sicher(fl, gross, ox + dx - rand, oy + dy - rand)
    return fl


def speichere(name, bilder, palette):
    A.MASSSTAB = MASSSTAB
    A.speichere(name, bilder, palette, QUELLE)


def main():
    bild = A.lade(QUELLE)
    palette = A.palette_von(bild, (bild.width // MASSSTAB, bild.height // MASSSTAB))
    m = MASSSTAB

    # Sprung: Ducken, Abheben, höchster Punkt, Landen (Höhe in Sprite-Pixeln)
    hoehe = [0, 0, 6, 14, 18, 14, 6, 0]
    stauch = [1.0, 0.9, 1.04, 1.0, 1.0, 1.0, 1.02, 0.92]
    speichere("held_sprung", [ganz(bild, dy=-h * m, sy=s, sx=2 - s) for h, s in zip(hoehe, stauch)], palette)

    # Rolle vorwärts (nach rechts = im Uhrzeigersinn), zusammengerollt; Bilder 2-6 unverwundbar
    rolle = [(0, 1.0, 0), (-40, 0.86, 2), (-120, 0.74, 6), (-200, 0.7, 7), (-280, 0.74, 6),
             (-340, 0.86, 3), (-360, 0.96, 1), (-360, 1.0, 0)]
    speichere("held_rolle", [ganz(bild, winkel=w, sx=s, sy=s, dy=d * m) for w, s, d in rolle], palette)

    # Schwerthieb: (Winkel, Körper dx/dy, Schwert dx/dy) in Entwurfspixeln, Drehpunkt Hand
    koerper, teil = zerlege_held(bild)
    lw = LEINWAND
    hieb = [(0, 0, 0, 0, 0), (60, -10, 0, 20, -80), (125, -20, -10, 40, -170), (135, -24, -10, 40, -190),
            (30, 40, 10, 140, -60), (5, 46, 20, 150, -20), (-15, 20, 10, 70, 0), (0, 0, 0, 0, 0)]
    A.MASSSTAB = MASSSTAB
    bilder = [A.bild_zusammensetzen(lw, ursprung(bild), koerper, teil, HAND, p) for p in hieb]
    speichere("held_atk_hieb", bilder, palette)

    # Treffer: weißes Aufblitzen, Zurückweichen nach links
    treffer = [(-1 * m, 0.7), (-3 * m, 0.25), (-2 * m, 0.0), (0, 0.0)]
    speichere("held_treffer", [ganz(bild, dx=dx, weiss=w) for dx, w in treffer], palette)

    # Tod: kippt nach hinten (nach links, gegen den Uhrzeigersinn) um die Füße
    fuss = (520, FUESSE_Y)
    tod = [0, 8, 24, 45, 68, 84, 90, 90]
    speichere("held_tod", [ganz(bild, winkel=w, pivot=fuss, dx=-round(w / 90 * 6 * m)) for w in tod], palette)


if __name__ == "__main__":
    main()
