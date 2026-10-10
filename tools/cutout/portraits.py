"""Porträts für die Dialogbox, 48 x 48, aus den Konzeptbildern.

    portrait_koenigin  Helm mit Astkrone und leuchtenden Augen (koenigin-helm-lila-v1);
                       die Verderbnis nutzt dasselbe Bild magenta eingefärbt (im Spiel)
    portrait_held      Kapuze, Riemen und Arm (held-idle-hood-v3); im Spiel mit den
                       Farbtabellen seiner Ausrüstungsstufe
    portrait_diener    dasselbe, burgunderrot, mit Bauch, gespiegelt

    python tools/cutout/portraits.py
"""

import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402
import diener as DN  # noqa: E402

GROESSE = 48
HINTERGRUND = (30, 22, 40, 255)


def portrait(name, bild, box, spiegeln=False):
    ausschnitt = bild.crop(box)
    grund = Image.new("RGBA", ausschnitt.size, HINTERGRUND)
    grund.alpha_composite(ausschnitt.convert("RGBA"))
    klein = grund.convert("RGB").resize((GROESSE, GROESSE), Image.Resampling.BOX)
    if spiegeln:
        klein = klein.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    q = klein.quantize(colors=40, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    q.save(os.path.join(A.OUT, name + ".png"))
    meta = {"name": name, "frame_w": GROESSE, "frame_h": GROESSE, "fps": 12, "anker": [0, 0],
            "quelle": "portraits.py",
            "frames": [{"x": 0, "y": 0, "w": GROESSE, "h": GROESSE}]}
    with open(os.path.join(A.OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)


def main():
    koenigin = Image.open(os.path.join(A.REPO, "assets", "menu", "koenigin-preview-v1",
                                       "koenigin-helm-lila-v1.png"))
    portrait("portrait_koenigin", koenigin, (330, 0, 730, 400))
    held = A.lade("held-idle-hood-v3.webp")
    portrait("portrait_held", held, (220, 200, 680, 660))
    portrait("portrait_diener", DN.bauch(DN.umfaerben(held)), (200, 220, 700, 720), spiegeln=True)


if __name__ == "__main__":
    main()
