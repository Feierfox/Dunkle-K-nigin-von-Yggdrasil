"""Baut die Königin (Phase 1 mit Helm und Sense, Phase 2 mit gerissenem Helm).

Ergebnis:
    assets/3d/koenigin.blend, assets/3d/koenigin.glb
    assets/sprites/koenigin_*.png + .json

Vorlagen: assets/konzept/koenigin-idle-sense-helm-v5.webp,
          assets/konzept/koenigin-p2-helmbruch-v1.webp
"""

import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import common as C  # noqa: E402
from mathutils import Vector  # noqa: E402

# --- Palette (docs/VISUAL_KOENIGIN.md) -------------------------------------
SCHWARZ = "#070418"
RUESTUNG = "#292248"
RUESTUNG_HELL = "#514d81"
RUESTUNG_DUNKEL = "#1b1433"
MANTEL = "#5a10aa"
MANTEL_HELL = "#7914c7"
MANTEL_INNEN = "#300462"
HAAR = "#95abf8"
HAAR_HELL = "#dbd7ea"
AUGE = "#59c3c3"
MAGENTA = "#ee20fb"
KRISTALL = "#cc32f2"
GOLD = "#dbb176"
BLATT = "#c4bce2"
STREIFEN = "#6004c7"
LAUB = "#49bcbb"
BLUETE_MITTE = "#e16366"
# Phase 2
RISS = "#a8fff4"
AUGE_P2 = "#e8fffb"
VERDERBNIS_DUNKEL = "#3a0640"

BASE = [SCHWARZ, RUESTUNG, RUESTUNG_HELL, RUESTUNG_DUNKEL, MANTEL, MANTEL_HELL, MANTEL_INNEN,
        HAAR, HAAR_HELL, KRISTALL, GOLD, BLATT, STREIFEN, LAUB, BLUETE_MITTE, VERDERBNIS_DUNKEL]
GLOW = [AUGE, MAGENTA, RISS, AUGE_P2]

# Pixel pro Einheit: Krone und Kristalle passen in 96 px Höhe.
PPU = 35

# Drehung zur Kamera: Blick nach links, leicht dem Betrachter zugewandt.
DREHUNG = 35.0
# Richtung "quer zum Bild" im lokalen Raum (für Krone und Fächer).
QUER = Vector((math.cos(math.radians(DREHUNG)), -math.sin(math.radians(DREHUNG)), 0))
# Richtung zur Kamera im lokalen Raum (für Risse auf der sichtbaren Seite).
ZUR_KAMERA = Vector((-math.sin(math.radians(DREHUNG)), -math.cos(math.radians(DREHUNG)), 0))

