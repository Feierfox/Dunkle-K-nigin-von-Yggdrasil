"""Animationen direkt aus den Konzeptbildern (Verformung statt Neuzeichnen).

Jedes Bild wird pro Animationsbild über ein Verschiebungsfeld verformt:
Atmen (Oberkörper hebt sich), Mantel und Haar wehen (wellenförmige
Verschiebung, nach außen und unten stärker), Schweben (ganzer Körper).
Danach wird auf Sprite-Größe verkleinert und auf eine feste Palette
gebunden, die für alle Bilder einer Animation gleich ist (kein Flimmern).

    python tools/cutout/verformen.py
"""

import json
import math
import os

import numpy as np
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KONZEPT = os.path.join(REPO, "assets", "konzept")
OUT = os.path.join(REPO, "assets", "sprites", "cutout")


def lade(name):
    return np.asarray(Image.open(os.path.join(KONZEPT, name)).convert("RGBA")).astype(np.float32)


def glatt(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def verforme(src, dx, dy):
    """Rückwärtsabbildung: Zielpixel (x, y) liest Quelle (x - dx, y - dy), bilinear."""
    h, w, _ = src.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sx = np.clip(xx - dx, 0, w - 1.001)
    sy = np.clip(yy - dy, 0, h - 1.001)
    x0, y0 = np.floor(sx).astype(int), np.floor(sy).astype(int)
    fx, fy = (sx - x0)[..., None], (sy - y0)[..., None]
    a = src[y0, x0] * (1 - fx) + src[y0, x0 + 1] * fx
    b = src[y0 + 1, x0] * (1 - fx) + src[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy


def felder(h, w, t, p):
    """Verschiebungsfeld für Phase t (0..1) mit Parametern p."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    s = math.sin(2 * math.pi * t)
    # Atmen: alles oberhalb der Hüfte hebt sich, nach oben hin voll
    atem = glatt((p["huefte_y"] - yy) / 250.0) * p["atem"] * (0.5 - 0.5 * math.cos(2 * math.pi * t))
    dy = -atem
    # Mantel und Haar: rechts von mantel_x, nach unten stärker, Welle läuft abwärts
    gewicht = glatt((xx - p["mantel_x"]) / 220.0) * glatt((yy - p["mantel_y"]) / 700.0)
    welle = np.sin(2 * math.pi * t - yy / 260.0)
    dx = gewicht * welle * p["wehen"]
    dy = dy + gewicht * np.cos(2 * math.pi * t - yy / 260.0) * p["wehen"] * p["auftrieb"]
    # Schweben: ganzer Körper
    dy = dy - p["schweben"] * (0.5 - 0.5 * math.cos(2 * math.pi * t))
    return dx, dy


def zu_sprite(bild, groesse, palette=None, farben=24):
    im = Image.fromarray(np.clip(bild, 0, 255).astype(np.uint8), "RGBA")
    klein = im.resize(groesse, Image.Resampling.BOX)
    alpha = klein.getchannel("A").point(lambda a: 255 if a > 110 else 0)
    rgb = klein.convert("RGB")
    if palette is None:
        palette = rgb.quantize(colors=farben, method=Image.Quantize.MEDIANCUT)
    q = rgb.quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
    q.putalpha(alpha)
    return q, palette


def animation(name, quelle, bilder, groesse, rand, p):
    src = lade(quelle)
    h, w, _ = src.shape
    # Rand oben/unten für Schweben und Auftrieb, damit nichts abgeschnitten wird
    pad = rand
    src = np.pad(src, ((pad, pad), (pad, pad), (0, 0)))
    for k in ("huefte_y", "mantel_y"):
        p[k] += pad
    p["mantel_x"] += pad
    h, w, _ = src.shape
    gross = (groesse[0], round(groesse[0] * h / w))
    sheet = Image.new("RGBA", (gross[0] * bilder, gross[1]))
    palette = None
    for i in range(bilder):
        dx, dy = felder(h, w, i / bilder, p)
        spr, palette = zu_sprite(verforme(src, dx, dy), gross, palette)
        sheet.paste(spr, (i * gross[0], 0))
    os.makedirs(OUT, exist_ok=True)
    sheet.save(os.path.join(OUT, name + ".png"))
    meta = {"name": name, "frame_w": gross[0], "frame_h": gross[1], "fps": 12, "quelle": quelle,
            "frames": [{"x": i * gross[0], "y": 0, "w": gross[0], "h": gross[1]} for i in range(bilder)]}
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    # Vorschau-GIF, vierfach vergrößert
    frames = []
    for i in range(bilder):
        fr = sheet.crop((i * gross[0], 0, (i + 1) * gross[0], gross[1]))
        bg = Image.new("RGBA", fr.size, (28, 24, 44, 255))
        bg.alpha_composite(fr)
        frames.append(bg.resize((fr.width * 4, fr.height * 4), Image.Resampling.NEAREST).convert("P"))
    frames[0].save(os.path.join(OUT, name + "_vorschau.gif"), save_all=True, append_images=frames[1:],
                   duration=1000 // 12, loop=0)
    return sheet


if __name__ == "__main__":
    # Koordinaten im Originalbild (1024 x 1536)
    animation("koenigin_p1_idle", "koenigin-idle-sense-helm-v5.webp", 6, (72, 108), 64,
              {"huefte_y": 1000, "atem": 14, "mantel_x": 560, "mantel_y": 650, "wehen": 18,
               "auftrieb": 0.25, "schweben": 0})
    animation("koenigin_p2_idle", "koenigin-p2-helmbruch-v1.webp", 10, (72, 108), 96,
              {"huefte_y": 1000, "atem": 10, "mantel_x": 520, "mantel_y": 450, "wehen": 34,
               "auftrieb": 0.6, "schweben": 48})
    animation("held_idle", "held-idle-hood-v3.webp", 6, (40, 60), 48,
              {"huefte_y": 760, "atem": 12, "mantel_x": 80, "mantel_y": 500, "wehen": 10,
               "auftrieb": 0.2, "schweben": 0})
