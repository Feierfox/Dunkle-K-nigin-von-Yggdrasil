"""Gemeinsame Bausteine für die Blender-Modelle von "Dunkle Königin von Yggdrasil".

Die Modelle sind Vorlagen für 2D-Pixel-Sprites (siehe docs/VISUAL_KOENIGIN.md).
Sie bestehen aus einem einzigen Mesh pro Figur, einer Palettentextur (jede Farbe
ein Feld, die UVs zeigen auf die Feldmitte) und einem Skelett mit Gewichtung.

Ausführen mit Blender als Python-Modul (bpy) oder mit
    blender --background --python tools/blender/build_koenigin.py
"""

import json
import math
import os

import bpy  # muss vor bmesh geladen werden
import bmesh
from mathutils import Matrix, Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_3D = os.path.join(REPO, "assets", "3d")
OUT_SPRITES = os.path.join(REPO, "assets", "sprites")

# Hochrechnungsfaktor beim Rendern; das Bild wird danach blockweise verkleinert.
SUPERSAMPLE = 4
# Pixel pro Blender-Einheit im fertigen Sprite.
PPU = 40
# Bildrate der Animationen (docs/VISUAL_KOENIGIN.md).
FPS = 12
# Helligkeitsstufen des Cel-Shadings: Schatten, Mitte, Licht.
SHADE_LEVELS = (0.58, 0.82, 1.0)
OUTLINE = "#020007"


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


# --------------------------------------------------------------------------
# Szene


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = FPS
    return scene


# --------------------------------------------------------------------------
# Mesh-Baukasten


