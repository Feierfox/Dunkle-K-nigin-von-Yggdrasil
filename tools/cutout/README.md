# Animationen aus den Konzeptbildern

`verformen.py` erzeugt Animationen direkt aus den Entwürfen in `assets/konzept/`: Jedes Bild wird pro Animationsbild leicht verformt (Atmen, wehender Mantel und Haar, Schweben). Danach wird es auf Sprite-Größe verkleinert und auf eine für alle Bilder gleiche Palette gebunden. Dadurch sehen die Sprites aus wie die Entwürfe.

Ausgabe in `assets/sprites/cutout/`: Sprite-Streifen (`.png`), Bildpositionen (`.json`), Vorschau (`_vorschau.gif`, vierfach vergrößert).

| Animation | Quelle | Bilder |
| --- | --- | --- |
| `koenigin_p1_idle` | koenigin-idle-sense-helm-v5 | 6 |
| `koenigin_p2_idle` | koenigin-p2-helmbruch-v1 | 10, schwebend |
| `held_idle` | held-idle-hood-v3 | 6 |
| `koenigin_p1_atk_richtschlag` | Imagegen-Entwurf p1_atk_richtschlag (`entwuerfe.py`) | 10, 107 × 96 |
| `koenigin_p1_umarmung` | Imagegen-Entwurf p1_ritual_umarmung_feuer (`entwuerfe.py`), Held liegt im Bild | 8, 116 × 93 |
| `koenigin_p1_umarmung_umhang` | dto., nur der grüne Umhang des Helden, wird mit den Farbtabellen der Ausrüstungsstufe darübergezeichnet | 8 |
| `koenigin_p1_umarmung_stehend` | dto., erstes Bild ohne den Helden: Aufstehen nach dem Ritual | 1 |
| `koenigin_sense_boden` | koenigin-idle-sense-helm-v5, Sense flach am Boden (während der Umarmung abgelegt) | 1, 91 × 28 |
| `koenigin_p1_atk_richtschlag_alt` | koenigin-idle-sense-helm-v5, Cut-out (`angriffe.py`), nicht mehr im Spiel | 10, 128 × 128 |
| `koenigin_p1_atk_sensenzug` | dto. | 14, 128 × 128 |
| `koenigin_p1_atk_kreisschnitt` | dto., Körper in der Drehung kurz gespiegelt | 14, 128 × 128 |
| `koenigin_p2_atk_sternschauer` | koenigin-p2-helmbruch-v1, Cut-out (`angriffe.py`) | 12, 128 × 128 |
| `koenigin_p2_atk_windklinge` | dto. | 10, 128 × 128 |
| `koenigin_p2_atk_todesurteil` | dto. | 12, 128 × 128 |
| `held_sprung` | held-idle-hood-v3 (`held.py`) | 8, 64 × 80 |
| `held_rolle` | dto., Rolle auf der Stelle, die Engine bewegt ihn | 8, 64 × 80 |
| `held_atk_hieb` | Imagegen-Entwurf held_atk_hieb (`entwuerfe.py`) | 8, 76 × 54 |
| `held_atk_hieb_alt` | held-idle-hood-v3, Schwert mit Hand ausgeschnitten (`held.py`), nicht mehr im Spiel | 8, 64 × 80 |
| `held_treffer` | dto., weißes Aufblitzen | 4, 64 × 80 |
| `held_tod` | held-idle-hood-v3 (`entwuerfe.py`): sackt nach vorn zur Königin hin zusammen; die letzten Bilder sind genau der liegende Körper aus dem ersten Umarmungsbild | 8, 74 × 47 |
| `held_schwert_boden` | held-idle-hood-v3, Schwert flach am Boden (rutscht ihm im 3. Tod-Bild aus der Hand) | 1, 37 × 7 |
| `held_tod_alt` | held-idle-hood-v3 (`held.py`), kippt nach hinten, am Bildrand abgeschnitten, nicht mehr im Spiel | 8, 64 × 80 |

