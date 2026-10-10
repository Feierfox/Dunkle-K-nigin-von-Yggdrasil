"""Wandelt Sprites und Hintergründe in PSP-Texturen um.

Ausgabe:
    psp/data/<gruppe>.bin    Texturseiten (8 Bit, höchstens 512 x 512) mit Farbtabelle (CLUT)
    psp/src/assets_gen.h     Tabellen für den C-Code: Animationen, Bilder, Ankerpunkte

Format einer .bin-Datei (little endian):
    "DKAT"  u16 seiten  u16 cluts
    cluts x 256 x u32   Farbtabellen (Byte-Reihenfolge R, G, B, A)
    je Seite: u16 breite, u16 hoehe, breite*hoehe Bytes Farbindex (0 = transparent)

    python tools/psp/assets_bauen.py
"""

import colorsys
import json
import os
import struct

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CUT = os.path.join(REPO, "assets", "sprites", "cutout")
FX = os.path.join(REPO, "assets", "sprites", "effekte")
KONZEPT = os.path.join(REPO, "assets", "konzept")
OUT_DATA = os.path.join(REPO, "psp", "data")
OUT_H = os.path.join(REPO, "psp", "src", "assets_gen.h")
SEITE = 512


def anker_verformen(pad, breite_ziel, quelle_w, mitte_x, fuss_y):
    s = (quelle_w + 2 * pad) / breite_ziel
    return ((pad + mitte_x) / s, (pad + fuss_y) / s)


# Ankerpunkt je Animation = Fußpunkt unter der Körpermitte im Bild (Sprite-Pixel).
# None: Anker aus dem JSON der Animation ("anker", z. B. von tools/cutout/entwuerfe.py).
K_IDLE = anker_verformen(64, 72, 1024, 560, 1490)
K_P2 = anker_verformen(96, 72, 1024, 560, 1490)
K_ATK = ((820 + 560) / 16, (2048 - 1536 - 32 + 1490) / 16)
K_ATK_P2 = K_ATK  # die Schwebehöhe ist im Bild enthalten
H_IDLE = anker_verformen(48, 40, 1024, 500, 1422)
H_AKT = ((300 + 500) / 28, (2240 - 1422 - 56 + 1422) / 28)

GRUPPEN = {
    "koenigin": [
        ("Q_P1_IDLE", "koenigin_p1_idle", K_IDLE),
        ("Q_P2_IDLE", "koenigin_p2_idle", K_P2),
        ("Q_RICHTSCHLAG", "koenigin_p1_atk_richtschlag", None),
        ("Q_SENSENZUG", "koenigin_p1_atk_sensenzug", K_ATK),
        ("Q_KREISSCHNITT", "koenigin_p1_atk_kreisschnitt", K_ATK),
        ("Q_STERNSCHAUER", "koenigin_p2_atk_sternschauer", K_ATK_P2),
        ("Q_WINDKLINGE", "koenigin_p2_atk_windklinge", K_ATK_P2),
        ("Q_TODESURTEIL", "koenigin_p2_atk_todesurteil", K_ATK_P2),
        ("Q_UMARMUNG", "koenigin_p1_umarmung", None),
        ("Q_SENSE_BODEN", "koenigin_sense_boden", None),
        ("Q_AUFSTEHEN", "koenigin_p1_umarmung_stehend", None),
        ("Q_P1_GEHEN", "koenigin_p1_gehen", K_ATK),
        ("Q_PORTRAIT", "portrait_koenigin", None),
    ],
    "held": [
        ("H_IDLE", "held_idle", H_IDLE),
        ("H_GEHEN", "held_gehen", H_AKT),
        ("D_IDLE", "diener_idle", H_AKT),
        ("D_GEHEN", "diener_gehen", H_AKT),
        ("D_KNIEN", "diener_knien", H_AKT),
        ("D_TOD", "diener_tod", H_AKT),
        ("H_PORTRAIT", "portrait_held", None),   # Farbtabellen der Stufe wirken auch hier
        ("D_PORTRAIT", "portrait_diener", None),
        ("H_SPRUNG", "held_sprung", H_AKT),
        ("H_ROLLE", "held_rolle", H_AKT),
        ("H_HIEB", "held_atk_hieb", None),
        ("H_TREFFER", "held_treffer", H_AKT),
        ("H_TOD", "held_tod", None),
        ("H_SCHWERT_BODEN", "held_schwert_boden", None),
        ("H_UMARMUNG_UMHANG", "koenigin_p1_umarmung_umhang", None),  # Farbtabellen der Stufen
    ],
    "fx": [
        ("FX_RING", ("fx_impuls1_ring", 480, 48), (240, 38)),
        ("FX_FEUER", ("fx_feuer_eisblau", 40, 48), (20, 47)),
        ("FX_PORTAL", ("fx_portal", 64, 24), (32, 12)),
        ("FX_KREIS", ("fx_kreis", 30, 10), (15, 5)),
        ("FX_RUNE", ("fx_rune", 56, 16), (28, 8)),
        ("FX_STERN", ("fx_stern", 8, 18), (4, 17)),
        ("FX_EINSCHLAG", ("fx_einschlag", 28, 18), (14, 17)),
        ("FX_SICHEL", ("fx_sichel", 40, 20), (20, 19)),
        ("FX_RISS", ("fx_riss", 30, 8), (15, 4)),
        ("FX_WURZEL", ("fx_wurzel", 16, 56), (8, 55)),
        ("FX_WELLE", ("fx_welle", 24, 34), (12, 34)),
        ("FX_KUGEL", ("fx_kugel", 26, 26), (13, 13)),
        ("FX_NEBEL", ("fx_nebel_kachel", 64, 64), (0, 0)),
    ],
}