class Builder:
    """Sammelt alle Teile einer Figur in einem bmesh.

    Jedes Teil bekommt eine Palettenfarbe (UV auf die Feldmitte der Textur),
    optional "glow" (wird nicht schattiert) und Gewichte für Knochen.
    """

    def __init__(self, palette):
        self.palette = list(palette)  # Liste von Hex-Farben
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.verify()
        self.deform = self.bm.verts.layers.deform.verify()
        self.groups = []

    # -- Palette ----------------------------------------------------------
    def color_index(self, hexcol):
        if hexcol not in self.palette:
            self.palette.append(hexcol)
        return self.palette.index(hexcol)

    def grid(self):
        return max(1, math.ceil(math.sqrt(len(self.palette))))

    def cell_uv(self, idx, grid):
        cx, cy = idx % grid, idx // grid
        return ((cx + 0.5) / grid, 1.0 - (cy + 0.5) / grid)

    def group_index(self, name):
        if name not in self.groups:
            self.groups.append(name)
        return self.groups.index(name)

    # -- Zuweisung --------------------------------------------------------
    def _finish(self, verts, color, bone, glow, weight_fn):
        verts = list(verts)
        faces = {f for v in verts for f in v.link_faces}
        cidx = self.color_index(color)
        for f in faces:
            f.material_index = 1 if glow else 0
            for loop in f.loops:
                loop[self.uv].uv = (cidx, 0.0)  # Platzhalter, finalisiert in to_object
        for v in verts:
            d = v[self.deform]
            weights = weight_fn(v.co) if weight_fn else {bone: 1.0}
            for b, w in weights.items():
                if w > 0.0:
                    d[self.group_index(b)] = w
        return verts

    # -- Grundformen ------------------------------------------------------
    def box(self, center, size, color, bone, rot=(0, 0, 0), glow=False, weight_fn=None):
        m = Matrix.Translation(center) @ euler_matrix(rot) @ Matrix.Diagonal((*size, 1.0))
        res = bmesh.ops.create_cube(self.bm, size=1.0, matrix=m)
        return self._finish(res["verts"], color, bone, glow, weight_fn)

    def cone(self, base, tip, r1, r2, color, bone, seg=6, glow=False, weight_fn=None, scale=(1, 1)):
        base, tip = Vector(base), Vector(tip)
        axis = tip - base
        m = Matrix.Translation((base + tip) / 2) @ axis.to_track_quat("Z", "Y").to_matrix().to_4x4() \
            @ Matrix.Diagonal((scale[0], scale[1], 1, 1))
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg,
                                    radius1=r1, radius2=r2, depth=axis.length, matrix=m)
        return self._finish(res["verts"], color, bone, glow, weight_fn)

    def ball(self, center, radius, color, bone, scale=(1, 1, 1), sub=1, glow=False, weight_fn=None, rot=(0, 0, 0)):
        m = Matrix.Translation(center) @ euler_matrix(rot) @ Matrix.Diagonal((*scale, 1.0))
        res = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=radius, matrix=m)
        return self._finish(res["verts"], color, bone, glow, weight_fn)

    def tube(self, points, ra, rb, color, bone, hint=(0, 1, 0), seg=6, glow=False, weight_fn=None, cap=True):
        """Röhre entlang einer Punktliste mit elliptischem Querschnitt.

        ra/rb: Radien (Zahl oder Liste je Punkt). hint legt die Achse von ra fest.
        Damit entstehen Haarsträhnen, Mantel, Wurzeln, Sensenblatt und Stiel.
        """
        pts = [Vector(p) for p in points]
        n = len(pts)
        ra = ra if isinstance(ra, (list, tuple)) else [ra] * n
        rb = rb if isinstance(rb, (list, tuple)) else [rb] * n
        hint = Vector(hint)
        rings = []
        for i, p in enumerate(pts):
            t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
            a = hint - t * hint.dot(t)
            if a.length < 1e-5:
                a = Vector((1, 0, 0)) - t * t.x
            a.normalize()
            b = t.cross(a).normalized()
            ring = []
            for k in range(seg):
                ang = 2 * math.pi * k / seg
                ring.append(self.bm.verts.new(p + a * (math.cos(ang) * ra[i]) + b * (math.sin(ang) * rb[i])))
            rings.append(ring)
        for i in range(n - 1):
            for k in range(seg):
                k2 = (k + 1) % seg
                self.bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
        if cap:
            self.bm.faces.new(list(reversed(rings[0])))
            self.bm.faces.new(rings[-1])
        verts = [v for r in rings for v in r]
        return self._finish(verts, color, bone, glow, weight_fn)

    def crystal(self, center, size, color, bone, glow=True, stretch=1.6):
        """Achtflächiger Kristall (Raute)."""
        c = Vector(center)
        tips = [c + Vector((0, 0, size * stretch)), c - Vector((0, 0, size * stretch))]
        ring = [c + Vector((math.cos(a) * size, math.sin(a) * size, 0)) for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2)]
        vs = [self.bm.verts.new(p) for p in tips + ring]
        top, bot, r = vs[0], vs[1], vs[2:]
        for i in range(4):
            j = (i + 1) % 4
            self.bm.faces.new((top, r[i], r[j]))
            self.bm.faces.new((bot, r[j], r[i]))
        return self._finish(vs, color, bone, glow, None)

    # -- Ausgabe ----------------------------------------------------------
    def to_object(self, name, palette_image, materials):
        grid = self.grid()
        for f in self.bm.faces:
            for loop in f.loops:
                idx = int(round(loop[self.uv].uv.x))
                loop[self.uv].uv = self.cell_uv(idx, grid)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        mesh = bpy.data.meshes.new(name)
        self.bm.to_mesh(mesh)
        self.bm.free()
        for m in materials:
            mesh.materials.append(m)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        for g in self.groups:
            obj.vertex_groups.new(name=g)
        # Gruppenindizes im bmesh entsprechen der Reihenfolge in self.groups.
        for poly in mesh.polygons:
            poly.use_smooth = False
        return obj


def euler_matrix(rot):
    from mathutils import Euler
    return Euler(rot, "XYZ").to_matrix().to_4x4()


def chain_weights(bones, z_top, z_bottom):
    """Gewichte entlang einer Knochenkette nach Höhe (für Mantel und Haar)."""
    n = len(bones)

    def fn(co):
        t = (z_top - co.z) / max(1e-5, z_top - z_bottom)
        t = min(max(t, 0.0), 0.999) * n
        i = int(t)
        f = t - i
        w = {bones[i]: 1.0 - f}
        if i + 1 < n:
            w[bones[i + 1]] = f
        else:
            w[bones[i]] = 1.0
        return w
    return fn


# --------------------------------------------------------------------------
# Palettentextur und Materialien