KNOCHEN = [
    ("root", (0, 0, 0), (0, 0, 0.25), None),
    ("hips", (0, 0, 1.0), (0, 0, 1.22), "root"),
    ("spine", (0, 0, 1.22), (0, 0, 1.46), "hips"),
    ("chest", (0, 0, 1.46), (0, 0, 1.74), "spine"),
    ("neck", (0, 0, 1.74), (0, 0, 1.84), "chest"),
    ("head", (0, 0, 1.84), (0, 0, 2.1), "neck"),
    ("thigh_f", (0, -0.11, 1.0), (0, -0.11, 0.56), "hips"),
    ("shin_f", (0, -0.11, 0.56), (0, -0.11, 0.14), "thigh_f"),
    ("foot_f", (0, -0.11, 0.14), (-0.14, -0.11, 0.04), "shin_f"),
    ("thigh_b", (0, 0.11, 1.0), (0, 0.11, 0.56), "hips"),
    ("shin_b", (0, 0.11, 0.56), (0, 0.11, 0.14), "thigh_b"),
    ("foot_b", (0, 0.11, 0.14), (-0.14, 0.11, 0.04), "shin_b"),
    ("upper_f", (0, -0.25, 1.68), (-0.06, -0.27, 1.38), "chest"),
    ("fore_f", (-0.06, -0.27, 1.38), (-0.5, -0.24, 1.22), "upper_f"),
    ("hand_f", (-0.5, -0.24, 1.22), (-0.58, -0.24, 1.22), "fore_f"),
    ("upper_b", (0, 0.25, 1.68), (0.03, 0.27, 1.36), "chest"),
    ("fore_b", (0.03, 0.27, 1.36), (0.02, 0.28, 1.06), "upper_b"),
    ("hand_b", (0.02, 0.28, 1.06), (0.02, 0.28, 0.96), "fore_b"),
    ("sense", (-0.56, -0.22, 1.22), (-0.56, -0.22, 1.52), "hand_f"),
    ("cape1", (0.12, 0, 1.70), (0.20, 0, 1.30), "chest"),
    ("cape2", (0.20, 0, 1.30), (0.30, 0, 0.80), "cape1"),
    ("cape3", (0.30, 0, 0.80), (0.42, 0, 0.35), "cape2"),
    ("cape4", (0.42, 0, 0.35), (0.52, 0, 0.04), "cape3"),
    ("hair1", (0.08, 0, 2.0), (0.14, 0, 1.70), "head"),
    ("hair2", (0.14, 0, 1.70), (0.20, 0, 1.40), "hair1"),
    ("hair3", (0.20, 0, 1.40), (0.24, 0, 1.05), "hair2"),
]


def v(*a):
    return Vector(a)


def bein(b, s, y):
    """Bein mit Panzerung; s = '_f' oder '_b'."""
    b.cone((0, y, 1.0), (0, y, 0.56), 0.105, 0.08, RUESTUNG, "thigh" + s, seg=6)
    # Oberschenkelplatte mit Kristall (wie im Entwurf v5)
    b.box((-0.07, y, 0.78), (0.06, 0.15, 0.2), RUESTUNG_HELL, "thigh" + s, rot=(0, 0.15, 0))
    b.crystal((-0.105, y, 0.8), 0.022, KRISTALL, "thigh" + s)
    b.cone((0, y, 0.56), (0, y, 0.14), 0.075, 0.058, RUESTUNG_DUNKEL, "shin" + s, seg=6)
    b.box((-0.06, y, 0.56), (0.07, 0.12, 0.09), RUESTUNG_HELL, "shin" + s)  # Knie
    # Stiefel mit Absatz
    b.cone((0, y, 0.2), (0, y, 0.04), 0.07, 0.065, RUESTUNG, "foot" + s, seg=6)
    b.box((-0.1, y, 0.035), (0.16, 0.08, 0.07), RUESTUNG, "foot" + s)
    b.box((0.05, y, 0.03), (0.04, 0.05, 0.06), SCHWARZ, "foot" + s)
    b.box((-0.03, y, 0.2), (0.12, 0.13, 0.04), RUESTUNG_HELL, "foot" + s)  # Stulpe


def arm(b, s, schulter, ellbogen, hand):
    b.cone(schulter, ellbogen, 0.06, 0.052, RUESTUNG_DUNKEL, "upper" + s, seg=6)
    b.cone(ellbogen, hand, 0.07, 0.052, RUESTUNG, "fore" + s, seg=6)  # Armschiene
    b.ball(hand, 0.055, RUESTUNG, "hand" + s, scale=(1.1, 0.9, 1))


def schulter(b, s, y):
    b.ball((0.0, y, 1.69), 0.14, RUESTUNG_HELL, "chest", scale=(1.15, 0.95, 0.8), sub=1)
    # Dornen und kleine Äste aus der Schulterplatte
    sign = -1 if y < 0 else 1
    for dx, dz, dy, ln in ((0.06, 0.05, 0.04, 0.16), (-0.02, 0.07, 0.06, 0.13), (0.1, 0.0, 0.08, 0.11)):
        base = v(dx, y + sign * 0.02, 1.72)
        tip = base + v(dx * 0.6 + 0.04, sign * dy, dz + ln)
        b.cone(base, tip, 0.026, 0.004, SCHWARZ, "chest", seg=4)


