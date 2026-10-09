# Musik und Ton

Entwurf vom 09.10.2026.

## Festgelegt

- Es gibt ein **Hauptthema**, **Soundeffekte** und eine **Bosskampf-Musik, die sich dynamisch an die Phasen anpasst**.
- **Sobald der Held tot ist, herrscht Stille.**

## Musikstücke

| Stück | Wann | Stimmung |
| --- | --- | --- |
| **Hauptthema** | Titelbild, Menü, Abspann | Langsam, feierlich, melancholisch. Orgel oder Chor mit tiefen Streichern, eine einfache Melodie, die später im Kampf wiederkehrt |
| **Audienz** | Phase 0, Gespräche | Sehr leise, gehaltene Töne, das Thema nur angedeutet |
| **Kampf Phase 1** | rote Leiste | Schwer und gemessen: tiefe Streicher, Pauken im Schrittrhythmus der Königin |
| **Kampf Phase 2** | orange Leiste | Dasselbe Thema, schneller und dichter, dazu ein Chor. Türkise Magie klingt gläsern (Celesta, Glocken) |
| **Kampf Phase 3** | lila Leiste | Volles Thema, Chor und Orgel. Darunter ein verzerrter, tiefer Ton für die Verderbnis |
| **Enden** | je Ende | Eigene kurze Fassungen des Themas; E1 und E2 enden in Stille bzw. im Verderbnis-Ton |

## Dynamik im Kampf

- **Phasenwechsel:** Die Musik bricht bei Beginn der Verwandlung ab. Während der Verwandlung läuft ein **Übergangsstück**, das genau so lang ist wie die Animation (etwa 4 bzw. 8 Sekunden, gekürzte Fassung bei Wiederholung). Mit dem Impuls setzt die Musik der nächsten Phase ein.
- **Kampfverlauf:** Innerhalb einer Phase kann eine zweite, dichtere Fassung einsetzen, wenn die Leiste unter die Hälfte fällt. Der Wechsel passiert am Taktende.
- **Zögern beim Weltgericht (G8):** Die Musik dünnt auf einen gehaltenen Ton aus.
- **Tod des Helden: sofort Stille.** Kein Ausblenden, kein Nachhall der Musik. Hörbar bleiben nur die Schritte der Königin und die Geräusche des Totenrituals (Vorschlag, sehr leise).
- **Rückkehr des Helden:** Die Musik setzt erst wieder ein, wenn er den Saal betritt, je nach Lage mit „Audienz“ oder direkt mit der Kampfmusik von Phase 1.
- **Abwesenheit des Helden:** ebenfalls Stille. Es geschieht bewusst nichts, auch musikalisch nicht.

## Soundeffekte

| Gruppe | Effekte |
| --- | --- |
| Königin | Schritte (schwer, Metall auf Stein), Schweben (leises Summen), Sense ausholen, Sense trifft Boden, Sense zieht durch die Luft, Treffer an ihr (dumpf, kaum Reaktion) |
| Angriffe Phase 2 | Bodenkreise erscheinen, Sternschauer schlägt ein, Windklinge, Rune leuchtet auf, Rune schlägt ein |
| Angriffe Phase 3 | Risse im Boden, Wurzeln brechen durch, Riss in der Luft (verzerrte Stimmen), Weltgericht aufladen, Weltgericht entladen |
| Verwandlung | Helm reißt (Glas und Holz), Helm zerfällt, Impuls Phase 2 (Ringwelle), Impuls Phase 3 (Nebel rauscht heran) |
| Held | Schritte (Leder), Rolle, Sprung, Landung, Schwerthieb, Treffer an ihm, Tod (kurz, dann Stille), Amulett-Schild (heller Glockenton) |
| Totenritual | Feuer (eisblau, knisternd und kalt), Umarmen (Stoffrascheln, sonst nichts), Portal (tiefes Saugen, Wurzeln knarren) |
| Oberfläche | Textbox öffnet sich, Auswahl wechseln, Auswahl bestätigen. Für Sätze der Verderbnis ein eigenes, verzerrtes Textgeräusch |

## Umsetzung auf der PSP-1000

- **Musik** als ATRAC3plus oder MP3 vom Memory Stick streamen. Die PSP decodiert beides mit eigener Hardware (Media Engine), die Hauptrechenzeit bleibt frei.
- **Phasenmusik** als getrennte Schleifen pro Phase plus Übergangsstücke. Das ist einfacher und sparsamer als mehrere gleichzeitig laufende Spuren.
- **Soundeffekte** als kurze PCM-Dateien (22 kHz, mono), dauerhaft im Speicher, über die Kanäle der PSP gemischt. Speicherbudget: siehe „Ton und Musik“ in [PSP1000.md](PSP1000.md).
- **Stille beim Tod:** Musikkanal sofort stoppen, nicht ausblenden.

## Offen

- Komponist bzw. Herkunft der Musik und Lizenz.
- Länge der Schleifen pro Phase.
- Ob die Königin eine Stimme bekommt oder nur Text (bisher: nur Text).
