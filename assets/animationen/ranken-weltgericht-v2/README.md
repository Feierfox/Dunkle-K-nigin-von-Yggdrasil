# Bodenranken und Weltgericht v2

Vier neue Animationsentwürfe, mit dem eingebauten Imagegen-Tool erstellt. Die neue Weltgericht-Fassung ersetzt gestalterisch die kleine Sichelwelle aus held-und-stufe3-v1; die ältere Version bleibt zum Vergleich erhalten. [Vorschau](index.html), [Prompts](PROMPTS.md), [Timing und Angriffsvorgaben](attack_spec.json).

## Zwei eigenständige Bodenranken

- **fx_ranke_a:** hohe, verdrehte Dornenranke mit drei spitzen Ausläufern.
- **fx_ranke_b:** breite, gegabelte Hakenranke mit ineinander verschlungenen Stämmen.

Beide Assets sind unabhängig von der Königin platzierbar. Ablauf: Bodenwarnung, Spitze tritt hervor, Ranke fährt hoch, aktive Schadensphase, Rückzug in dieselbe Bodenstelle, vollständig unsichtbares Schlussbild. Die Bodenanker aller Posen liegen bei (480, 600) auf der Arbeitsfläche. Die Wurzeln verschwinden durch Rückzug, nicht durch Wegfliegen. Acht Schlüsselbilder werden über 28 Ticks bei 12 Ticks/s gehalten. Das erste Warnbild steht acht Ticks; die aktive Fläche beginnt beim Durchbruch und endet vor dem Rückzug. Im Angriff werden drei bis vier Stellen nacheinander aktiviert, mit beiden Varianten. Es wird kein Boden in die Textur eingebrannt.

## Weltgericht: vernichtende Entladung

- **p3_atk_weltgericht_v2:** maximale Flügelöffnung, aufladender Energiekern, Entladung in beide Richtungen, Nachbeben und Erschöpfung.
- **fx_weltgericht_saal:** eigene Zerstörungsebene für den ganzen Saal: Lichtadern, Wurzelausbrüche an mehreren Stellen, Lichtgitter, Steintrümmer und abklingende Risse. Zusammen mit der Königin abspielen, nicht als einzelnes ausweichbares Geschoss.

Beide Clips dauern 48 Ticks: 24 Ticks Aufladen, danach 24 Ticks Entladung und Nachwirkung. Sie besitzen unterschiedliche Haltezeiten der acht Schlüsselbilder, damit Entladung und Höhepunkt zusammenpassen. Die saalweite Effektentladung beginnt im vierten Schlüsselbild, die Geste der Königin im sechsten; beide erreichen diesen Punkt exakt bei Tick 24. Die Spielvorgabe bleibt: Der ganze Saal wird gleichzeitig getroffen, der Held stirbt sofort, weder Sprung, Rolle noch Amulett-Schild helfen. Nur das erzählerische Zögern (G8), bei dem keine Entladung stattfindet, verhindert diesen Angriff. Die Stärke entsteht durch räumliche Ausdehnung, Wurzeln, Trümmer und Nachbeben; kein voller weißer Bildschirmblitz.

## Dateien und Stand

Pro Clip: source-sheet.png, acht transparente Einzelbilder 00.png–07.png, sheet.png, animation.json, preview.gif. Die GIFs haben nur für die Vorschau eine zusätzliche Schluss-Pause. PNGs enthalten echte Alpha-Transparenz. pack_previews.py verpackt die eingeschlossenen Quellbilder ohne Neuzeichnen oder Skalieren. Im vorgesehenen leeren Schlussbild der Ranken werden unsichtbare Alpha-1-Reste auf exakt null gesetzt; das Quell-Sheet bleibt unverändert. verify_exports.py prüft Rechtecke, Timing und vollständig transparente Schlussbilder der Ranken.

Noch Arbeitsauflösung 960 × 720 pro Bild, weiche Randpixel und mehr als 32 Farben. Für native PSP-Sprites fehlen feste Paletten, Pixelüberarbeitung, Zwischenbilder und kleine Atlanten. Stufe-3-Flügel sind noch nicht vom Körper getrennt. Der saalweite Effekt muss für 480 × 272 separat ausgearbeitet werden; die große Arbeitsfläche ist kein PSP-Atlas. attack_spec.json dokumentiert eine Designvorgabe, keine eingebundene Engine-Konfiguration. Die Änderungen betreffen Grafikentwürfe und Konzeptdokumentation; sie ändern keine Spiellogik.