def bilder_laden(quelle):
    meta = {}
    if isinstance(quelle, tuple):
        name, fw, fh = quelle
        bogen = Image.open(os.path.join(FX, name + ".png")).convert("RGBA")
    else:
        bogen = Image.open(os.path.join(CUT, quelle + ".png")).convert("RGBA")
        meta = json.load(open(os.path.join(CUT, quelle + ".json"), encoding="utf-8"))
        fw, fh = meta["frame_w"], meta["frame_h"]
    return [bogen.crop((i * fw, 0, i * fw + fw, fh)) for i in range(bogen.width // fw)], meta


def packe(stuecke):
    """Einfaches Regalpacken in Seiten von 512 x 512. stuecke: Liste von Bildern."""
    plaetze, seiten = [], [[]]
    x = y = regal = 0
    reihenfolge = sorted(range(len(stuecke)), key=lambda i: -stuecke[i].height)
    plaetze = [None] * len(stuecke)
    for i in reihenfolge:
        w, h = stuecke[i].size
        if x + w > SEITE:
            x, y, regal = 0, y + regal, 0
        if y + h > SEITE:
            seiten.append([])
            x = y = regal = 0
        plaetze[i] = (len(seiten) - 1, x, y)
        seiten[-1].append(i)
        x += w
        regal = max(regal, h)
    return plaetze, len(seiten)


def pot2(n):
    p = 8
    while p < n:
        p *= 2
    return p


def quantisiere(seiten_bilder):
    """Gemeinsame Palette (255 Farben + transparent) für alle Seiten einer Gruppe."""
    breite = sum(b.width for b in seiten_bilder)
    hoehe = max(b.height for b in seiten_bilder)
    gesamt = Image.new("RGBA", (breite, hoehe))
    x = 0
    for b in seiten_bilder:
        gesamt.paste(b, (x, 0))
        x += b.width
    deckend = gesamt.convert("RGB")
    pal = deckend.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    farben = pal.getpalette()[:255 * 3]
    clut = [(0, 0, 0, 0)] + [(farben[i], farben[i + 1], farben[i + 2], 255) for i in range(0, len(farben), 3)]
    clut += [(0, 0, 0, 0)] * (256 - len(clut))
    indizes = []
    for b in seiten_bilder:
        q = b.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE)
        a = b.getchannel("A")
        qi = q.load()
        ai = a.load()
        daten = bytearray(b.width * b.height)
        for yy in range(b.height):
            for xx in range(b.width):
                daten[yy * b.width + xx] = 0 if ai[xx, yy] < 128 else min(255, qi[xx, yy] + 1)
        indizes.append(bytes(daten))
    return clut, indizes


def umhang_cluts(clut):
    """Fünf Farbtabellen für die Ausrüstungsstufen des Helden (siehe docs/HELD.md)."""
    stufen = [(0, 1.0, 1.0), (22, 0.85, 1.05), (8, 1.45, 1.25), (8, 1.45, 1.25), (18, 1.6, 1.15)]
    aus = []
    for dh, ds, dv in stufen:
        neu = []
        for r, g, b, a in clut:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if a and 0.25 < h < 0.5 and s > 0.15:
                nr, ng, nb = colorsys.hsv_to_rgb((h + dh / 360) % 1, min(1, s * ds), min(1, v * dv))
                neu.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
            else:
                neu.append((r, g, b, a))
        aus.append(neu)
    return aus


def schreibe_bin(name, cluts, seiten):
    os.makedirs(OUT_DATA, exist_ok=True)
    with open(os.path.join(OUT_DATA, name + ".bin"), "wb") as f:
        f.write(b"DKAT" + struct.pack("<HH", len(seiten), len(cluts)))
        for clut in cluts:
            for r, g, b, a in clut:
                f.write(bytes((r, g, b, a)))
        for w, h, daten in seiten:
            f.write(struct.pack("<HH", w, h))
            f.write(daten)


def gruppe_bauen(gname, eintraege, gid, anim_tab, frame_tab, konstanten):
    stuecke, info = [], []
    for enum, quelle, anker in eintraege:
        bilder, meta = bilder_laden(quelle)
        konstanten.update(meta.get("konstanten", {}))
        ax, ay = anker if anker else meta["anker"]
        erstes = len(info)
        for b in bilder:
            bb = b.getbbox() or (0, 0, 1, 1)
            stuecke.append(b.crop(bb))
            info.append((bb[0] - ax, bb[1] - ay))
        anim_tab.append((enum, gid, len(frame_tab) + erstes, len(bilder)))
    plaetze, n = packe(stuecke)
    seiten = []
    for s in range(n):
        idx = [i for i, p in enumerate(plaetze) if p[0] == s]
        w = pot2(max(plaetze[i][1] + stuecke[i].width for i in idx))
        h = pot2(max(plaetze[i][2] + stuecke[i].height for i in idx))
        seite = Image.new("RGBA", (w, h))
        for i in idx:
            seite.alpha_composite(stuecke[i], plaetze[i][1:])
        seiten.append(seite)
    clut, indizes = quantisiere(seiten)
    cluts = umhang_cluts(clut) if gname == "held" else [clut]
    schreibe_bin(gname, cluts, [(s.width, s.height, d) for s, d in zip(seiten, indizes)])
    for i, st in enumerate(stuecke):
        p, x, y = plaetze[i]
        ox, oy = info[i]
        frame_tab.append((gid, p, x, y, st.width, st.height, round(ox), round(oy)))
    return n


def hintergrund():
    """Drei Seiten: Thronsaal Phase 1, 2 (türkise Fackeln) und 3 (Platzhalter, dunkler)."""
    p1 = Image.open(os.path.join(KONZEPT, "thronsaal-pixel-v2.webp")).convert("RGB").resize((480, 272), Image.Resampling.BOX)
    p2 = Image.open(os.path.join(KONZEPT, "psp", "thronsaal-p2.png")).convert("RGB")
    p3 = Image.open(os.path.join(KONZEPT, "psp", "thronsaal-p3.png")).convert("RGB")
    seiten = []
    for im in (p1, p2, p3):
        seite = Image.new("RGBA", (512, 512))
        seite.paste(im.convert("RGBA"), (0, 0))
        seiten.append(seite)
    clut, idx = quantisiere(seiten)
    schreibe_bin("saal", [clut], [(512, 512, d) for d in idx])


TITEL_HOCH = 30


def titel():
    """Titelbildschirm: das Bild aus dem PSP-Menü (psp/PIC1.PNG), eigene Farbtabelle."""
    bild = Image.open(os.path.join(REPO, "psp", "PIC1.PNG")).convert("RGB").resize((480, 272), Image.Resampling.BOX)
    # 30 Pixel nach oben, damit "Start drücken" mit Abstand unter dem Schriftzug Platz hat;
    # unten den Boden gespiegelt und abgedunkelt verlängern
    hoch = TITEL_HOCH
    neu = Image.new("RGB", (480, 272))
    neu.paste(bild.crop((0, hoch, 480, 272)), (0, 0))
    boden = bild.crop((0, 272 - hoch, 480, 272)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    neu.paste(boden.point(lambda v: int(v * 0.7)), (0, 272 - hoch))
    bild = neu
    seite = Image.new("RGBA", (512, 512))
    seite.paste(bild.convert("RGBA"), (0, 0))
    clut, idx = quantisiere([seite])
    schreibe_bin("titel", [clut], [(512, 512, d) for d in idx])


# Menütexte in der Art des Titelschriftzugs: Großbuchstaben, Anfangsbuchstaben größer,
# Bronzeverlauf mit dunkler Kontur. (Name, Text, aktiv)
MENUE_TEXTE = [
    ("START", "Start drücken", False),
    ("SPIEL", "Spiel starten", False), ("SPIEL_AKTIV", "Spiel starten", True),
    ("OPTIONEN", "Optionen", False), ("OPTIONEN_AKTIV", "Optionen", True),
    ("CREDITS", "Credits", False), ("CREDITS_AKTIV", "Credits", True),
]
MENUE_SCHRIFT = "C:/Windows/Fonts/constanb.ttf"


def _menue_text(text, aktiv, gross=26, klein=20):
    from PIL import ImageDraw, ImageFilter, ImageFont
    fg = ImageFont.truetype(MENUE_SCHRIFT, gross)
    fk = ImageFont.truetype(MENUE_SCHRIFT, klein)
    # Wortanfänge groß, Rest als kleinere Großbuchstaben (wie "THE DARK QUEEN")
    teile = []
    for wi, wort in enumerate(text.split(" ")):
        if wi:
            teile.append((" ", fk))
        teile.append((wort[0].upper(), fg))
        if len(wort) > 1:
            teile.append((wort[1:].upper(), fk))
    breite = sum(round(f.getlength(t)) for t, f in teile) + 8
    hoehe = gross + 10
    maske = Image.new("L", (breite, hoehe), 0)
    d = ImageDraw.Draw(maske)
    x = 4
    grund = 4 + fg.getmetrics()[0]
    for t, f in teile:
        d.text((x, grund - f.getmetrics()[0]), t, font=f, fill=255)
        x += round(f.getlength(t))
    # Bronzeverlauf von hell (oben) nach dunkel (unten)
    oben, unten = ((255, 236, 180), (176, 112, 52)) if aktiv else ((214, 182, 128), (120, 78, 40))
    verlauf = Image.new("RGB", (1, hoehe))
    for y in range(hoehe):
        t = min(1.0, max(0.0, (y - 6) / (hoehe - 12)))
        verlauf.putpixel((0, y), tuple(round(oben[i] + (unten[i] - oben[i]) * t) for i in range(3)))
    verlauf = verlauf.resize((breite, hoehe))
    kontur = maske.filter(ImageFilter.MaxFilter(3))
    bild = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))
    if aktiv:   # leichtes Leuchten hinter dem gewählten Punkt
        glanz = maske.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(2))
        bild.paste(Image.new("RGBA", bild.size, (190, 120, 255, 255)), (0, 0), glanz.point(lambda a: int(a * 0.55)))
    bild.paste(Image.new("RGBA", bild.size, (24, 12, 8, 255)), (0, 0), kontur)
    bild.paste(verlauf.convert("RGBA"), (0, 0), maske)
    return bild