def make_palette_image(name, palette, cell=4):
    """Schreibt die Palettentextur als PNG nach assets/3d/ und lädt sie.

    Jede Farbe belegt ein Feld von cell x cell Pixeln, zeilenweise von oben links.
    """
    from PIL import Image
    grid = max(1, math.ceil(math.sqrt(len(palette))))
    size = grid * cell
    im = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    for i, h in enumerate(palette):
        cx, cy = i % grid, i // grid
        for y in range(cell):
            for x in range(cell):
                im.putpixel((cx * cell + x, cy * cell + y), (*hex_rgb(h), 255))
    os.makedirs(OUT_3D, exist_ok=True)
    path = os.path.join(OUT_3D, name.lower() + ".png")
    im.save(path)
    img = bpy.data.images.load(path)
    img.name = name
    return img


def make_materials(img):
    """Material 0: Cel-Shading mit drei Stufen. Material 1: Leuchten ohne Schatten.

    Beide lesen die Farbe aus der Palettentextur. Für den glTF-Export ist
    zusätzlich ein Principled BSDF angeschlossen (Basisfarbe = Textur).
    """
    mats = []
    for glow in (False, True):
        mat = bpy.data.materials.new("Leuchten" if glow else "Palette")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        out.name = "Ausgabe"
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Closest"
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        if glow:
            nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = 1.0
        bsdf.name = "Export"
        emit = nt.nodes.new("ShaderNodeEmission")
        emit.name = "Render"
        if glow:
            nt.links.new(tex.outputs["Color"], emit.inputs["Color"])
        else:
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            dot = nt.nodes.new("ShaderNodeVectorMath")
            dot.operation = "DOT_PRODUCT"
            dot.inputs[1].default_value = Vector((-0.55, -0.62, 0.56)).normalized()
            nt.links.new(geo.outputs["Normal"], dot.inputs[0])
            ramp = nt.nodes.new("ShaderNodeValToRGB")
            ramp.color_ramp.interpolation = "CONSTANT"
            els = ramp.color_ramp.elements
            # Werte in linearem Raum, damit die sRGB-Ausgabe genau SHADE_LEVELS ergibt.
            lv = [srgb_to_linear(s * 255) / max(1e-6, srgb_to_linear(255)) for s in SHADE_LEVELS]
            els[0].position = 0.0
            els[0].color = (lv[0], lv[0], lv[0], 1)
            els[1].position = 0.45
            els[1].color = (lv[1], lv[1], lv[1], 1)
            e = els.new(0.72)
            e.color = (lv[2], lv[2], lv[2], 1)
            remap = nt.nodes.new("ShaderNodeMapRange")
            remap.inputs["From Min"].default_value = -1.0
            remap.inputs["From Max"].default_value = 1.0
            nt.links.new(dot.outputs["Value"], remap.inputs["Value"])
            nt.links.new(remap.outputs["Result"], ramp.inputs["Fac"])
            mul = nt.nodes.new("ShaderNodeMix")
            mul.data_type = "RGBA"
            mul.blend_type = "MULTIPLY"
            mul.inputs["Factor"].default_value = 1.0
            nt.links.new(tex.outputs["Color"], mul.inputs[6])
            nt.links.new(ramp.outputs["Color"], mul.inputs[7])
            nt.links.new(mul.outputs[2], emit.inputs["Color"])
        nt.links.new(emit.outputs[0], out.inputs[0])
        mats.append(mat)
    return mats


def material_mode(mode):
    """'render': Cel-Shading über Emission. 'export': Principled BSDF für glTF."""
    for mat in bpy.data.materials:
        if not mat.use_nodes or "Ausgabe" not in mat.node_tree.nodes:
            continue
        nt = mat.node_tree
        src = nt.nodes["Render" if mode == "render" else "Export"]
        nt.links.new(src.outputs[0], nt.nodes["Ausgabe"].inputs[0])


# --------------------------------------------------------------------------
# Skelett


