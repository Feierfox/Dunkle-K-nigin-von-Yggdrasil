"""Der Untertan der Königin für die Eröffnungsszene, aus dem Helden-Entwurf abgeleitet.

Schwert entfernt (wie beim Hieb-Zuschnitt), Umhang von Grün in ein fahles
Grauviolett umgefärbt, etwas kleiner und nach vorn gebeugt.

    diener_idle   1 Bild   gebeugt stehend
    diener_gehen  8 Bilder  Beine wie bei held_gehen
    diener_knien  4 Bilder  verneigt sich tief vor der Königin (letztes Bild wird gehalten)
    diener_tod    8 Bilder  Aufblitzen, kippt nach hinten

    python tools/cutout/diener.py
"""

import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402
import gehen as GH  # noqa: E402
import held as HD  # noqa: E402

GROESSE = 0.88    # kleiner als der Held
BEUGE = -7        # Grad nach vorn gebeugt (er blickt nach rechts)


def umfaerben(bild):
    """Grüner Umhang -> fahles Grauviolett, Leder etwas dunkler."""
    a = np.array(bild).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    gruen = (g > r + 8) & (g >= b) & (a[..., 3] > 0)
    hell = 0.3 * r + 0.59 * g + 0.11 * b
    a[gruen, 0] = hell[gruen] * 0.86 + 6
    a[gruen, 1] = hell[gruen] * 0.74
    a[gruen, 2] = hell[gruen] * 0.98 + 14
    braun = (r > g + 10) & (g > b) & ~gruen
    a[braun, :3] *= 0.8
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


HUEFTE = (470, 1040)   # Drehpunkt für die Verneigung


def verneigen(bild, winkel):
    """Oberkörper (über der Hüfte) um die Hüfte drehen, Beine bleiben stehen."""
    if not winkel:
        return bild
    oben = bild.copy()
    unten = bild.copy()
    oa, ua = np.array(oben), np.array(unten)
    oa[HUEFTE[1]:] = 0
    ua[:HUEFTE[1]] = 0
    oben = Image.fromarray(oa).rotate(winkel, resample=Image.Resampling.BICUBIC, center=HUEFTE)
    erg = Image.fromarray(ua)
    erg.alpha_composite(oben)
    return erg


def pose(b, winkel=0.0, dy=0, sx=1.0, sy=1.0, weiss=0.0, pivot=None):
    fuss = (520, HD.FUESSE_Y)
    return HD.ganz(b, winkel=BEUGE + winkel, pivot=pivot or fuss, dy=dy,
                   sx=GROESSE * sx, sy=GROESSE * sy, weiss=weiss)


def main():
    bild = A.lade(HD.QUELLE)
    koerper, _schwert = HD.zerlege_held(bild)
    koerper = umfaerben(koerper)
    palette = A.palette_von(koerper, (koerper.width // HD.MASSSTAB, koerper.height // HD.MASSSTAB))
    m = HD.MASSSTAB

    HD.speichere("diener_idle", [pose(koerper)], palette)

    a = np.array(koerper)
    r, g, b = (a[..., i].astype(int) for i in range(3))
    sat, mx = GH._saettigung(a)
    umhang = (sat < 0.35) & (b > r) & (b > g) & (mx > 0.15)   # umgefärbter Umhang
    ist_bein = ~umhang
    boxen = [(130, 1110, 320, 1440), (440, 1090, 720, 1430)]
    luecke = GH._rechteck(a.shape, (120, 1080, 730, 1440))
    k, beine = GH.zerlege_beine(koerper, boxen, ist_bein, luecke)
    bilder = GH.zyklus(k, beine, 1110, 1420, schritt=2.6 * m, hub=1.0 * m, wippen=0.8 * m)
    HD.speichere("diener_gehen", [pose(bb, dy=dy) for bb, dy in bilder], palette)

    # tiefe Verneigung: Oberkörper ab der Hüfte nach vorn, dabei leicht in die Knie
    HD.speichere("diener_knien", [pose(verneigen(koerper, w), dy=d * m, sy=s)
                                  for w, d, s in [(0, 0, 1.0), (-18, 0, 0.97), (-34, 1, 0.94), (-46, 1, 0.92)]],
                 palette)

    # Tod: weiß aufblitzen, nach hinten kippen
    fuss = (520, HD.FUESSE_Y)
    tod = [(0, 0.8), (6, 0.4), (20, 0.0), (42, 0.0), (64, 0.0), (82, 0.0), (90, 0.0), (90, 0.0)]
    HD.speichere("diener_tod", [pose(koerper, winkel=w - BEUGE * (w / 90), weiss=f, pivot=fuss)
                                for w, f in tod], palette)


if __name__ == "__main__":
    main()