def menue():
    """Menüseite: Hintergrund mit der Königin links (oben) und die Menütexte darunter."""
    from PIL import ImageDraw, ImageFilter
    seite = Image.new("RGBA", (512, 512))
    hg = Image.new("RGB", (480, 272), (10, 7, 14))
    # weicher violetter Schein hinter ihr
    schein = Image.new("L", (480, 272), 0)
    ImageDraw.Draw(schein).ellipse((-40, -20, 300, 300), fill=120)
    schein = schein.filter(ImageFilter.GaussianBlur(40))
    hg.paste(Image.new("RGB", hg.size, (60, 26, 84)), (0, 0), schein)
    koenigin = Image.open(os.path.join(REPO, "assets", "menu", "koenigin-preview-v1",
                                       "koenigin-helm-lila-v1.png")).convert("RGB")
    koenigin = koenigin.crop((140, 0, 900, 910)).resize((227, 272), Image.Resampling.LANCZOS)
    # nach rechts und unten ins Dunkle auslaufen lassen
    blende = Image.new("L", koenigin.size, 255)
    bp = blende.load()
    for x in range(koenigin.width):
        for y in range(koenigin.height):
            a = 1.0
            if x > 150:
                a *= max(0.0, 1 - (x - 150) / 77)
            if y > 220:
                a *= max(0.0, 1 - (y - 220) / 52)
            bp[x, y] = round(255 * a)
    hg.paste(koenigin, (8, 0), blende)
    seite.paste(hg.convert("RGBA"), (0, 0))
    rechtecke = []
    x, y, zeile = 0, 280, 0
    for name, text, aktiv in MENUE_TEXTE:
        t = _menue_text(text, aktiv)
        if x + t.width > 512:
            x, y = 0, y + zeile
            zeile = 0
        seite.alpha_composite(t, (x, y))
        rechtecke.append((name, x, y, t.width, t.height))
        x += t.width
        zeile = max(zeile, t.height)
    clut, idx = quantisiere([seite])
    schreibe_bin("menue", [clut], [(512, 512, idx[0])])
    return rechtecke


