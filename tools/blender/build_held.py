"""Baut den Held mit Kapuzenumhang und Schwert.

Ergebnis:
    assets/3d/held.blend, assets/3d/held.glb, assets/3d/held_palette.png
    assets/sprites/held_*.png + .json

Vorlage: assets/konzept/held-idle-hood-v3.webp
"""

import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import common as C  # noqa: E402
from mathutils import Vector  # noqa: E402

# --- Palette (aus held-idle-hood-v3) ----------------------------------------
UMHANG = "#265338"
UMHANG_DUNKEL = "#133125"
UMHANG_SAUM = "#6f8a45"
SCHATTEN = "#050608"
ELFENBEIN = "#ddd5c6"
STAHL = "#9aa2b8"
STAHL_DUNKEL = "#4b5168"
LEDER = "#74422b"
LEDER_DUNKEL = "#4e2c1f"
STIEFEL = "#9a5a32"
HOSE = "#4a402e"
KLINGE = "#d3d0d2"

BASE = [UMHANG, UMHANG_DUNKEL, UMHANG_SAUM, SCHATTEN, ELFENBEIN, STAHL, STAHL_DUNKEL,
        LEDER, LEDER_DUNKEL, STIEFEL, HOSE, KLINGE]

PPU = 40
# Blick nach rechts, leicht dem Betrachter zugewandt (lokal blickt die Figur nach -X).
DREHUNG = 145.0

KNOCHEN = [
    ("root", (0, 0, 0), (0, 0, 0.12), None),
    ("hips", (0, 0, 0.46), (0, 0, 0.58), "root"),
    ("spine", (0, 0, 0.58), (0, 0, 0.7), "hips"),
    ("chest", (0, 0, 0.7), (0, 0, 0.84), "spine"),
    ("head", (0, 0, 0.84), (0, 0, 1.05), "chest"),
    ("thigh_f", (0, -0.06, 0.46), (0, -0.06, 0.27), "hips"),
    ("shin_f", (0, -0.06, 0.27), (0, -0.06, 0.07), "thigh_f"),
    ("foot_f", (0, -0.06, 0.07), (-0.08, -0.06, 0.02), "shin_f"),
    ("thigh_b", (0, 0.06, 0.46), (0, 0.06, 0.27), "hips"),
    ("shin_b", (0, 0.06, 0.27), (0, 0.06, 0.07), "thigh_b"),
    ("foot_b", (0, 0.06, 0.07), (-0.08, 0.06, 0.02), "shin_b"),
    ("upper_f", (0, -0.13, 0.8), (-0.02, -0.14, 0.64), "chest"),
    ("fore_f", (-0.02, -0.14, 0.64), (-0.13, -0.15, 0.55), "upper_f"),
    ("hand_f", (-0.13, -0.15, 0.55), (-0.17, -0.15, 0.55), "fore_f"),
    ("upper_b", (0, 0.13, 0.8), (0.02, 0.14, 0.64), "chest"),
    ("fore_b", (0.02, 0.14, 0.64), (0.01, 0.15, 0.5), "upper_b"),
    ("hand_b", (0.01, 0.15, 0.5), (0.01, 0.15, 0.46), "fore_b"),
    ("schwert", (-0.15, -0.16, 0.54), (-0.25, -0.16, 0.48), "hand_f"),
    ("cape1", (0.07, 0, 0.84), (0.1, 0, 0.6), "chest"),
    ("cape2", (0.1, 0, 0.6), (0.14, 0, 0.36), "cape1"),
    ("cape3", (0.14, 0, 0.36), (0.18, 0, 0.14), "cape2"),
]


def v(*a):
    return Vector(a)


def bein(b, s, y):
    b.cone((0, y, 0.47), (0, y, 0.27), 0.05, 0.042, HOSE, "thigh" + s, seg=6)
    b.cone((0, y, 0.3), (0, y, 0.05), 0.05, 0.046, STIEFEL, "shin" + s, seg=6)
    b.cone((0, y, 0.31), (0, y, 0.27), 0.056, 0.056, LEDER_DUNKEL, "shin" + s, seg=6)  # Stulpe
    b.box((-0.04, y, 0.03), (0.12, 0.07, 0.06), STIEFEL, "foot" + s)


