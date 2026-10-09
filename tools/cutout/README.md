# Animationen aus den Konzeptbildern

`verformen.py` erzeugt Animationen direkt aus den Entwürfen in `assets/konzept/`: Jedes Bild wird pro Animationsbild leicht verformt (Atmen, wehender Mantel und Haar, Schweben). Danach wird es auf Sprite-Größe verkleinert und auf eine für alle Bilder gleiche Palette gebunden. Dadurch sehen die Sprites aus wie die Entwürfe.

Ausgabe in `assets/sprites/cutout/`: Sprite-Streifen (`.png`), Bildpositionen (`.json`), Vorschau (`_vorschau.gif`, vierfach vergrößert).

| Animation | Quelle | Bilder |
| --- | --- | --- |
| `koenigin_p1_idle` | koenigin-idle-sense-helm-v5 | 6 |
| `koenigin_p2_idle` | koenigin-p2-helmbruch-v1 | 10, schwebend |
| `held_idle` | held-idle-hood-v3 | 6 |
| `koenigin_p1_atk_richtschlag` | koenigin-idle-sense-helm-v5, Cut-out (`angriffe.py`) | 10, 128 × 128 |
| `koenigin_p1_atk_sensenzug` | dto. | 14, 128 × 128 |
| `koenigin_p1_atk_kreisschnitt` | dto., Körper in der Drehung kurz gespiegelt | 14, 128 × 128 |
| `held_sprung` | held-idle-hood-v3 (`held.py`) | 8, 64 × 80 |
| `held_rolle` | dto., Rolle auf der Stelle, die Engine bewegt ihn | 8, 64 × 80 |
| `held_atk_hieb` | dto., Schwert mit Hand ausgeschnitten | 8, 64 × 80 |
| `held_treffer` | dto., weißes Aufblitzen | 4, 64 × 80 |
| `held_tod` | dto., letztes Bild ist der liegende Körper | 8, 64 × 80 |

```
pip install pillow numpy
python tools/cutout/verformen.py   # Ruheposen
python tools/cutout/angriffe.py    # Angriffe (oder einzeln: angriffe.py sensenzug)
python tools/cutout/thronsaal.py   # Thronsaal Phase 2 und 3
python tools/cutout/ausruestung.py # Ausrüstungsstufen, Nebel-Mockup
python tools/cutout/held.py        # Bewegungen des Helden
python tools/cutout/effekte.py     # Effekte und Vorschau-Szenen
```

`angriffe.py` schneidet Sense, Hand und Unterarm aus dem Entwurf aus, füllt die verdeckte Stelle am Körper mit den angrenzenden Rüstungsfarben und dreht das Teil je Bild um den Ellbogen. Der Arm hebt sich beim Ausholen zusätzlich an.

`ausruestung.py` erzeugt die fünf Ausrüstungsstufen des Helden als Farbtausch (`held_stufen.png`) und das Mockup des Amulett-Schilds im lila Nebel (`assets/konzept/psp/mockup-impuls2-amulett*.png`).

`effekte.py` erzeugt Effekte in nativer Auflösung in `assets/sprites/effekte/`: Ringwelle des ersten Impulses (10 Bilder, 480 × 48), kachelbaren Nebel (64 × 64), eisblaues Feuer (8 Bilder, 40 × 48) und das lila Portal (12 Bilder, 64 × 24). Dazu vier Vorschau-Szenen als GIF in `assets/konzept/psp/`: `szene_impuls1_sprung`, `szene_impuls2_amulett`, `szene_ritual_feuer`, `szene_ritual_portal`.

**Grenze:** Verformung reicht für ruhige Bewegungen. Gehen, Angriffe und Rituale brauchen bewegliche Einzelteile (Cut-out mit Gelenken). Die Sense mit dem vorderen Arm lässt sich aus dem Bild ausschneiden; verdeckte Stellen wie die Beine unter dem Mantel brauchen zusätzliche Teile-Bilder.
