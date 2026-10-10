"""Gehen als Cut-out direkt aus den Konzeptbildern.

Die Beine werden aus dem Entwurf ausgeschnitten (Bereich unter dem Umhang
bzw. Rüstungsrock, ohne Umhangfarben). Die Lücke dahinter wird von den
Rändern her mit den angrenzenden Farben gefüllt. Je Bild werden die Beine
geschert: Die Hüfte bleibt, der Fuß schwingt vor und zurück und hebt sich
beim Vorschwingen. Dazu wippt der ganze Körper.

    held_gehen          8 Bilder  64 x 80, Anker wie held_sprung
    koenigin_p1_gehen   8 Bilder  128 x 128, Anker wie die Angriffe in Phase 1

    python tools/cutout/gehen.py
"""

import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402
import held as HD  # noqa: E402
from verformen import verforme  # noqa: E402

BILDER = 8


def _saettigung(a):
    rgb = a[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    return np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0), mx


def _rechteck(shape, box):
    m = np.zeros(shape[:2], bool)
    x0, y0, x1, y1 = box
    m[y0:y1, x0:x1] = True
    return m


def _loecher_fuellen(a, loch):
    """Lochpixel innerhalb der Silhouette mit der Farbe eines deckenden Nachbarn füllen."""
    a = a.copy()
    for _ in range(300):
        deckend = a[..., 3] > 0
        nachbarn = np.zeros(deckend.shape, np.int32)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    nachbarn += np.roll(np.roll(deckend, dy, 0), dx, 1)
        neu = loch & ~deckend & (nachbarn >= 3)
        if not neu.any():
            break
        quelle = a.copy()
        for dy, dx in ((0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)):
            nb = np.roll(np.roll(quelle, -dy, 0), -dx, 1)
            setzen = neu & (a[..., 3] == 0) & (nb[..., 3] > 0)
            a[setzen] = nb[setzen]
    return a


def zerlege_beine(bild, boxen, ist_bein, luecke):
    """Gibt (Körper ohne Beine, [Bein je Box]) als float-Arrays zurück.

    luecke: Bereich, in dem die freigewordenen Stellen hinter den Beinen gefüllt werden.
    """
    a = np.array(bild)
    beine = []
    alle = np.zeros(a.shape[:2], bool)
    for box in boxen:
        m = _rechteck(a.shape, box) & ist_bein & (a[..., 3] > 0) & ~alle
        b = np.zeros_like(a)
        b[m] = a[m]
        beine.append(b.astype(np.float32))
        alle |= m
    koerper = a.copy()
    koerper[alle] = 0
    koerper = _loecher_fuellen(koerper, alle & luecke)
    return koerper.astype(np.float32), beine


def scheren(bein, oben, unten, versatz, heben):
    """Hüfte (oben) fest, Fuß (unten) um versatz nach vorn und um heben nach oben."""
    h, w, _ = bein.shape
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32)
    g = np.clip((yy - oben) / float(unten - oben), 0, 1)
    return verforme(bein, versatz * g, -heben * g * g)


def ueber(unten, oben):
    """Alpha-Compositing zweier float-RGBA-Arrays."""
    ao = oben[..., 3:4] / 255
    return oben * ao + unten * (1 - ao)


def zyklus(koerper, beine, oben, unten, schritt, hub, wippen):
    """8 Bilder: Bein 0 und Bein 1 schwingen gegenläufig."""
    bilder = []
    for i in range(BILDER):
        t = 2 * math.pi * i / BILDER
        s = math.sin(t)
        lagen = []
        for k, bein in enumerate(beine):
            v = s if k == 0 else -s
            # gehoben wird das Bein, das gerade nach vorn schwingt
            vor = math.cos(t) if k == 0 else -math.cos(t)
            lagen.append(scheren(bein, oben, unten, v * schritt, max(0.0, vor) * hub))
        bild = koerper
        # das hintere Bein zuerst, das vordere darüber
        for k in sorted(range(len(beine)), key=lambda k: (s if k == 0 else -s)):
            bild = ueber(bild, lagen[k])
        dy = -abs(math.cos(t)) * wippen   # höchster Punkt, wenn die Beine aneinander vorbeigehen
        bilder.append((Image.fromarray(np.clip(bild, 0, 255).astype(np.uint8), "RGBA"), round(dy)))
    return bilder


def held():
    bild = A.lade(HD.QUELLE)
    a = np.array(bild)
    sat, mx = _saettigung(a)
    r, g, b = (a[..., i].astype(int) for i in range(3))
    gruen = (g > r + 8) & (g >= b)              # Umhang
    ist_bein = ~gruen & ~HD._schwert_maske(bild)
    # vorderes (linkes) und hinteres (rechtes) Bein unterhalb des Umhangsaums
    boxen = [(130, 1110, 320, 1440), (440, 1090, 720, 1430)]
    luecke = _rechteck(a.shape, (120, 1080, 730, 1440))
    koerper, beine = zerlege_beine(bild, boxen, ist_bein, luecke)
    palette = A.palette_von(bild, (bild.width // HD.MASSSTAB, bild.height // HD.MASSSTAB))
    m = HD.MASSSTAB
    bilder = zyklus(koerper, beine, 1110, 1420, schritt=3.2 * m, hub=1.2 * m, wippen=1.0 * m)
    HD.speichere("held_gehen", [HD.ganz(b, dy=dy) for b, dy in bilder], palette)


def koenigin():
    quelle = "koenigin-idle-sense-helm-v5.webp"
    bild = A.lade(quelle)
    a = np.array(bild)
    sat, mx = _saettigung(a)
    r, g, b = (a[..., i].astype(int) for i in range(3))
    umhang = (sat > 0.45) & (b > g + 40) & (mx > 0.3)   # kräftiges Lila des Umhangs
    ist_bein = ~umhang
    boxen = [(360, 1040, 497, 1495), (497, 1040, 660, 1495)]
    luecke = _rechteck(a.shape, (350, 1030, 670, 1500))
    koerper, beine = zerlege_beine(bild, boxen, ist_bein, luecke)
    palette = A.palette_von(bild, (bild.width // A.MASSSTAB, bild.height // A.MASSSTAB))
    leinwand = (2048, 2048)
    ursprung = (820, leinwand[1] - bild.height - 32)
    m = A.MASSSTAB
    bilder = []
    for b, dy in zyklus(koerper, beine, 1040, 1490, schritt=3.5 * m, hub=1.0 * m, wippen=1.0 * m):
        fl = Image.new("RGBA", leinwand)
        fl.alpha_composite(b, (ursprung[0], ursprung[1] + dy))
        bilder.append(fl)
    A.MASSSTAB = 16
    A.speichere("koenigin_p1_gehen", bilder, palette, quelle)


if __name__ == "__main__":
    held()
    koenigin()