def koerper(b):
    b.cone((0, 0, 0.92), (0, 0, 1.24), 0.19, 0.14, RUESTUNG, "hips", seg=8, scale=(1, 0.85))
    b.cone((0, 0, 1.22), (0, 0, 1.47), 0.13, 0.155, RUESTUNG_DUNKEL, "spine", seg=8, scale=(1, 0.85))
    b.cone((0, 0, 1.45), (0, 0, 1.76), 0.17, 0.15, RUESTUNG, "chest", seg=8, scale=(1, 0.82))
    # Brustplatte mit Mittelgrat und Kristall
    b.box((-0.13, 0, 1.6), (0.06, 0.2, 0.26), RUESTUNG_HELL, "chest", rot=(0, 0.12, 0))
    b.crystal((-0.17, -0.02, 1.62), 0.03, MAGENTA, "chest")
    # Gürtel-Kristall und Hüftplatten
    b.crystal((-0.17, -0.02, 1.13), 0.025, MAGENTA, "hips")
    b.box((-0.1, -0.1, 1.02), (0.08, 0.12, 0.16), RUESTUNG_HELL, "hips", rot=(0.2, 0.2, 0))
    b.cone((0, 0, 1.74), (0, 0, 1.86), 0.06, 0.055, SCHWARZ, "neck", seg=6)


def helm_und_krone(b):
    b.ball((0, 0, 1.96), 0.13, RUESTUNG_DUNKEL, "head", scale=(1.05, 0.88, 1.18), sub=2)
    # Visier: spitz nach vorn, mit Sehschlitz
    b.cone((-0.06, 0, 2.05), (-0.17, 0, 1.92), 0.07, 0.02, RUESTUNG, "head", seg=4, scale=(1, 0.8))
    b.box((-0.125, 0, 1.97), (0.03, 0.17, 0.025), SCHWARZ, "head")
    for y in (-0.045, 0.04):
        b.box((-0.14, y - 0.01, 1.97), (0.03, 0.05, 0.03), AUGE, "head", glow=True)
    # Krone: fünf Äste, die mittlere am höchsten, quer zum Bild aufgefächert
    for i, (q, hoehe, neig) in enumerate(((-2, 0.26, -0.7), (-1, 0.36, -0.35), (0, 0.46, 0), (1, 0.36, 0.35), (2, 0.26, 0.7))):
        base = v(0.0, 0, 2.06) + QUER * (q * 0.04)
        mitte = base + QUER * (neig * 0.12) + v(0, 0, hoehe * 0.55)
        spitze = base + QUER * (neig * 0.24) + v(0.01, 0, hoehe)
        b.tube([base, mitte, spitze], [0.034, 0.026, 0.016], [0.034, 0.026, 0.016], SCHWARZ, "head", seg=5)
        b.crystal(spitze + v(0, 0, 0.03), 0.026, MAGENTA, "head")
        if abs(q) == 1:  # kleine Seitenzweige
            ast = mitte + QUER * (q * 0.07) + v(0, 0, 0.06)
            b.tube([mitte, ast], 0.012, 0.012, SCHWARZ, "head", seg=4)


def haar(b):
    gew = C.chain_weights(["hair1", "hair2", "hair3"], 2.05, 1.0)
    straehnen = [
        (HAAR, -0.06, [(0.08, 2.05), (0.2, 1.86), (0.22, 1.62), (0.3, 1.38), (0.28, 1.14), (0.36, 0.92)]),
        (HAAR, -0.16, [(0.1, 2.0), (0.22, 1.8), (0.3, 1.56), (0.36, 1.3), (0.44, 1.08)]),
        (HAAR_HELL, -0.2, [(0.06, 1.98), (0.14, 1.78), (0.14, 1.56), (0.2, 1.34), (0.18, 1.16)]),
        (HAAR, 0.06, [(0.1, 2.02), (0.24, 1.82), (0.32, 1.5), (0.4, 1.2)]),
    ]
    for farbe, y, pts in straehnen:
        punkte = [v(x, y, z) for x, z in pts]
        n = len(punkte)
        breite = [0.085 * (1 - 0.6 * i / (n - 1)) for i in range(n)]
        b.tube(punkte, breite, [0.025] * n, farbe, "hair1", hint=(0, 1, 0), seg=5, weight_fn=gew)


