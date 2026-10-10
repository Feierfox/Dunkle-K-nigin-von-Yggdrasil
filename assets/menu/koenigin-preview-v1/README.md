# Königin: animierte PSP-Menüvorschau

Die Königin aus koenigin-v1.png wurde mit dem eingebauten Imagegen-Tool bearbeitet: geschlossener Helm mit fünf Astkronenspitzen nach dem Sprite, violett leuchtende Augen und Glühnebel. Rüstung, Haar, Mantel, Pose und die ursprüngliche Waffe bleiben gestalterisch erhalten. Das Ausgangsbild bleibt unverändert; die bearbeitete Fassung liegt in koenigin-helm-lila-v1.png. Vollständiger Prompt: PROMPTS.md.

Die 16-Sekunden-Vorschau zeigt einen Ausschnitt von Krone, Helm und Oberkörper. Die Kamera bewegt sich langsam vor und zurück, violetter Lichtnebel pulsiert am Helm. Es handelt sich um eine animierte Standbildinszenierung, nicht um eine neue Körperanimation. Das freigegebene Thronsaal-Wallpaper psp/PIC1.PNG bleibt gesetzt.

## Musik und Rechte

Musik: **The Final Battle** von **skrjablin**, laut [Originalseite](https://opengameart.org/content/the-final-battle) CC0/Public Domain. the_final_battle-original.ogg ist die unveränderte Quelle. theme-16s.wav verwendet die ersten 16 Sekunden mit 0,35 s Einblendung, 1,4 s Ausblendung und reduziertem Pegel. Herkunft, Prüfsumme und Einstellungen stehen in provenance.json. Die Auswahl beruht auf der Quellenbeschreibung als dramatische Orchestermusik; eine eigene auditive Freigabe wird nicht behauptet.

Das PSP-Media-Toolkit steht unter MIT und ist mit Lizenz und festgehaltener Version unter tools/psp/vendor/psp-media-toolkit enthalten. Eine lokale Anpassung verwendet kurze GOPs, um die PTS-Abstände im erzeugten Preview unter 0,7 s zu halten. Encoder-Binaries von FFmpeg und atracdenc werden nur im lokalen Werkzeugcache gespeichert, nicht im Repository verteilt.

## Dateien

- preview-16s.mp4: Vorschau mit Ton, 720 × 408, H.264/AAC.
- psp/ICON1.PMF: animiertes XMB-Symbol, 144 × 80, H.264 im PSMF-Container.
- psp/SND0.AT3: zugehörige Menü-Musik, ATRAC3, 44,1 kHz Stereo.
- psp/EBOOT.PBP: eingebettetes Wallpaper, statisches Symbol, Menüvideo und Musik.

Die PMF-Prüfung decodiert 480 Frames, vergleicht die demuxten Video-Daten mit der Kodierung, prüft Indexeinträge und PTS-Abstände. ATRAC wurde mit FFmpeg decodiert. ICON1 und SND0 zusammen liegen unter 500 KiB. Der kompilierte Spielcode bleibt beim Packen unverändert. Noch kein Test im XMB einer echten PSP-1000; diese strukturellen und Decoder-Prüfungen garantieren keinen Hardwaretest.

Neu erstellen: `python tools/psp/prepare_preview_tools.py`, danach `python tools/psp/menu_video_bauen.py --toolkit tools/psp/vendor/psp-media-toolkit`, anschließend `python tools/psp/menu_bauen.py --repack --media`. Für den Bildexport benötigt menu_bauen.py Pillow.
