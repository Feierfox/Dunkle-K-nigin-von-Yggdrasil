# Grafikentwürfe

Erste Konzeptgrafiken vom 09.10.2026, erzeugt mit dem Bildgenerator von ChatGPT. Die vollständigen Prompts stehen in [PROMPTS.md](PROMPTS.md).

Die Dateien hier sind **komprimierte WebP-Kopien** zur Ansicht. Die PNG-Originale liegen lokal beim Projektinhaber. Die Dateinamen wurden von `arvid-…` auf `held-…` umgestellt.

## Aktuelle Entwürfe

### PSP-Menü

[Titel-Wallpaper](menu/thronsaal-title-v1/README.md) · [Königin-Vorschau mit Musik](menu/koenigin-preview-v1/index.html). Der Thronsaal trägt den Titel **The Dark Queen of Yggdrasil**; das 16-Sekunden-Menüvideo zeigt die Königin mit Helmkrone, violetten Augen und Glühnebel. ICON1.PMF und SND0.AT3 sind in EBOOT.PBP eingebunden, strukturell und per Decoder geprüft; ein echter PSP-XMB-Test steht aus. Die Originalmusik von skrjablin ist CC0.

### Audio: technisch geprüfte SFX-Entwürfe

[Elf Mischungen und Quellen](audio/audit-v1/README.md) · [Hörvergleich mit Master und PSP-Mono](audio/audit-v1/index.html) · [CC0-Originalquellen](audio/audit-v1/LICENSES.md). Schritte, Waffen, Ranken und Weltgericht wurden aus dokumentierten CC0-Aufnahmen gestaltet. 267 Dateien technisch untersucht; zwölf ausgewählte Originale, 48-kHz-Master, 22,05-kHz-Mono-Fassungen und Prüfberichte enthalten. **Hörfreigabe und AA-Endqualität stehen aus.**

### Neue Animationsentwürfe: Held und Königin Stufe 3

**Ergänzung v2:** [Zwei Bodenranken und verstärktes Weltgericht](animationen/ranken-weltgericht-v2/README.md) · [Vorschau](animationen/ranken-weltgericht-v2/index.html). Unabhängige Dornen- und Hakenranke mit Hervorbrechen und Rückzug; neue Entladung der Königin und separate saalweite Zerstörungsebene. Als Grafikentwürfe gekennzeichnet, noch keine fertigen PSP-Sprites.

[Paket und Hinweise](animationen/held-und-stufe3-v1/README.md) · [HTML-Vorschau mit Pause und Einzelbild-Regler](animationen/held-und-stufe3-v1/index.html)

Sechs Sequenzen mit je acht Schlüsselbildern: Held **Sprung, Ausweichrolle, Amulett-Schild**; Königin Stufe 3 **Ranken, Erinnerungsriss, Weltgericht**. Enthalten sind transparente PNG-Sheets, Einzelbilder, GIF-Vorschauen, JSON-Zeiten und die Imagegen-Prompts. Die längeren Angriffe halten Schlüsselbilder auf einer Zeitbasis von 12 Ticks/s; sie besitzen noch nicht alle vorgeschlagenen Zwischenbilder. Große Arbeitsauflösung, wechselnde Details und noch nicht getrennte Flügel/Effekte: **keine fertigen PSP-Sprites**.

### Figuren und Thronsaal

| Datei | Größe | Inhalt |
| --- | --- | --- |
| [konzept/koenigin-idle-sense-helm-v5.webp](konzept/koenigin-idle-sense-helm-v5.webp) | 1024 × 1536, transparent | **Königin Phase 0/1:** Ruhepose, Blick nach links, geschlossener Helm mit Kronen-Ästen, Sense aus Wurzelholz |
| [konzept/koenigin-p2-helmbruch-v1.webp](konzept/koenigin-p2-helmbruch-v1.webp) | 1024 × 1536, transparent | **Königin Phase 2:** Helm gerissen, verdorbene Wurzeln mit magentafarbenen Adern, türkise Risse auf der Rüstung, Wurzeln binden Hand und Sense, schwebend mit wehendem Mantel |
| [konzept/held-idle-hood-v3.webp](konzept/held-idle-hood-v3.webp) | 1024 × 1536, transparent | Held in Ruhepose, Seitenansicht, Blick nach rechts, grüner Kapuzenumhang, Gesicht im Schatten |
| [konzept/thronsaal-pixel-v2.webp](konzept/thronsaal-pixel-v2.webp) | 1672 × 941, deckend | Thronsaal in fester Seitenansicht: Eingang links, erhöhter leerer Thron rechts, gotische Fenster |

## PSP-Bildkonzept

Die Entwürfe verkleinert auf echte PSP-Auflösung, um Lesbarkeit und Aufteilung zu prüfen. Die Figuren stehen mittig am hinteren Rand des Bodens (Kampflinie Y ≈ 240).

