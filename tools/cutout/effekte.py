"""Effekte in nativer PSP-Auflösung und Vorschau-Szenen im Thronsaal.

Effekte (assets/sprites/effekte/):
    fx_impuls1_ring   10 Bilder  Ringwelle über den Boden (Wechsel zu Phase 2), 480 x 48
    fx_nebel_kachel    1 Bild    kachelbare Nebeltextur 64 x 64 (Wechsel zu Phase 3)
    fx_feuer_eisblau   8 Bilder  eisblaues Feuer des Totenrituals, 40 x 48
    fx_portal         12 Bilder  lila Portal am Boden: öffnen, kreisen, schließen, 64 x 24

Vorschau-Szenen (GIF, zweifach vergrößert):
    szene_impuls1_sprung, szene_impuls2_amulett, szene_ritual_feuer, szene_ritual_portal

    python tools/cutout/effekte.py
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import angriffe as A  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FX = os.path.join(REPO, "assets", "sprites", "effekte")
CUT = os.path.join(REPO, "assets", "sprites", "cutout")
PSP = os.path.join(REPO, "assets", "konzept", "psp")
W, H = 480, 272
BODEN = 240

EIS = [(0, 0, 0, 0), (20, 40, 70, 255), (42, 143, 154, 255), (89, 195, 195, 255), (168, 255, 244, 255), (232, 255, 251, 255)]
LILA = [(58, 6, 64), (96, 16, 140), (122, 24, 190), (204, 50, 242), (238, 32, 251), (240, 200, 255)]


def streifen(bilder):
    w, h = bilder[0].size
    s = Image.new("RGBA", (w * len(bilder), h))
    for i, b in enumerate(bilder):
        s.paste(b, (i * w, 0))
    return s


def speichere_fx(name, bilder):
    os.makedirs(FX, exist_ok=True)
    streifen(bilder).save(os.path.join(FX, name + ".png"))


def gif(name, bilder, dauer=83, faktor=2):
    frames = [b.convert("RGB").resize((b.width * faktor, b.height * faktor), Image.Resampling.NEAREST) for b in bilder]
    frames[0].save(os.path.join(PSP, name + ".gif"), save_all=True, append_images=frames[1:], duration=dauer, loop=0)


# --- Effekte -------------------------------------------------------------------

def impuls1_ring(n=10, w=480, h=48, cx=240):
    bilder = []
    for i in range(n):
        t = (i + 1) / n
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        rx = 10 + t * (w / 2 + 20)
        ry = max(3, rx * 0.11)
        cy = h - 10
        for dicke, farbe in ((5, EIS[2]), (3, EIS[4]), (1, EIS[5])):
            a = int(255 * (1 - t * 0.6))
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(*farbe[:3], a), width=dicke)
        # Funken auf der Welle
        rnd = random.Random(i)
        for _ in range(int(12 * (1 - t) + 4)):
            ang = rnd.uniform(0, 2 * math.pi)
            x, y = cx + math.cos(ang) * rx, cy + math.sin(ang) * ry - rnd.randint(1, 6)
            d.point((x, y), fill=EIS[5])
        bilder.append(b)
    return bilder


def nebel_kachel(g=64):
    """Kachelbare Nebeltextur aus überlagerten Sinuswellen, in 2x2-Blöcken."""
    b = Image.new("RGBA", (g, g))
    px = b.load()
    for y in range(0, g, 2):
        for x in range(0, g, 2):
            u, v = 2 * math.pi * x / g, 2 * math.pi * y / g
            n = 0.5 + 0.2 * math.sin(u + 2 * v) + 0.15 * math.sin(3 * u - v) + 0.15 * math.cos(2 * u + 3 * v)
            n = min(1, max(0, n))
            c = (round(100 + 40 * n), round(18 + 14 * n), round(160 + 40 * n), round(110 + 80 * n))
            for dy in (0, 1):
                for dx in (0, 1):
                    px[x + dx, y + dy] = c
    return b


def feuer(n=8, w=40, h=48):
    """Eisblaues Feuer nach dem klassischen Glut-Verfahren, deterministisch."""
    rnd = random.Random(3)
    glut = np.zeros((h, w), np.int32)
    glut[-1, 6:w - 6] = len(EIS) * 6 - 1
    bilder = []
    for schritt in range(n + 12):
        for x in range(w):
            for y in range(1, h):
                src = glut[y, x]
                r = rnd.randint(0, 3)
                nx = min(w - 1, max(0, x - r + 1))
                glut[y - 1, nx] = max(0, src - (r & 1) * 2)
        if schritt >= 12:
            b = Image.new("RGBA", (w, h))
            px = b.load()
            for y in range(h):
                for x in range(w):
                    k = glut[y, x] // 6
                    if k > 0:
                        px[x, y] = EIS[min(k, len(EIS) - 1)]
            bilder.append(b)
    return bilder


def portal(n=12, w=64, h=24):
    bilder = []
    for i in range(n):
        if i < 4:
            s = (i + 1) / 4
        elif i < 8:
            s = 1.0
        else:
            s = 1 - (i - 7) / 5
        b = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(b)
        cx, cy = w / 2, h / 2
        rx, ry = (w / 2 - 2) * s, (h / 2 - 2) * s
        if rx < 1:
            bilder.append(b)
            continue
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(*LILA[0], 255))
        d.ellipse((cx - rx * 0.8, cy - ry * 0.75, cx + rx * 0.8, cy + ry * 0.75), fill=(10, 2, 14, 255))
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(*LILA[3], 255), width=2)
        # kreisende Punkte
        for k in range(10):
            ang = k / 10 * 2 * math.pi + i * 0.6
            x, y = cx + math.cos(ang) * rx * 0.7, cy + math.sin(ang) * ry * 0.6
            d.point((x, y), fill=(*LILA[4], 255))
        bilder.append(b)
    return bilder


# --- Vorschau-Szenen -------------------------------------------------------------

def saal(datei="thronsaal-p2.png"):
    if datei == "p1":
        im = Image.open(os.path.join(REPO, "assets", "konzept", "thronsaal-pixel-v2.webp")).convert("RGB")
        return im.resize((W, H), Image.Resampling.BOX).quantize(colors=48).convert("RGBA")
    return Image.open(os.path.join(PSP, datei)).convert("RGBA")


def sprite_bild(name, i):
    s = Image.open(os.path.join(CUT, name + ".png")).convert("RGBA")
    import json
    meta = json.load(open(os.path.join(CUT, name + ".json"), encoding="utf-8"))
    fw = meta["frame_w"]
    n = s.width // fw
    return s.crop(((i % n) * fw, 0, (i % n) * fw + fw, s.height))


def setze_anim(bild, name, i, x_mitte, fuss_y):
    """Bild i einer Animation setzen, ausgerichtet wie Bild 0 (Sprung- und Schwebehöhe bleiben erhalten)."""
    erstes = sprite_bild(name, 0)
    unten = erstes.getbbox()[3]
    spr = sprite_bild(name, i)
    bild.alpha_composite(spr, (round(x_mitte - spr.width / 2), round(fuss_y - unten)))


def setze(bild, spr, x_mitte, fuss_y):
    """Sprite so setzen, dass seine unterste deckende Zeile auf fuss_y liegt."""
    bb = spr.getbbox()
    if not bb:
        return
    bild.alpha_composite(spr, (round(x_mitte - spr.width / 2), round(fuss_y - bb[3])))


def szene_impuls1(ring):
    bilder = []
    for i in range(10):
        b = saal("p1")
        setze_anim(b, "koenigin_p2_idle", i, 300, BODEN)
        # Held springt, wenn die Welle ihn erreicht
        j = max(0, min(7, i - 2))
        setze_anim(b, "held_sprung", j, 170, BODEN)
        r = ring[i]
        b.alpha_composite(r, (300 - 240, BODEN - r.height + 10))
        bilder.append(b)
    gif("szene_impuls1_sprung", bilder, 120)


def szene_impuls2(kachel):
    bilder = []
    for i in range(12):
        b = saal()
        setze_anim(b, "koenigin_p2_idle", i, 300, BODEN)
        t = min(1, i / 5)  # Nebel rollt von der Königin heran
        if t > 0.3:
            # goldener Schein um den Helden, solange der Schild steht
            held = sprite_bild("held_idle", i)
            schein = Image.new("RGBA", held.size)
            schein.paste((246, 217, 126, 255), (0, 0), held.getchannel("A"))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                tmp = Image.new("RGBA", b.size)
                setze_anim(tmp, "held_idle", 0, 170 + dx, BODEN + dy)
                gold = Image.new("RGBA", b.size, (246, 217, 126, 255))
                gold.putalpha(tmp.getchannel("A"))
                b.alpha_composite(gold)
        setze_anim(b, "held_idle", i, 170, BODEN)
        nebel = Image.new("RGBA", (W, H))
        for ty in range(0, H, 64):
            for tx in range(0, W, 64):
                nebel.alpha_composite(kachel, ((tx + i * 3) % (W + 64) - 64 + 0, ty))
        maske = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(maske)
        md.ellipse((300 - 600 * t, 136 - 400 * t, 300 + 600 * t, 136 + 400 * t), fill=255)
        md.ellipse((170 - 30, BODEN - 64, 170 + 30, BODEN + 8), fill=0)
        nebel.putalpha(Image.composite(nebel.getchannel("A"), Image.new("L", (W, H), 0), maske))
        b.alpha_composite(nebel)
        if t > 0.3:
            sd = ImageDraw.Draw(b)
            sd.ellipse((140, BODEN - 64, 200, BODEN + 8), outline=(246, 217, 126, 255), width=2)
        bilder.append(b)
    gif("szene_impuls2_amulett", bilder, 120)


def szene_feuer(flammen):
    bilder = []
    tod = sprite_bild("held_tod", 7)
    for i in range(16):
        b = saal()
        setze(b, tod, 175, BODEN)
        if i >= 3:
            f = flammen[(i - 3) % len(flammen)]
            setze(b, f, 175, BODEN + 2)
        setze_anim(b, "koenigin_p1_idle", i, 235, BODEN)
        bilder.append(b)
    gif("szene_ritual_feuer", bilder, 120)


def szene_portal(tor):
    bilder = []
    tod = sprite_bild("held_tod", 7)
    for i in range(12):
        b = saal()
        setze_anim(b, "koenigin_p2_idle", i, 245, BODEN)
        p = tor[i]
        b.alpha_composite(p, (175 - p.width // 2, BODEN - p.height // 2 - 2))
        # Körper sinkt ab Bild 4 ins Portal und wird dabei abgeschnitten
        sink = max(0, i - 3) * 3
        if sink < 20:
            koerper = tod.crop((0, 0, tod.width, max(1, tod.getbbox()[3] - sink)))
            setze(b, koerper, 175, BODEN)
        bilder.append(b)
    gif("szene_ritual_portal", bilder, 120)


def main():
    ring = impuls1_ring()
    speichere_fx("fx_impuls1_ring", ring)
    kachel = nebel_kachel()
    os.makedirs(FX, exist_ok=True)
    kachel.save(os.path.join(FX, "fx_nebel_kachel.png"))
    flammen = feuer()
    speichere_fx("fx_feuer_eisblau", flammen)
    tor = portal()
    speichere_fx("fx_portal", tor)
    szene_impuls1(ring)
    szene_impuls2(kachel)
    szene_feuer(flammen)
    szene_portal(tor)


if __name__ == "__main__":
    main()
