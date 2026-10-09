# Blender-Prototyp: Modelle, Skelette, Sprites

**Status: Prototyp.** Die Figuren werden per Skript aus Grundformen gebaut. Silhouette, Farben, Skelett und Bewegung stimmen grob, die gezeichneten Details der Entwürfe (Rüstungsformen, Falten, Stil) erreichen sie nicht. Sie dienen als Vorlage für Proportionen und Bewegung. Für Sprites, die wie die Entwürfe aussehen, ist eine Cut-out-Animation aus Teile-Bögen der Entwürfe im Gespräch.

## Inhalt

| Datei | Zweck |
| --- | --- |
| `common.py` | Formen-Baukasten, Palettentextur, Cel-Shading, Skelett, Animation, Render zu Pixel-Sprites |
| `build_koenigin.py` | Königin Phase 1 (Helm, Sense) und Phase-2-Zusatz (Risse, Wurzeln); Animationen `p1_idle`, `p1_walk`, `p1_atk_richtschlag`, `p2_idle` |
| `build_held.py` | Held mit Kapuzenumhang und Schwert; Animationen `held_idle`, `held_walk`, `held_atk_hieb` |

## Ausgabe

- `assets/3d/*.blend`: Modell mit Palettentextur, Skelett und Aktionen, in Blender 4.x/5.x zu öffnen.
- `assets/3d/*.glb`: dasselbe als glTF mit Skin und Animationen.
- `assets/sprites/*.png` + `.json`: Sprite-Streifen je Animation, 12 Bilder/s, palettengebunden, mit Umriss.

## Ausführen

```
pip install bpy pillow        # Blender als Python-Modul (bpy 5.x)
python tools/blender/build_koenigin.py
python tools/blender/build_held.py
NUR=p1_idle python tools/blender/build_koenigin.py   # nur eine Animation rendern
```

Ohne Bildschirm braucht Blender `libegl1` und `libgl1`.

## Abweichungen von docs/VISUAL_KOENIGIN.md

- Richtschlag auf 128 × 128 statt 96 × 96, weil die Sense beim Ausholen über den Kopf ragt.
- Held auf 48 × 48 (Schwerthieb 64 × 64) statt 32 × 48, weil das Schwert nach vorn ragt.
