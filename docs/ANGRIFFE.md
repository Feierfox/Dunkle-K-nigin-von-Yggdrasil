# Angriffe der Königin

Entwurf vom 09.10.2026. Grundlage: [SPIELKONZEPT.md](SPIELKONZEPT.md), [VISUAL_KOENIGIN.md](VISUAL_KOENIGIN.md).

## Festgelegte Regeln

- **Jeder Angriff hat ein Zeitfenster zum Reagieren.** Zwischen dem ersten sichtbaren Signal und dem Treffer liegt immer genug Zeit, dass der Held ausweichen kann, wenn er das Muster kennt.
- **Der Held weicht auf zwei Arten aus:** mit einer **Ausweichrolle** (kurz unverwundbar, bewegt ihn ein Stück zur Seite) oder mit einem **Sprung** (über bodennahe Angriffe).
- **Flächenschaden markiert vorher den Boden.** Wo eine Markierung leuchtet, schlägt es gleich ein.
- **Während des Kampfes wird nicht gesprochen.** Nur Verwandlungen und das Zögern beim Weltgericht unterbrechen den Kampf.
- Die Werte der Königin bleiben immer gleich (siehe [SPIELKONZEPT.md](SPIELKONZEPT.md)).

Alle Zeiten in **Animationsbildern zu 12 Bildern pro Sekunde** (1 Bild ≈ 83 ms). Die Spiellogik zählt intern in 60er-Schritten (1 Animationsbild = 5 Logikbilder). Werte sind Vorschläge und werden beim Testen abgestimmt.

## Überblick

| Phase | Angriff | Taste | Signal | Reaktionsfenster | Treffer | Ausweichen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Richtschlag | □ | Sense hebt sich über den Kopf | 5 Bilder (0,42 s) | vorn, Nahbereich | Rolle |
| 1 | Sensenzug | △ | Blatt wird nach vorn geworfen | 6 Bilder (0,5 s) | beim Zurückziehen, bodennah, weit | Sprung |
| 1 | Kreisschnitt | ○ | Sense waagerecht, sie dreht sich ein | 5 Bilder (0,42 s) | beidseitig, Brusthöhe, Nahbereich | Rolle aus der Reichweite |
| 2 | Sternschauer | □ | Leuchtende Kreise am Boden | 8 Bilder (0,67 s) | auf den Kreisen | Rolle zwischen die Kreise |
| 2 | Windklinge | △ | Sense holt waagerecht aus, Klinge glüht | 5 Bilder (0,42 s) | Sichel über den ganzen Boden, bodennah | Sprung |
| 2 | Todesurteil | ○ | Rune erscheint unter dem Helden | 10 Bilder (0,83 s) | ganze Runenfläche | Rolle aus der Rune |
| 3 | Ranken | □ | Risse im Boden leuchten nacheinander | je 8 Bilder (0,67 s) | an den Rissen, nacheinander | Rolle über freie Stellen |
| 3 | Erinnerungsriss | △ | Riss in der Luft öffnet sich | 6 Bilder (0,5 s) | Welle in Brusthöhe über den Saal | Rolle unter der Welle |
| 3 | Weltgericht | L + R | Saal verdunkelt sich, Lichtkugel wächst | 24 Bilder (2 s) | ganzer Saal | kein Schutz, nur das Zögern (G8) |

Die Tasten sind ein Vorschlag auf Grundlage von [PSP1000.md](PSP1000.md). In jeder Phase liegen die drei Angriffe auf denselben Tasten, damit der Spieler nicht umlernen muss.

## Phase 1 — Schwertarbeit mit der Sense (rote Leiste)

### Richtschlag (□)

| Bilder | Ablauf |
| --- | --- |
| 1 | Ruhe |
| 2–5 | **Signal:** Arm hebt sich, Sense kippt hinter den Kopf |
| 6–7 | **Treffer:** Blatt fährt vor ihr in den Boden, Reichweite 0–40 px vor ihr |
| 8–10 | Erholung, Blatt wird aus dem Boden gezogen. **Lücke für den Helden** |

