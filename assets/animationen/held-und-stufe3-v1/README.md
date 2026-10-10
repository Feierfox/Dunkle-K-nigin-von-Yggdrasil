# Held und Königin Stufe 3 – bewegte Entwürfe

Mit dem eingebauten Imagegen-Tool erstellt. Die verwendeten Prompts und Korrekturen sind in PROMPTS.md gespeichert. Alle Ergebnisse liegen in diesem Ordner; vorhandene Animationen wurden nicht überschrieben. Die Vorschau index.html zeigt alle sechs Clips mit Pause und Einzelbild-Regler und benötigt keine Netzwerkverbindung.

| Clip | Schlüsselbilder | Dauer bei 12 Ticks/s | Inhalt |
| --- | ---: | ---: | --- |
| held_sprung | 8 | 0,67 s | Vorbereitung, Absprung, Scheitelpunkt, Landung |
| held_rolle | 8 | 0,67 s | Ducken, volle Rolle, Aufrichten |
| held_amulett_schild | 8 | 1,83 s | Amulett berühren, goldenen Schild bilden, halten, ausblenden |
| p3_atk_ranken | 8 | 2,33 s / 28 Ticks | Warnung, Wurzelausbruch, Höhepunkt, Rückzug |
| p3_atk_erinnerungsriss | 8 | 1,50 s / 18 Ticks | Riss öffnen, Erinnerungswelle freisetzen, schließen |
| p3_atk_weltgericht | 8 | 4,00 s / 48 Ticks | Aufladen 24 Ticks, Entladung und Erholung 24 Ticks |

Die längeren Zeiten entstehen durch Halten von Schlüsselbildern. Es sind ausdrücklich nicht 28, 18 oder 48 individuell gezeichnete Bewegungsbilder. Die Vorschauen wiederholen sich mit zusätzlicher Pause von 0,7 s am Ende; die JSON-Daten enthalten diese Vorschaupause nicht. Alle Clips sind im Entwurf einmalige Aktionen, keine nahtlosen Schleifen.

## Dateien

Jeder Clip enthält source-sheet.png (ausgewähltes Imagegen-Ergebnis), 00.png bis 07.png (transparente Einzelbilder auf einer Arbeitsfläche 960 × 720), sheet.png (4 × 2), animation.json (Rechtecke, Anker, Haltezeiten) und preview.gif (dunkler Vorschauhintergrund). PNGs behalten den Alpha-Kanal. Die Verpackung verschiebt die Bildpixel lediglich; sie zeichnet oder skaliert sie nicht neu. pack_previews.py dokumentiert die Aufteilung; validation.json enthält Alpha-Prüfung, Bildzahlen, Farben und Schnittpositionen.

Der Held bleibt geschlechtsneutral und gesichtslos unter seiner grünen Kapuze. Die Königin blickt nach links; Stufe 3 zeigt ihr dunkles Gesicht, Wurzelflügel und den mit dem Arm verbundenen Sensenansatz. Eisblau und Türkis kennzeichnen ihre Magie, Magenta die Verderbnis und Kristalle.

## Noch erforderlich für die PSP

Dies sind Animationsentwürfe, keine produktionsfertigen Spielassets. Die Bilder enthalten weiche Randpixel und mehr als 32 Farben; Körper- und Waffendetails wechseln stellenweise zwischen den Posen. Insbesondere das verschmolzene Sensenblatt ist in aktiven Stufe-3-Posen nicht durchgehend klar abgebildet. Flügel und Angriffseffekte sind im Entwurf noch mit dem Körper zusammengefasst. Die Anker sind manuell gesetzt, die Bewegungen nicht auf der PSP getestet.

Für den finalen Export: Held-Körper 32 × 48, Stufe-3-Körper 80 × 112, Flügel separat (zusammen etwa 160 × 112), harte Pixelkanten und feste Palette bis 32 Farben, ausgearbeitete Zwischenbilder, Atlanten höchstens 512 × 512. Die vorliegenden großen Arbeits-Sheets und das JSON-Entwurfsformat dürfen nicht direkt als PSP-Produktionsformat behandelt werden.