ZEICHEN = [chr(c) for c in range(32, 127)] + list("ÄÖÜäöüß„“‚‘…–’□△○✕←→↑↓▶")


def schrift(name="schrift", datei="DejaVuSansMono.ttf"):
    """Bitmap-Schrift ohne Kantenglättung, 6 x 11 Pixel je Zeichen.

    "schrift" für Königin und Held, "schrift_verderbnis" schräg für die Stimme der Verderbnis.
    """
    pfad = "/usr/share/fonts/truetype/dejavu/" + datei
    font = ImageFont.truetype(pfad, 10) if os.path.exists(pfad) else ImageFont.load_default()
    zw, zh, je_zeile = 6, 11, 42
    zeilen = (len(ZEICHEN) + je_zeile - 1) // je_zeile
    seite = Image.new("RGBA", (256, pot2(zeilen * zh)))
    d = ImageDraw.Draw(seite)
    d.fontmode = "1"
    for i, ch in enumerate(ZEICHEN):
        x, y = (i % je_zeile) * zw, (i // je_zeile) * zh
        d.text((x, y - 1), ch, font=font, fill=(255, 255, 255, 255))
    clut = [(0, 0, 0, 0), (255, 255, 255, 255)] + [(0, 0, 0, 0)] * 254
    a = seite.getchannel("A").load()
    daten = bytearray(seite.width * seite.height)
    for y in range(seite.height):
        for x in range(seite.width):
            daten[y * seite.width + x] = 1 if a[x, y] >= 128 else 0
    schreibe_bin(name, [clut], [(seite.width, seite.height, bytes(daten))])
    return zw, zh, je_zeile


def main():
    anim_tab, frame_tab, konstanten = [], [], {}
    gruppen = list(GRUPPEN)
    seitenzahl = {}
    for gid, g in enumerate(gruppen):
        seitenzahl[g] = gruppe_bauen(g, GRUPPEN[g], gid, anim_tab, frame_tab, konstanten)
    hintergrund()
    titel()
    menue_rechtecke = menue()
    zw, zh, je_zeile = schrift()
    schrift("schrift_verderbnis", "DejaVuSansMono-BoldOblique.ttf")
    os.makedirs(os.path.dirname(OUT_H), exist_ok=True)
    with open(OUT_H, "w", encoding="utf-8") as f:
        f.write("/* Erzeugt von tools/psp/assets_bauen.py - nicht von Hand ändern. */\n#pragma once\n\n")
        f.write("enum { " + ", ".join(f"G_{g.upper()}" for g in gruppen) + ", G_ANZAHL };\n")
        f.write("static const char *const GRUPPEN_DATEI[] = { " + ", ".join(f'"data/{g}.bin"' for g in gruppen) + " };\n\n")
        f.write("typedef struct { unsigned char gruppe, seite; short u, v, w, h, ox, oy; } Bild;\n")
        f.write("typedef struct { unsigned char gruppe; short erstes, anzahl; } Anim;\n\n")
        f.write("enum { " + ", ".join(e[0] for e in anim_tab) + ", A_ANZAHL };\n\n")
        f.write("static const Anim ANIMS[] = {\n")
        for enum, gid, erstes, anzahl in anim_tab:
            f.write(f"    {{{gid}, {erstes}, {anzahl}}}, /* {enum} */\n")
        f.write("};\n\nstatic const Bild BILDER[] = {\n")
        for t in frame_tab:
            f.write("    {%d, %d, %d, %d, %d, %d, %d, %d},\n" % t)
        f.write("};\n\n")
        f.write("/* Maße aus den Sprites (\"konstanten\" im JSON) */\n")
        for k, v in sorted(konstanten.items()):
            f.write(f"#define {k} {v}\n")
        f.write("\n")
        f.write(f"#define SCHRIFT_ZW {zw}\n#define SCHRIFT_ZH {zh}\n#define SCHRIFT_JE_ZEILE {je_zeile}\n")
        f.write("/* Zeichenvorrat der Schrift als UTF-8, Index = Position */\n")
        zeichen_c = "".join(ZEICHEN).replace("\\", "\\\\").replace('"', '\\"')
        f.write(f'static const char SCHRIFT_ZEICHEN[] = "{zeichen_c}";\n')
        f.write("\n/* Menütexte auf der Seite data/menue.bin (u, v, w, h) */\n")
        f.write("enum { " + ", ".join(f"MT_{n}" for n, *_ in menue_rechtecke) + ", MT_ANZAHL };\n")
        f.write("static const short MENUE_TEXT[][4] = {\n")
        for n, x, y, w, h in menue_rechtecke:
            f.write(f"    {{{x}, {y}, {w}, {h}}}, /* MT_{n} */\n")
        f.write("};\n")
    print("Gruppen:", {g: seitenzahl[g] for g in gruppen}, "Bilder:", len(frame_tab))


if __name__ == "__main__":
    main()