def arm(b, s, schulter, ellbogen, hand):
    b.cone(schulter, ellbogen, 0.042, 0.038, ELFENBEIN, "upper" + s, seg=6)
    b.cone(ellbogen, hand, 0.044, 0.036, STAHL, "fore" + s, seg=6)
    b.ball(hand, 0.035, LEDER, "hand" + s, scale=(1.1, 1, 1))


def koerper(b):
    b.cone((0, 0, 0.42), (0, 0, 0.84), 0.11, 0.1, UMHANG, "spine", seg=8, scale=(1, 0.85),
           weight_fn=lambda co: {"hips": 1.0} if co.z < 0.58 else {"chest": 1.0})
    b.cone((0, 0, 0.5), (0, 0, 0.55), 0.112, 0.112, LEDER, "hips", seg=8, scale=(1, 0.87))
    b.box((-0.1, -0.02, 0.525), (0.03, 0.05, 0.04), STAHL, "hips")
    # Riemen schräg über die Brust
    b.box((-0.07, -0.02, 0.7), (0.03, 0.2, 0.035), LEDER_DUNKEL, "chest", rot=(0.9, 0, 0))
    b.box((-0.088, -0.03, 0.72), (0.02, 0.035, 0.035), STAHL, "chest")


def kapuze_und_umhang(b):
    # Schulterumhang
    b.cone((0.01, 0, 0.66), (0.0, 0, 0.88), 0.17, 0.08, UMHANG, "chest", seg=8, scale=(1, 0.95))
    # Kapuze mit Spitze nach hinten
    b.ball((0.015, 0, 0.95), 0.1, UMHANG, "head", scale=(1.15, 1.0, 1.12), sub=2)
    b.cone((0.05, 0, 1.0), (0.14, 0, 1.08), 0.06, 0.01, UMHANG, "head", seg=5)
    b.tube([v(-0.08, -0.07, 1.04), v(-0.1, 0, 1.06), v(-0.08, 0.07, 1.04)], 0.018, 0.018, UMHANG_SAUM, "head", seg=4)
    # Gesichtsöffnung: vollständig im Schatten
    b.ball((-0.07, 0, 0.93), 0.068, SCHATTEN, "head", scale=(0.55, 0.95, 1.1), sub=1)
    # Langer Umhang hinten
    gew = C.chain_weights(["cape1", "cape2", "cape3"], 0.86, 0.14)
    pfad = [v(0.07, 0.0, 0.86), v(0.11, 0.0, 0.62), v(0.15, 0.0, 0.38), v(0.2, 0.0, 0.16)]
    b.tube(pfad, [0.16, 0.19, 0.22, 0.25], 0.03, UMHANG, "cape1", hint=(0, 1, 0), seg=6, weight_fn=gew)
    b.tube([p + v(0.0, 0, -0.005) for p in pfad[2:]], [0.225, 0.255], 0.034, UMHANG_SAUM, "cape3",
           hint=(0, 1, 0), seg=6, weight_fn=lambda co: {"cape3": 1.0})
    # Vordere Umhangbahn auf der Kameraseite
    vorn = [v(-0.02, -0.14, 0.82), v(-0.03, -0.16, 0.6), v(-0.02, -0.17, 0.36), v(0.0, -0.17, 0.2)]
    b.tube(vorn, [0.06, 0.07, 0.08, 0.09], 0.02, UMHANG_DUNKEL, "chest", hint=(1, 0, 0), seg=5,
           weight_fn=lambda co: {"chest": 1.0} if co.z > 0.58 else {"hips": 1.0})


def schwert(b):
    hand = v(-0.15, -0.16, 0.54)
    richtung = v(-0.39, 0, -0.22).normalized()
    b.tube([hand - richtung * 0.07, hand + richtung * 0.03], 0.016, 0.016, LEDER_DUNKEL, "schwert", seg=5)
    b.ball(hand - richtung * 0.08, 0.022, STAHL, "schwert", sub=1)
    quer = v(0, 0, 1).cross(richtung).normalized()
    parier = hand + richtung * 0.04
    oben = v(-richtung.z, 0, richtung.x)  # senkrecht zur Klinge in der Bildebene
    b.tube([parier - oben * 0.06, parier + oben * 0.06], 0.016, 0.016, STAHL, "schwert", seg=4)
    spitze = hand + richtung * 0.5
    b.tube([parier, hand + richtung * 0.4, spitze], 0.01, [0.026, 0.024, 0.004], KLINGE, "schwert",
           hint=(0, 1, 0), seg=4)
    del quer