def make_armature(name, bones, rot_z_deg):
    """bones: Liste (name, kopf, schwanz, eltern)."""
    arm = bpy.data.armatures.new(name)
    obj = bpy.data.objects.new(name, arm)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    for bname, head, tail, parent in bones:
        eb = arm.edit_bones.new(bname)
        eb.head, eb.tail = Vector(head), Vector(tail)
        if parent:
            eb.parent = arm.edit_bones[parent]
            eb.use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in obj.pose.bones:
        pb.rotation_mode = "QUATERNION"
    obj.rotation_euler = (0, 0, math.radians(rot_z_deg))
    return obj


def skin(mesh_obj, arm_obj):
    mesh_obj.parent = arm_obj
    mod = mesh_obj.modifiers.new("Skelett", "ARMATURE")
    mod.object = arm_obj


# --------------------------------------------------------------------------
# Animation


def new_action(arm_obj, name):
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    if arm_obj.animation_data is None:
        arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    return act


def key_pose(arm_obj, frame, pose, loc=None):
    """pose: {knochen: neigung} oder {knochen: (neigung, seite)} in Grad.

    Neigung dreht um die seitliche Achse der Figur (Ruhelage, Welt -Y vor der
    Drehung des Skelettobjekts). Bei einer Figur mit Blick nach -X kippt ein
    positiver Wert einen nach oben zeigenden Knochen nach vorn; ein nach unten
    zeigender Knochen (Bein, Arm) schwingt damit nach hinten.
    Seite dreht um die Längsachse Welt +X. Nicht genannte Knochen stehen auf 0.
    loc: {knochen: (x, y, z)} im Knochenraum; beim Wurzelknochen ist y oben.
    """
    from mathutils import Quaternion
    for pb in arm_obj.pose.bones:
        v = pose.get(pb.name, 0.0)
        pitch, side = (v, 0.0) if isinstance(v, (int, float)) else v
        rest_inv = pb.bone.matrix_local.to_3x3().inverted()
        ax_p = (rest_inv @ Vector((0, -1, 0))).normalized()
        ax_s = (rest_inv @ Vector((1, 0, 0))).normalized()
        pb.rotation_quaternion = Quaternion(ax_p, math.radians(pitch)) @ Quaternion(ax_s, math.radians(side))
        pb.keyframe_insert("rotation_quaternion", frame=frame)
        pb.location = (loc or {}).get(pb.name, (0, 0, 0))
        pb.keyframe_insert("location", frame=frame)


def build_action(arm_obj, name, frames, keys, cyclic=True):
    """keys: Liste (bild, pose, loc). Bild 1 = erstes Sprite-Bild.

    Bei Schleifen wird Bild frames+1 gleich Bild 1 gesetzt, damit die
    Interpolation nahtlos ist; gerendert werden nur die Bilder 1..frames.
    """
    act = new_action(arm_obj, name)
    for frame, pose, loc in keys:
        key_pose(arm_obj, frame, pose, loc)
    if cyclic:
        f, pose, loc = keys[0]
        key_pose(arm_obj, frames + 1, pose, loc)
    act["sprite_frames"] = frames
    return act


# --------------------------------------------------------------------------
# Rendern zu Pixel-Sprites