def mantel(b):
    gew = C.chain_weights(["cape1", "cape2", "cape3", "cape4"], 1.72, 0.04)
    pfad = [v(0.1, 0.08, 1.72), v(0.2, 0.1, 1.4), v(0.32, 0.12, 0.95), v(0.46, 0.14, 0.5), v(0.64, 0.16, 0.06)]
    b.tube(pfad, [0.2, 0.26, 0.32, 0.38, 0.44], 0.035, MANTEL, "cape1", hint=(0, 1, 0), seg=6, weight_fn=gew)
    b.tube([p + v(-0.03, 0, 0) for p in pfad[:4]], [0.2, 0.25, 0.3, 0.35], 0.03, MANTEL_INNEN, "cape1",
           hint=(0, 1, 0), seg=6, weight_fn=gew)
    # ausgefranster Saum
    for i, y in enumerate((-0.24, -0.06, 0.14, 0.32, 0.5)):
        base = v(0.6 + 0.02 * i, y, 0.12)
        b.cone(base, base + v(0.06, 0, -0.14 - 0.03 * (i % 2)), 0.06, 0.005, MANTEL_HELL, "cape4", seg=4,
               weight_fn=lambda co: {"cape4": 1.0})


def blumen(b):
    for pos, bone in (((-0.05, -0.26, 1.78), "chest"), ((-0.15, -0.08, 1.3), "spine"), ((0.08, -0.2, 0.9), "hips")):
        p = v(*pos)
        b.ball(p, 0.035, KRISTALL, bone, scale=(1, 1, 0.6), sub=1)
        b.ball(p + v(-0.02, -0.02, 0.0), 0.014, BLUETE_MITTE, bone, sub=1)
        b.box(p + v(0.03, 0.0, -0.05), (0.03, 0.03, 0.05), LAUB, bone, rot=(0.4, 0, 0))


def sense(b):
    x, y = -0.56, -0.22
    stiel = [v(x + 0.012 * math.sin(i * 1.7), y, 0.12 + i * 0.22) for i in range(10)]
    stiel.append(v(x, y, 2.3))
    b.tube(stiel, 0.03, 0.03, RUESTUNG_DUNKEL, "sense", seg=6)
    for z in (0.55, 1.62):
        b.cone((x, y, z), (x, y, z + 0.06), 0.042, 0.042, GOLD, "sense", seg=6)
    b.crystal((x, y, 0.07), 0.04, KRISTALL, "sense", glow=False)
    # Astgabel und großer Kristall am Blattansatz
    for dx in (-0.08, 0.08):
        b.tube([v(x, y, 2.24), v(x + dx, y, 2.36), v(x + dx * 1.3, y, 2.42)], [0.022, 0.016, 0.008],
               [0.022, 0.016, 0.008], RUESTUNG_DUNKEL, "sense", seg=4)
    b.crystal((x, y - 0.03, 2.33), 0.06, MAGENTA, "sense")
    # Sensenblatt: Bogen nach vorn (-X), Spitze abwärts
    zentrum = v(x - 0.28, y, 2.08)
    r = 0.36
    a0, a1 = math.radians(37), math.radians(205)
    n = 12
    punkte, breite, innen = [], [], []
    for i in range(n + 1):
        t = i / n
        a = a0 + (a1 - a0) * t
        p = zentrum + v(math.cos(a) * r, 0, math.sin(a) * r)
        punkte.append(p)
        breite.append(0.085 * (1 - t) + 0.012)
        innen.append(zentrum + (p - zentrum) * (1 - (0.085 * (1 - t)) / r))
    b.tube(punkte, 0.014, breite, BLATT, "sense", hint=(0, 1, 0), seg=4)
    b.tube(innen[:-2], 0.02, [w * 0.35 for w in breite[:-2]], STREIFEN, "sense", hint=(0, 1, 0), seg=4)