```
pip install pillow numpy
python tools/cutout/verformen.py   # Ruheposen
python tools/cutout/angriffe.py    # Angriffe (oder einzeln: angriffe.py sensenzug)
python tools/cutout/thronsaal.py   # Thronsaal Phase 2 und 3
python tools/cutout/ausruestung.py # Ausrüstungsstufen, Nebel-Mockup
python tools/cutout/held.py        # Bewegungen des Helden
python tools/cutout/effekte.py     # Effekte und Vorschau-Szenen
python tools/cutout/entwuerfe.py   # Sprites aus den bewegten Imagegen-Entwürfen
```

`entwuerfe.py` liest die Entwürfe aus `assets/animationen/entwuerfe-2026-10-10/` (Sheet und `animation.json`). Jede Animation wird um einen festen Faktor verkleinert, sodass die Figur so hoch ist wie in den Ruheposen (Königin 91 px, Held 44 px). Danach folgen harte Transparenz, eine gemeinsame Palette mit 32 Farben und der Zuschnitt auf das gemeinsame Rechteck. Fußpunkt (`anker`) und Haltezeiten (`dauer`) stehen im JSON; `tools/psp/assets_bauen.py` übernimmt den Anker von dort. Die Palette entsteht per Median-Cut mit k-means-Nachbesserung; ohne diese wurden kleine Farbflächen falsch (braune Stiefel und Hautton des Helden rosa).

Damit Tod und Umarmung nahtlos ineinandergehen, schneidet `entwuerfe.py` den liegenden Helden aus dem ersten Umarmungsbild aus (an der Berührstelle mit dem Stiefel der Königin nach Farbe getrennt) und verwendet genau diese Pixel als letzte Bilder von `held_tod`. Der Abstand vom Fußpunkt des Toten zum Kniepunkt der Königin (`UMARM_ABSTAND`), die Körpermitte (`TOD_MITTE`) und das Bild, ab dem das Schwert am Boden liegt (`TOD_SCHWERT_BILD`), stehen unter `konstanten` im JSON. `assets_bauen.py` schreibt sie als `#define` nach `psp/src/assets_gen.h`.

`angriffe.py` schneidet Sense, Hand und Unterarm aus dem Entwurf aus, füllt die verdeckte Stelle am Körper mit den angrenzenden Rüstungsfarben und dreht das Teil je Bild um den Ellbogen. Der Arm hebt sich beim Ausholen zusätzlich an.

`ausruestung.py` erzeugt die fünf Ausrüstungsstufen des Helden als Farbtausch (`held_stufen.png`) und das Mockup des Amulett-Schilds im lila Nebel (`assets/konzept/psp/mockup-impuls2-amulett*.png`).

`effekte.py` erzeugt Effekte in nativer Auflösung in `assets/sprites/effekte/`: Ringwelle des ersten Impulses (10 Bilder, 480 × 48), kachelbaren Nebel (64 × 64), eisblaues Feuer (8 Bilder, 40 × 48) und das lila Portal (12 Bilder, 64 × 24). Dazu vier Vorschau-Szenen als GIF in `assets/konzept/psp/`: `szene_impuls1_sprung`, `szene_impuls2_amulett`, `szene_ritual_feuer`, `szene_ritual_portal`.

Für Phase 2 und 3 kommen dazu: Zielkreis, Rune, Stern, Einschlag, Windsichel, Erinnerungsriss, Wurzel, Welle und Lichtkugel des Weltgerichts (`fx_kreis` … `fx_kugel`).

**Grenze:** Verformung reicht für ruhige Bewegungen. Gehen, Angriffe und Rituale brauchen bewegliche Einzelteile (Cut-out mit Gelenken). Die Sense mit dem vorderen Arm lässt sich aus dem Bild ausschneiden; verdeckte Stellen wie die Beine unter dem Mantel brauchen zusätzliche Teile-Bilder.
