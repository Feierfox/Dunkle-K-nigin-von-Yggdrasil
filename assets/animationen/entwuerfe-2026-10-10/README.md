# Angriffe und Umarmung – Animationsentwürfe

Die Bilder wurden mit dem eingebauten Imagegen-Tool anhand der bestehenden Figuren erzeugt. Sie ersetzen keine vorhandenen Assets. Die vollständigen Erzeugungs- und Korrekturprompts stehen in PROMPTS.md.

| Sequenz | Bilder | Ablauf | Zeitbasis |
| --- | ---: | --- | --- |
| p1_atk_richtschlag | 10 | Ausholen, Sensenschlag nach links, tiefe Trefferpose, Rückkehr | 12 Bilder/s, ca. 0,83 s |
| held_atk_hieb | 8 | Ausholen, Schwerthieb nach rechts, Rückkehr | 12 Bilder/s, ca. 0,67 s |
| p1_ritual_umarmung_feuer | 8 Schlüsselbilder | Niederknien, gefallenen Helden aufnehmen, halten, eisblaues Feuer, leere Arme | 43 Ticks bei 12/s, ca. 3,58 s |

Die Königin trägt ihren geschlossenen Helm. Der Held bleibt unter seiner Kapuze gesichtslos. Die Umarmung ist das Ritual mit dem gefallenen Gegner; die Sense ist dabei außerhalb des Bildes abgelegt.

## Dateien pro Sequenz

**Im Repository** liegen pro Sequenz nur `sheet.webp` (komprimierte Kopie von sheet.png, Qualität 90, Alpha verlustfrei), `animation.json` und `preview.gif`. Die PNG-Originale, die Einzelbilder und `source-sheet.png` bleiben lokal beim Projektinhaber. Die Einzelbilder sind die 720 × 600 großen Felder des Sheets.

- source-sheet.png: unverändertes ausgewähltes Imagegen-Ergebnis mit echter Transparenz.
- 00.png usw.: einzelne Bilder auf gemeinsamer transparenter Arbeitsfläche, 720 × 600 px.
- sheet.png: neu angeordnetes PNG-Sheet, ohne Neuzeichnen oder Skalieren der Bildpixel.
- animation.json: Bildrechtecke, Anker, Reihenfolge und Haltezeiten. Dies ist Entwurfs-Metadatenformat, keine bestehende PSPSDK-Schnittstelle.
- preview.gif: wiederholte Wiedergabe auf dunklem Hintergrund, mit zusätzlicher Schluss-Pause von 0,7 s nur in der Vorschau. PNG und JSON enthalten diese Pause nicht.

pack_previews.py dokumentiert die Aufteilung und die manuell gesetzten Körperanker. Die Alpha-Kanal-Prüfung und Bildzahlen stehen in validation.json. Die Aufteilung prüft auf sichtbare Schnittüberschneidungen und auf abgeschnittene Bilder.

## Stand und Grenzen

Diese Dateien sind bewegte Konzeptentwürfe, noch keine fertigen PSP-Sprites. Die PNGs besitzen echte Alpha-Transparenz, enthalten aber sehr viele Farben und teilweise weiche Randpixel. Bildweise Abweichungen bei Proportionen, Waffendetails und der Rückkehr zur Ausgangshaltung bestehen weiterhin. Die Körperanker sind visuell gesetzt und brauchen bei der Endbearbeitung eine Pixelprüfung.

Die endgültige Fassung benötigt eine sorgfältige Überarbeitung bei den Zielgrößen (Königin-Angriffe 96 × 96, Held-Körper 32 × 48 mit Waffenüberhang), feste Paletten mit maximal 32 Farben und Atlanten von höchstens 512 × 512. Die vorliegenden großen Sheets sind ausdrücklich Arbeitsdateien. Weitere Sense-Angriffe, Portalritual und die Animationen der übrigen Phasen sind in diesem Paket noch nicht enthalten.

## PSP-Sprites daraus

`tools/cutout/entwuerfe.py` macht daraus Sprites in `assets/sprites/cutout/` (`koenigin_p1_atk_richtschlag`, `held_atk_hieb`, `koenigin_p1_umarmung`). Sie ersetzen die alten Cut-out-Fassungen in der PSP-Testszene. Die Sprites sind automatisch verkleinert (32 Farben), nicht von Hand nachgezeichnet. Offen bleiben:

- Die Größe der Figur schwankt leicht zwischen den Bildern (Held im Schwerthieb: 45 px im ersten, 43 px im letzten Bild). Der Maßstab ist pro Animation gemittelt.
- Die Umarmung ist mit 116 × 93 breiter als die geplanten 96 × 96, weil der liegende Held mit im Bild ist. Sein Umhang wechselt dort nicht die Farbe mit der Ausrüstungsstufe.
- Der liegende Körper aus `held_tod` ist kleiner als der Held in der Umarmung; beim Start der Umarmung wirkt er dadurch plötzlich größer.