def phase2_zusatz(b):
    """Gerissener Helm, verdorbene Wurzeln, leuchtende Risse, Wurzeln um Arm und Stiel."""
    k = ZUR_KAMERA

    def zickzack(start, schritte, farbe, bone, dicke=0.016):
        p = v(*start)
        for dx, dz in schritte:
            q = p + v(dx, 0, dz)
            b.tube([p, q], dicke, dicke, farbe, bone, seg=4, glow=True)
            p = q

    # Helmrisse (magenta) auf der Kameraseite
    hz = v(0, 0, 1.96) + k * 0.12
    zickzack(hz + v(-0.02, 0, 0.12), [(0.03, -0.06), (-0.02, -0.06), (0.03, -0.07)], MAGENTA, "head")
    zickzack(hz + v(0.05, 0.02, 0.1), [(0.02, -0.05), (0.04, -0.04)], MAGENTA, "head")
    # Wurzeln aus dem Helm
    for start, mitte, ende in (((0.06, -0.06, 2.06), (0.18, -0.12, 2.12), (0.22, -0.2, 2.02)),
                               ((0.1, 0.05, 2.0), (0.24, 0.08, 2.04), (0.3, 0.02, 1.9)),
                               ((-0.02, -0.08, 2.08), (-0.1, -0.16, 2.2), (-0.16, -0.14, 2.28))):
        b.tube([v(*start), v(*mitte), v(*ende)], [0.022, 0.016, 0.006], [0.022, 0.016, 0.006],
               VERDERBNIS_DUNKEL, "head", seg=4)
        b.tube([v(*start) + k * 0.012, v(*mitte) + k * 0.012], 0.008, 0.008, MAGENTA, "head", seg=4, glow=True)
    # hellere Augen
    for y in (-0.045, 0.04):
        b.box((-0.146, y - 0.01, 1.97), (0.03, 0.054, 0.034), AUGE_P2, "head", glow=True)
    # Türkise Risse auf Brust, Hüfte und Beinen (Kameraseite)
    for bone, mitte, r in (("chest", (0, 0, 1.6), 0.15), ("hips", (0, 0, 1.08), 0.17),
                           ("thigh_f", (0, -0.11, 0.8), 0.1), ("shin_f", (0, -0.11, 0.36), 0.07),
                           ("thigh_b", (0, 0.11, 0.78), 0.1)):
        s = v(*mitte) + k * r
        zickzack(s + v(-0.02, 0, 0.08), [(0.03, -0.05), (-0.03, -0.05), (0.02, -0.06)], RISS, bone, 0.013)
    # Wurzeln um Unterarm und Stiel (Spirale)
    x, y = -0.56, -0.22
    spirale = [v(x + 0.045 * math.cos(t), y + 0.045 * math.sin(t), 0.85 + t * 0.06) for t in [i * 0.7 for i in range(12)]]
    b.tube(spirale, 0.016, 0.016, VERDERBNIS_DUNKEL, "sense", seg=4)
    b.tube(spirale[2:8], 0.006, 0.006, MAGENTA, "sense", seg=3, glow=True)
    arm_spirale = [v(-0.5 + 0.42 * (i / 8), -0.24 + 0.06 * math.cos(i * 1.4), 1.2 + 0.15 * (i / 8) + 0.05 * math.sin(i * 1.4))
                   for i in range(9)]
    b.tube(arm_spirale, 0.014, 0.014, VERDERBNIS_DUNKEL, "fore_f", seg=4)