Lernkurve: Zu frühes Rollen landet in Bild 5 noch vor ihr. Richtig ist die Rolle in Bild 5, durch sie hindurch oder nach hinten.

### Sensenzug (△)

| Bilder | Ablauf |
| --- | --- |
| 1–2 | Ausfallschritt |
| 3–6 | **Signal:** Sie wirft das Blatt weit nach vorn, bodennah. Der Wurf selbst trifft nicht |
| 7–9 | **Treffer beim Zurückziehen:** Das Blatt fährt bodennah zu ihr zurück, Reichweite 20–90 px |
| 10–14 | Erholung |

Lernkurve: Der Held weicht anfangs dem Wurf aus und wird vom Rückweg getroffen („Ich bin dem Wurf ausgewichen. Dem Rückweg nicht.“). Richtig ist der Sprung in Bild 7.

### Kreisschnitt (○)

| Bilder | Ablauf |
| --- | --- |
| 1–5 | **Signal:** Sense waagerecht, Oberkörper dreht sich ein |
| 6–9 | **Treffer:** volle Drehung, Reichweite 50 px auf beiden Seiten, Brusthöhe |
| 10–14 | Erholung, leicht taumelnd. **Lücke für den Helden** |

Lernkurve: Nah dran bleiben ist tödlich. Richtig ist die Rolle aus der Reichweite in Bild 4–5 und danach der Gegenangriff in der Erholung.

## Phase 2 — Magie mit Flächenschaden (orange Leiste)

### Sternschauer (□)

- **Signal:** 3–5 leuchtende Kreise (je 24 px) erscheinen am Boden, einer immer dort, wo der Held steht.
- **Reaktionsfenster:** 8 Bilder.
- **Treffer:** Geschosse fallen auf alle Kreise gleichzeitig.
- **Ausweichen:** Rolle in eine Lücke zwischen den Kreisen.

### Windklinge (△)

- **Signal:** Waagerechtes Ausholen, das Sensenblatt glüht türkis (5 Bilder).
- **Treffer:** Eine Sichel aus Licht fliegt bodennah über den ganzen Boden, in Richtung des Helden.
- **Ausweichen:** Sprung. Eine Rolle reicht nicht, die Sichel ist breiter als die Rolle.

### Todesurteil (○)

- **Signal:** Sie zeigt auf den Helden, eine Rune (48 px breit) leuchtet unter ihm auf.
- **Reaktionsfenster:** 10 Bilder, das längste in Phase 2.
- **Treffer:** Die Sense schlägt nach unten, die ganze Runenfläche wird getroffen.
- **Ausweichen:** Rolle aus der Rune. Ein Sprung landet wieder in ihr.

## Phase 3 — Die Wurzelgestalt (lila Leiste)

### Ranken (□)

- **Signal:** 3–4 Risse im Boden leuchten **nacheinander** auf, jeweils 8 Bilder vor dem Durchbruch.
- **Treffer:** An jedem Riss bricht eine Wurzel senkrecht aus dem Boden.
- **Grafik-Assets:** Zwei unabhängig platzierbare Varianten: hohe Dornenranke und breite Hakenranke. Beide brechen aus ihrer Bodenstelle hervor, halten die aktive Schadensfläche kurz und ziehen sich anschließend vollständig in dieselbe Stelle zurück. Beim Rückzug endet die Schadensphase; das Schlussbild ist transparent. Entwürfe: [Bodenranken v2](../assets/animationen/ranken-weltgericht-v2/README.md).
- **Ausweichen:** Rolle über die Stellen, die schon durchgebrochen sind oder noch nicht leuchten. Der Rhythmus muss gelernt werden.

### Erinnerungsriss (△)