def baue():
    scene = C.reset_scene()
    img = C.make_palette_image("Held_Palette", BASE)
    mats = C.make_materials(img)
    b = C.Builder(BASE)
    for s, y in (("_b", 0.06), ("_f", -0.06)):
        bein(b, s, y)
    koerper(b)
    arm(b, "_b", (0, 0.13, 0.8), (0.02, 0.14, 0.64), (0.01, 0.15, 0.48))
    kapuze_und_umhang(b)
    arm(b, "_f", (0, -0.13, 0.8), (-0.02, -0.14, 0.64), (-0.14, -0.15, 0.55))
    schwert(b)
    obj = b.to_object("Held", img, mats)
    rig = C.make_armature("Held_Skelett", KNOCHEN, DREHUNG)
    C.skin(obj, rig)
    return scene, rig, obj


def animationen(rig):
    A = {}
    A["held_idle"] = C.build_action(rig, "held_idle", 6, [
        (1, {"cape2": 2, "cape3": 2, "upper_f": 0}, {"root": (0, 0, 0)}),
        (4, {"chest": 2, "cape1": 2, "cape2": 5, "cape3": 6, "upper_f": 3, "upper_b": 3, "schwert": -3},
         {"root": (0, -0.008, 0)}),
    ])

    def schritt(f_vor):
        s = 1 if f_vor else -1
        return {"chest": 5, "thigh_f": -28 * s, "shin_f": 12 if f_vor else 26, "foot_f": -6 * s,
                "thigh_b": 28 * s, "shin_b": 26 if f_vor else 12, "foot_b": 6 * s,
                "upper_b": -18 * s, "fore_b": -8, "cape1": 8, "cape2": 12, "cape3": 14, "hips": 3 * s}

    def durchgang(f_traeger):
        return {"chest": 5, "thigh_f": 0 if f_traeger else -14, "shin_f": 4 if f_traeger else 42,
                "thigh_b": -14 if f_traeger else 0, "shin_b": 42 if f_traeger else 4,
                "cape1": 6, "cape2": 9, "cape3": 10}
    A["held_walk"] = C.build_action(rig, "held_walk", 8, [
        (1, schritt(True), {"root": (0, -0.018, 0)}),
        (3, durchgang(False), {"root": (0, 0.008, 0)}),
        (5, schritt(False), {"root": (0, -0.018, 0)}),
        (7, durchgang(True), {"root": (0, 0.008, 0)}),
    ])

    # Schwerthieb: Weltwinkel W des Schwerts, schwert = W - (upper_f + fore_f)
    def hieb(upper, fore, welt, extra, root):
        p = {"upper_f": upper, "fore_f": fore, "schwert": welt - (upper + fore)}
        p.update(extra)
        return p, {"root": (0, root, 0)}
    aus = {"chest": -8, "upper_b": -20, "thigh_b": 10, "cape2": 4}
    zu = {"chest": 16, "thigh_f": -26, "shin_f": 20, "thigh_b": 18, "shin_b": 8, "upper_b": 20,
          "cape1": 10, "cape2": 14, "cape3": 16}
    keys = []
    for f, args in ((1, (0, 0, 0, {}, 0)),
                    (3, (-150, 10, -150, aus, 0.005)),
                    (4, (-155, 10, -160, aus, 0.008)),
                    (5, (-60, -10, 40, zu, -0.03)),
                    (6, (-50, -10, 55, zu, -0.032)),
                    (8, (-10, 0, 8, {"chest": 3}, 0))):
        p, l = hieb(*args)
        keys.append((f, p, l))
    A["held_atk_hieb"] = C.build_action(rig, "held_atk_hieb", 8, keys, cyclic=False)
    return A


def main():
    scene, rig, obj = baue()
    A = animationen(rig)
    pal = C.shaded_palette(BASE)
    tmp = tempfile.mkdtemp(prefix="held_")
    plan = [("held_idle", (48, 48), 2, 20), ("held_walk", (48, 48), 2, 20), ("held_atk_hieb", (64, 64), 2, 26)]
    only = os.environ.get("NUR")
    for name, canvas, foot, cx in plan:
        if only and name not in only.split(","):
            continue
        C.render_action(scene, rig, obj, A[name], canvas, foot, pal, name, tmp, center_x_px=cx, ppu=PPU)
    rig.animation_data.action = A["held_idle"]
    scene.frame_set(1)
    C.export_files("held", [rig, obj])


if __name__ == "__main__":
    main()