def baue():
    scene = C.reset_scene()
    palette = BASE + GLOW
    img = C.make_palette_image("Koenigin_Palette", palette)
    mats = C.make_materials(img)

    b1 = C.Builder(palette)
    for s, y in (("_b", 0.11), ("_f", -0.11)):
        bein(b1, s, y)
    koerper(b1)
    schulter(b1, "_b", 0.25)
    schulter(b1, "_f", -0.25)
    arm(b1, "_b", (0, 0.25, 1.68), (0.03, 0.27, 1.36), (0.02, 0.28, 1.04))
    arm(b1, "_f", (0, -0.25, 1.68), (-0.06, -0.27, 1.38), (-0.52, -0.23, 1.22))
    helm_und_krone(b1)
    haar(b1)
    mantel(b1)
    blumen(b1)
    sense(b1)
    koerper_obj = b1.to_object("Koenigin", img, mats)

    b2 = C.Builder(palette)
    phase2_zusatz(b2)
    p2_obj = b2.to_object("Koenigin_P2_Zusatz", img, mats)

    rig = C.make_armature("Koenigin_Skelett", KNOCHEN, DREHUNG)
    C.skin(koerper_obj, rig)
    C.skin(p2_obj, rig)
    return scene, rig, koerper_obj, p2_obj, palette


