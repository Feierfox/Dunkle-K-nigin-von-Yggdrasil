# Animationen aus den Konzeptbildern

`verformen.py` erzeugt Animationen direkt aus den Entwürfen in `assets/konzept/`: Jedes Bild wird pro Animationsbild leicht verformt (Atmen, wehender Mantel und Haar, Schweben). Danach wird es auf Sprite-Größe verkleinert und auf eine für alle Bilder gleiche Palette gebunden. Dadurch sehen die Sprites aus wie die Entwürfe.

Ausgabe in `assets/sprites/cutout/`: Sprite-Streifen (`.png`), Bildpositionen (`.json`), Vorschau (`_vorschau.gif`, vierfach vergrößert).

| Animation | Quelle | Bilder |
| --- | --- | --- |
| `koenigin_p1_idle` | koenigin-idle-sense-helm-v5 | 6 |
| `koenigin_p2_idle` | koenigin-p2-helmbruch-v1 | 10, schwebend |
| `held_idle` | held-idle-hood-v3 | 6 |

```
pip install pillow numpy
python tools/cutout/verformen.py
```

**Grenze:** Verformung reicht für ruhige Bewegungen. Gehen, Angriffe und Rituale brauchen bewegliche Einzelteile (Cut-out mit Gelenken). Die Sense mit dem vorderen Arm lässt sich aus dem Bild ausschneiden; verdeckte Stellen wie die Beine unter dem Mantel brauchen zusätzliche Teile-Bilder.
