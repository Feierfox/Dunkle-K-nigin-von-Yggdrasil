# SFX: technische Prüfung und erste Mischungen

[Originale und Mischungen anhören](index.html) · [Messbericht](reports/SUMMARY.md) · [Originalquellen](selected_sources.json) · [Mischrezepte](mix_recipes.json)

Stand 10.10.2026. Fünf CC0-Quellen heruntergeladen, 267 einzelne Audiodateien decodiert und technisch untersucht. Vollständige Archive und lokale Lizenzseiten-Nachweise liegen außerhalb des Repositorys im Arbeitscache. sources.json dokumentiert URLs, Autoren, Downloadgrößen und SHA-256-Prüfsummen. Nur die tatsächlich verwendeten Originaldateien wurden in originals/ übernommen. Alle gewählten Quellen sind laut ihren OpenGameArt-Seiten CC0; es wurden keine Sonniss- oder 99Sounds-Dateien übernommen.

## Geleistet

- 23 Clipping-Verdachtsfälle und ein auffälliges Dateiende markiert und aus der Auswahl ausgeschlossen.
- Elf bearbeitete Mischungen: drei Schrittvarianten, Schwerthieb, Richtschlag, beide Ranken, Weltgericht-Aufladung, Entladung, Gesamtvergleich mit Ausklang und eine bewusst kurze Todesstille-Fassung.
- Quellanteile geschichtet, gefiltert und teilweise verlangsamt; ein gemeinsamer dezenter synthetischer Raumhall ergänzt. Die Rezepte dokumentieren die Eingriffe. Der Waffenschwung wurde aus einer Mehrfachaufnahme anhand der Energiehüllkurve mit zusätzlichem Rand isoliert; seine Hörprüfung steht aus.
- Master: 48 kHz, 24 Bit, Stereo. PSP-Vergleich: 22.050 Hz, 16 Bit, Mono. Exportdateien erneut decodiert, auf Clipping-Verdacht, Endabriss-Indikatoren und Endwerte geprüft. Mono-RMS-Verlust unter 3 dB geprüft; das ist keine vollständige Phasenanalyse.
- Ranken-Durchbruch bei 8/12 s, Rückzug bei 21/12 s. Weltgericht-Entladung bei zwei Sekunden, passend zur Animationszeitbasis.

## Hörprüfung und Qualitätsstand

**Ich kann mit den verfügbaren Werkzeugen keine Audio-Wahrnehmung durchführen.** Die Dateien sind technisch untersuchte Sounddesign-Entwürfe, keine behauptete Hörfreigabe oder bestätigte AA-Endqualität. Lautsprecherwiedergabe, subjektives Rauschen, Klangfarbe, überzeugende Wucht, räumliche Wirkung und die Passung im Spiel sind noch zu beurteilen. Die Vorschauseite enthält deshalb Originale, Master und Mono-Fassungen zum direkten Vergleich.

Ein ruhiges Dateiende allein beweist nicht, dass eine Aufnahme vollständig ausklingt. Viele Originale sind normalisiert; einige kommen als OGG oder mit .mp3.flac-Dateinamen. Die Container sind kein Nachweis einer verlustfreien Erstaufnahme. Mehr Bit beziehungsweise höhere Samplingrate reparieren keine ursprünglichen Codec-Artefakte. Der synthetische Hall ist ein Gestaltungsmittel und kein Wiederherstellen fehlender Originalnachklänge. Längere Enden dürfen im Spiel nicht automatisch am Ende des Animationsbildes abgeschnitten werden.

Beim Weltgericht widersprechen sich voller Nachhall und unmittelbare Todesstille als Gestaltungsziele. Deshalb existieren getrennte Fassungen: weltgericht_demo_voller_ausklang zeigt die lange Nachwirkung, weltgericht_todesstille hat nach der Entladung einen absichtlich geformten 220-ms-Abschluss. Keine Variante ändert die Spielmechanik oder wird automatisch als Endfassung eingebunden.

Die Originalquellen bleiben unverändert. Vor endgültigem Einsatz bitte die Mischungen zuerst mit moderater Lautstärke und dann zusammen mit Musik/Animation auf Kopfhörern und echten PSP-Lautsprechern beurteilen.

## Werkzeuge

download_sources.py beschafft und entpackt die verifizierten Quellen; analyze_sources.py untersucht die Dateien; build_mixes.py erstellt die Entwürfe; create_review.py prüft die tatsächlichen Exporte und baut die Vorschau. Benötigt werden die Pakete aus requirements.txt. Standardmäßig liegt der Downloadcache unter ~/.cache/dark-queen-audio; DARK_QUEEN_AUDIO_CACHE kann ihn ändern. DARK_QUEEN_AUDIO_DEPS ist ein optionaler Pfad zu lokal installierten Python-Paketen; mit normaler virtueller Umgebung ist er nicht nötig. Es sind keine benutzerspezifischen absoluten Pfade erforderlich. Kein KI-Audio wurde erzeugt.

Für den Hörvergleich ist keine Python-Installation nötig: index.html lokal öffnen. Für erneute Exportprüfung: Python-Pakete installieren und `python create_review.py` ausführen. Die Mischungen können aus den mitgelieferten Originalen mit `python build_mixes.py` neu aufgebaut werden; erneutes Herunterladen der ganzen Bibliotheken ist dafür nicht nötig. Alle Quellen und Lizenzen stehen in LICENSES.md.