- **Signal:** Mit einer Hand öffnet sie einen Riss in der Luft, Bilder vergangener Reiche flackern darin (6 Bilder).
- **Treffer:** Eine Welle in **Brusthöhe** zieht über den ganzen Saal.
- **Ausweichen:** Rolle *unter* der Welle hindurch. Wer springt, springt hinein.

### Weltgericht (L + R)

- **Signal:** Der Saal verdunkelt sich, die Flügel öffnen sich maximal, eine Lichtkugel wächst (24 Bilder).
- **Treffer:** Der ganze Saal.
- **Inszenierung:** Die Entladung erfasst gleichzeitig beide Seiten sowie die ganze Höhe des Saals. Wurzeln brechen an mehreren Stellen hervor, ein eisblau-türkises Lichtgitter durchzieht den Raum, Steintrümmer und Nachbeben folgen. Keine kleine, ausweichbare Sichelwelle und keine freie Schutzzone. Königin und saalweiter Effekt sind getrennte Assets; ihre Entladung beginnt nach denselben 24 Aufladebildern. [Weltgericht v2](../assets/animationen/ranken-weltgericht-v2/README.md).
- **Ausweichen:** Nicht möglich. Auch der Amulett-Schild hält es nicht auf; der Held stirbt, sobald es entladen wird. Seine einzige Chance ist, dass sie zögert (G8).
- **Abklingzeit:** einmal pro Versuch, frühestens 20 Sekunden nach Beginn von Phase 3. Ab Runde 25 kann hier das Zögern (G8) eintreten.

## Phasenwechsel-Impulse

| Wechsel | Signal | Treffer | Gegenmaßnahme |
| --- | --- | --- | --- |
| 1 → 2 | Licht sammelt sich in ihrer Brust (4 Bilder) | Ringwelle über den Boden | **Sprung** im richtigen Moment |
| 2 → 3 | Flügel öffnen sich vollständig (8 Bilder) | Lila Nebel flutet den Bildschirm | **Amulett-Schild** (ab Stufe 4) |

## Lernen des Helden

Der Held lernt für jeden Angriff einzeln. **Vorschlag** (passt zu [PSP1000.md](PSP1000.md)): Pro Angriff führt das Spiel zwei kleine Zähler, „erlebt“ und „getroffen“.

| Lernstand | Verhalten |
| --- | --- |
| Neu (0–2 Mal erlebt) | Reagiert gar nicht oder falsch (rollt beim Sensenzug statt zu springen) |
| Lernend (3–5 Mal) | Reagiert richtig, aber mit falschem Timing, meist zu früh |
| Sicher (ab 6 Mal) | Weicht im richtigen Bild aus und nutzt die Erholungslücke für einen Gegenangriff |

**Umsetzung (10.10.2026):** Getroffen 0 Mal: keine Reaktion; 1–2 Mal: falsche Ausweichart; ab 3 Mal: richtige Ausweichart im richtigen Bild. Nach jedem Angriff hat die Königin eine **Erholungslücke** von 40 Logikschritten (etwa 0,7 s), in der sie still steht. Beherrscht er den Angriff (ab 3 Mal getroffen), eilt er heran und schlägt in dieser Lücke immer zu; die Lücke endet erst nach seinem Hieb, höchstens nach 2,5 s. Gewöhnliche Hiebe kommen in festem Abstand statt zufällig. Steckt er 9 Versuche ohne neue Phase fest, wird sein Hieb stufenweise stärker (4, 6, 8, 10, höchstens 12 Schaden je Treffer bei 60 je Leiste).

Daraus ergibt sich das festgelegte Tempo: in jeder Phase mindestens 3 Runden leicht zu besiegen, danach mindestens 6 weitere bis zur nächsten Phase. **Neue Ausrüstung macht ihn widerstandsfähiger, aber nicht sofort siegreich**: Er hält mehr Treffer aus, muss die Muster aber trotzdem lernen.