| Datei | Inhalt |
| --- | --- |
| [psp/mockup-phase1-runde1.png](konzept/psp/mockup-phase1-runde1.png) (+ `-2x`) | 480 × 272: Phase 1, rote Leiste, Held mit 1 Herz |
| [psp/mockup-phase2-spaeter.png](konzept/psp/mockup-phase2-spaeter.png) (+ `-2x`) | 480 × 272: Phase 2, orange Leiste, Held mit 3 von 5 Herzen |
| [psp/koenigin-p1-sense-64x96.png](konzept/psp/koenigin-p1-sense-64x96.png) | Königin v5 automatisch auf 65 × 96 verkleinert, 24 Farben |
| [psp/koenigin-p2-helmbruch-64x96.png](konzept/psp/koenigin-p2-helmbruch-64x96.png) | Königin Phase 2 automatisch auf 65 × 96 verkleinert, 24 Farben |
| [psp/held-32x48.png](konzept/psp/held-32x48.png) | Held automatisch auf 37 × 48 verkleinert, 16 Farben |
| [psp/paletten-phasen.png](konzept/psp/paletten-phasen.png) | Farbpaletten der Phasen 1–3 |
| [psp/thronsaal-p2.png](konzept/psp/thronsaal-p2.png) (+ `-2x`) | Thronsaal Phase 2: Fackeln brennen türkis (Farbtausch aus Pixel v2) |
| [psp/thronsaal-p3.png](konzept/psp/thronsaal-p3.png) (+ `-2x`) | Thronsaal Phase 3: nur dunklere, violettere Stimmung als Platzhalter. Wurzeln und Risse folgen als Bild nach Prompt `thronsaal-p3-v1` ([PROMPTS.md](PROMPTS.md)) |
| [psp/mockup-impuls2-amulett.png](konzept/psp/mockup-impuls2-amulett.png) (+ `-2x`) | Impuls beim Wechsel zu Phase 3: lila Nebel, goldener Amulett-Schild |
| `psp/szene_*.gif` | Vorschau-Szenen: Sprung über die Ringwelle, Amulett-Schild im Nebel, Feuer- und Portal-Ritual |

Die verkleinerten Figuren sind automatisch erzeugt und nur ein Test. Echte Sprites müssen von Hand in nativer Größe gezeichnet werden. Das Phase-2-Mockup zeigt die Königin mit gerissenem Helm, 5 px schwebend. **Erkenntnis:** Bei 96 px Höhe gehen die feinen türkisen Risse und die magentafarbenen Adern beim automatischen Verkleinern fast verloren. Im nativen Sprite müssen sie als wenige, kräftige Linien gezeichnet werden.

## Bewegte Entwürfe

Animationsentwürfe vom 10.10.2026 (Imagegen): Richtschlag der Königin, Schwerthieb des Helden und die Umarmung beim Totenritual. Siehe [animationen/entwuerfe-2026-10-10/README.md](animationen/entwuerfe-2026-10-10/README.md). Daraus erzeugte PSP-Sprites: `tools/cutout/entwuerfe.py`.

## Ältere Entwürfe

| Datei | Größe | Inhalt |
| --- | --- | --- |
| [konzept/koenigin-idle-schwert-v4.webp](konzept/koenigin-idle-schwert-v4.webp) | 1024 × 1536, transparent | Königin mit Schwert und offenem Gesicht. Überholt durch v5, Grundlage der Farbpalette |
| [konzept/thronsaal-v1.webp](konzept/thronsaal-v1.webp) | 1672 × 941, deckend | Gemalter Thronsaal mit Blick auf den Wurzelthron in der Mitte. Passt nicht zur festen Seitenansicht, bleibt als Stimmungsbild erhalten |

## Abgleich mit den Dokumenten

- **Königin v5:** passt zu [KOENIGIN.md](../docs/KOENIGIN.md): geschlossener Helm, nur türkise Augen im Sehschlitz, fünf Kronenspitzen mit Kristallen, eisblaues Haar, Sense mit Wurzelstiel, Goldbändern und Kristallen. Kleine Abweichung: drei statt zwei Goldbänder am Stiel.
- **Königin Phase 2:** passt zu [VISUAL_KOENIGIN.md](../docs/VISUAL_KOENIGIN.md): Der Helm ist gerissen und von Wurzeln durchbrochen, das Gesicht bleibt verborgen; es wird erst in Phase 3 sichtbar. Die magentafarbenen Adern laufen auch durch die Wurzeln am Sensenstiel, die Verderbnis erfasst also schon die Sense.
- **Held:** passt zu [HELD.md](../docs/HELD.md): grüner Kapuzenumhang, Gesicht vollständig verschattet, geschlechtsneutrale Silhouette.
- **Thronsaal Pixel v2:** Der Thron ist hell und astförmig. Das eisblaue Licht durch einen Spalt im Stamm hinter dem Thron aus [KOENIGIN.md](../docs/KOENIGIN.md) fehlt noch.

## Stand und nächste Schritte

Die Bilder sind im Pixel-Stil gemalt, aber in hoher Auflösung und ohne festes Pixelraster. Sie sind **noch keine fertigen Sprites für die PSP-1000**. Dafür fehlen:

- Neuanlage in nativer Größe: Thronsaal 480 × 272, Königin etwa 64 × 96, Held etwa 32 × 48 Pixel (siehe [PSP1000.md](../docs/PSP1000.md)).
- Feste Farbpalette und einheitliche Pixelgröße.
- Animationen für Ruhepose, Angriffe, Ausweichen, Treffer und Tod.

## Herkunft und Rechte

Die Grafiken wurden neu generiert. Laut den Prompts dienten Referenzbilder nur als Vorlage für Kameraperspektive und Pixel-Dichte, nicht als Kopiervorlage. Die Referenzbilder selbst sind nicht Teil dieses Repositorys. Vor einer Veröffentlichung des Spiels sollten die Nutzungsbedingungen des Bildgenerators geprüft und die Grafiken möglichst durch eigene, nativ gezeichnete Pixel-Art ersetzt werden.