def setup_camera(scene, canvas_w, canvas_h, foot_px, center_x_px=None, ppu=PPU):
    """Orthografische Seitenkamera. foot_px: Abstand der Füße vom unteren Rand."""
    cam_data = bpy.data.cameras.new("Seitenkamera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(canvas_w, canvas_h) / ppu
    cam = bpy.data.objects.new("Seitenkamera", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cx = (center_x_px if center_x_px is not None else canvas_w / 2)
    # Weltkoordinate der Bildmitte: x = (canvas_w/2 - cx)/PPU, z = (canvas_h/2 - foot_px)/PPU
    cam.location = ((canvas_w / 2 - cx) / ppu, -20.0, (canvas_h / 2 - foot_px) / ppu)
    cam.rotation_euler = (math.radians(90), 0, 0)
    r = scene.render
    r.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.cycles.use_denoising = False
    scene.cycles.device = "CPU"
    scene.cycles.max_bounces = 0
    r.filter_size = 0.01
    r.film_transparent = True
    r.resolution_x = canvas_w * SUPERSAMPLE
    r.resolution_y = canvas_h * SUPERSAMPLE
    r.resolution_percentage = 100
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    if scene.world is None:
        scene.world = bpy.data.worlds.new("Welt")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Strength"].default_value = 0.0
    return cam


def render_frame(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def downsample_to_sprite(src_path, palette_hex):
    """Blockweise Verkleinerung (häufigste Farbe), Palettenbindung, Umriss."""
    from PIL import Image
    from collections import Counter

    im = Image.open(src_path).convert("RGBA")
    W, H = im.size
    s = SUPERSAMPLE
    w, h = W // s, H // s
    src = im.load()
    pal = [hex_rgb(c) for c in palette_hex]
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o = out.load()

    def nearest(c):
        return min(pal, key=lambda p: (p[0] - c[0]) ** 2 * 2 + (p[1] - c[1]) ** 2 * 3 + (p[2] - c[2]) ** 2 * 2)

    cache = {}
    for y in range(h):
        for x in range(w):
            cols = []
            for yy in range(y * s, y * s + s):
                for xx in range(x * s, x * s + s):
                    p = src[xx, yy]
                    if p[3] >= 128:
                        cols.append(p[:3])
            if len(cols) * 8 >= s * s * 3:
                # häufigste Farbe nach Palettenbindung
                mapped = []
                for c in cols:
                    if c not in cache:
                        cache[c] = nearest(c)
                    mapped.append(cache[c])
                o[x, y] = (*Counter(mapped).most_common(1)[0][0], 255)
    # Umriss: transparente Pixel neben deckenden werden dunkel.
    ol = hex_rgb(OUTLINE)
    edge = []
    for y in range(h):
        for x in range(w):
            if o[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and o[nx, ny][3] == 255 and o[nx, ny][:3] != ol:
                        edge.append((x, y))
                        break
    for x, y in edge:
        o[x, y] = (*ol, 255)
    return out


def shaded_palette(base_hex, glow_hex=()):
    """Alle Palettenfarben in drei Helligkeitsstufen plus Leuchtfarben unverändert."""
    out = []
    for h in base_hex:
        r, g, b = hex_rgb(h)
        for lv in SHADE_LEVELS:
            c = "#%02x%02x%02x" % (round(r * lv), round(g * lv), round(b * lv))
            if c not in out:
                out.append(c)
    for h in glow_hex:
        if h not in out:
            out.append(h)
    if OUTLINE not in out:
        out.append(OUTLINE)
    return out


def render_action(scene, arm_obj, mesh_obj, action, canvas, foot_px, palette_hex, prefix, tmpdir, center_x_px=None, ppu=PPU):
    """Rendert eine Aktion als waagerechten Streifen plus JSON mit Bildpositionen."""
    from PIL import Image

    cw, ch = canvas
    for c in [o for o in scene.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(c)
    material_mode("render")
    setup_camera(scene, cw, ch, foot_px, center_x_px, ppu)
    arm_obj.animation_data.action = action
    frames = int(action.get("sprite_frames", 1))
    sheet = Image.new("RGBA", (cw * frames, ch), (0, 0, 0, 0))
    meta = {"name": prefix, "frame_w": cw, "frame_h": ch, "fps": FPS, "frames": [], "foot_y": ch - foot_px}
    for i in range(frames):
        scene.frame_set(i + 1)
        raw = os.path.join(tmpdir, f"{prefix}_{i:03d}.png")
        render_frame(scene, raw)
        spr = downsample_to_sprite(raw, palette_hex)
        sheet.paste(spr, (i * cw, 0))
        meta["frames"].append({"x": i * cw, "y": 0, "w": cw, "h": ch})
    os.makedirs(OUT_SPRITES, exist_ok=True)
    sheet.save(os.path.join(OUT_SPRITES, prefix + ".png"))
    with open(os.path.join(OUT_SPRITES, prefix + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    return sheet


def export_files(name, select_objs):
    os.makedirs(OUT_3D, exist_ok=True)
    for img in bpy.data.images:
        if img.source == "FILE" and not img.packed_file:
            img.pack()
    material_mode("export")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_3D, name + ".blend"), compress=True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in select_objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_3D, name + ".glb"), export_format="GLB",
                              use_selection=True, export_animations=True,
                              export_animation_mode="ACTIONS", export_skins=True)