def animationen(rig):
    A = {}
    # --- p1_idle: 6 Bilder, ruhiger Atem, Mantel und Haar bewegen sich leicht
    A["p1_idle"] = C.build_action(rig, "p1_idle", 6, [
        (1, {"chest": 0, "cape2": 2, "cape3": 2, "hair2": 0, "upper_b": 3}, {"root": (0, 0, 0)}),
        (4, {"chest": 2, "neck": -1, "cape1": 2, "cape2": 5, "cape3": 6, "cape4": 4, "hair2": 4, "hair3": 4,
             "upper_b": 5, "upper_f": 2}, {"root": (0, -0.012, 0)}),
    ])
    # --- p1_walk: 8 Bilder, schwerer Schritt auf der Stelle
    stand = {"chest": 4, "upper_f": -4}

    def schritt(f_vor, gegen):
        # f_vor: vorderes Bein vorn (True) oder hinten
        s = 1 if f_vor else -1
        p = dict(stand)
        p.update({"thigh_f": -24 * s, "shin_f": 12 if f_vor else 22, "foot_f": -6 * s,
                  "thigh_b": 24 * s, "shin_b": 22 if f_vor else 12, "foot_b": 6 * s,
                  "upper_b": -14 * s, "fore_b": -6, "cape1": 6, "cape2": 9 + 3 * gegen, "cape3": 12, "cape4": 10,
                  "hair2": 6, "hair3": 8, "hips": 3 * s})
        return p

    def durchgang(f_traeger):
        p = dict(stand)
        p.update({"thigh_f": 0 if f_traeger else -12, "shin_f": 4 if f_traeger else 38,
                  "thigh_b": -12 if f_traeger else 0, "shin_b": 38 if f_traeger else 4,
                  "cape1": 4, "cape2": 6, "cape3": 8, "cape4": 6, "hair2": 3, "hair3": 4})
        return p
    A["p1_walk"] = C.build_action(rig, "p1_walk", 8, [
        (1, schritt(True, 0), {"root": (0, -0.03, 0)}),
        (3, durchgang(False), {"root": (0, 0.012, 0)}),
        (5, schritt(False, 1), {"root": (0, -0.03, 0)}),
        (7, durchgang(True), {"root": (0, 0.012, 0)}),
    ])
    # --- p1_atk_richtschlag: 10 Bilder, Sense über den Kopf, Schlag vor ihr in den Boden
    # Die Sense hängt an der Hand. Ihr Weltwinkel W ergibt sich aus Oberarm,
    # Unterarm und eigenem Winkel: sense = W - (upper_f + fore_f).
    def schlagpose(upper, fore, welt, extra, root):
        p = {"upper_f": upper, "fore_f": fore, "sense": welt - (upper + fore)}
        p.update(extra)
        return p, {"root": (0, root, 0)}
    ausholen = {"chest": -10, "spine": -4, "neck": -4, "upper_b": -30, "fore_b": -20, "thigh_b": 8,
                "cape1": 4, "cape2": 6, "cape3": 4, "hair2": 6}
    schlag = {"chest": 18, "spine": 8, "neck": 6, "thigh_f": -22, "shin_f": 18, "thigh_b": 16, "shin_b": 10,
              "upper_b": 25, "fore_b": 10, "cape1": 10, "cape2": 14, "cape3": 16, "cape4": 12, "hair2": 12, "hair3": 14}
    keys = []
    for f, (upper, fore, welt, extra, root) in (
            (1, (0, 0, 0, {"cape2": 2, "cape3": 2}, 0)),
            (3, (-140, 15, -70, ausholen, 0.01)),
            (5, (-150, 20, -80, ausholen, 0.015)),
            (6, (-70, -10, 95, schlag, -0.05)),
            (7, (-66, -10, 100, dict(schlag, chest=20), -0.055)),
            (9, (-30, 0, 40, dict(schlag, chest=10, cape2=8, cape3=8), -0.02)),
            (10, (-8, 0, 8, {"chest": 4}, 0))):
        p, l = schlagpose(upper, fore, welt, extra, root)
        keys.append((f, p, l))
    A["p1_atk_richtschlag"] = C.build_action(rig, "p1_atk_richtschlag", 10, keys, cyclic=False)
    # --- p2_idle: 10 Bilder, schwebt, Mantel weht nach oben und hinten
    def schweben(h, welle):
        pose = {"thigh_f": -6, "shin_f": 14, "foot_f": 28, "thigh_b": 4, "shin_b": 18, "foot_b": 30,
                "cape1": 14 + welle, "cape2": 22 + welle, "cape3": 26 + 2 * welle, "cape4": 22 + 2 * welle,
                "hair1": 6, "hair2": 14 + welle, "hair3": 18 + welle, "upper_b": 10, "fore_b": 12, "chest": -2}
        return pose, {"root": (0, h, 0)}
    keys = []
    for f, h, w in ((1, 0.125, 0), (4, 0.2, 4), (6, 0.2, 6), (9, 0.125, 2)):
        p, l = schweben(h, w)
        keys.append((f, p, l))
    A["p2_idle"] = C.build_action(rig, "p2_idle", 10, keys)
    return A


def main():
    scene, rig, koerper_obj, p2_obj, palette = baue()
    A = animationen(rig)
    pal_p1 = C.shaded_palette(BASE, [AUGE, MAGENTA])
    pal_p2 = C.shaded_palette(BASE, GLOW)
    tmp = tempfile.mkdtemp(prefix="koenigin_")
    plan = [
        ("p1_idle", False, (64, 96), 2, 41),
        ("p1_walk", False, (64, 96), 2, 41),
        ("p1_atk_richtschlag", False, (128, 128), 2, 76),
        ("p2_idle", True, (64, 96), 2, 41),
    ]
    only = os.environ.get("NUR")
    for name, p2, canvas, foot, cx in plan:
        if only and name not in only.split(","):
            continue
        p2_obj.hide_render = not p2
        C.render_action(scene, rig, koerper_obj, A[name], canvas, foot, pal_p2 if p2 else pal_p1,
                        "koenigin_" + name, tmp, center_x_px=cx, ppu=PPU)
    p2_obj.hide_render = False
    rig.animation_data.action = A["p1_idle"]
    scene.frame_set(1)
    C.export_files("koenigin", [rig, koerper_obj, p2_obj])

if __name__ == "__main__":
    main()
