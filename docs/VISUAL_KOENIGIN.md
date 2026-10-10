# Visuelles Designdokument — Die Königin

Sprite-Spezifikation der Königin für den Pixel-Artist. Grundlage ist ein eingereichter Vorschlag vom 09.10.2026, angepasst an die festgelegten Entscheidungen und an die Grenzen der PSP-1000.

**Verbindlich** sind: das Aussehen nach den Entwürfen [v5](../assets/konzept/koenigin-idle-sense-helm-v5.webp) (Phase 0/1, **Sense** und **geschlossener Helm mit Krone**) und [Phase 2](../assets/konzept/koenigin-p2-helmbruch-v1.webp), der gerissene Helm ab Phase 2, **das Gesicht erst ab Phase 3**, die drei Kampfphasen mit den Lebensleisten Rot, Orange und Lila, der magische Impuls bei jedem Phasenwechsel, das Verhalten des Helden während der Verwandlung und das Kampftempo. Alles andere, also Angriffsnamen, Bildzahlen, Paletten der Phasen 2 und 3 und Effekte, ist ein **Vorschlag**.

## Eckdaten

| Punkt | Vorgabe |
| --- | --- |
| Software | Aseprite (empfohlen) |
| Bildschirm | 480 × 272 Pixel (PSP-1000) |
| Sprite Phase 0–2 | 64 × 96 Pixel; Angriffe mit der Sense 96 × 96, weil das Sensenblatt weit ausholt |
| Sprite Phase 3 | 80 × 112 Pixel Körper, Flügel als eigene Ebene (gesamt etwa 160 × 112) |
| Farbmodus | Indiziert, eine Palette pro Phase, höchstens 32 genutzte Farben |
| Animationen | 12 Bilder pro Sekunde. Die Spiellogik läuft mit 60 Bildern pro Sekunde, ein Animationsbild steht also 5 Logikbilder lang |
| Ausrichtung | Blick nach links; für Blick nach rechts wird das Sprite im Spiel gespiegelt |

Ein Bildkonzept in echter PSP-Auflösung liegt in [assets/konzept/psp/](../assets/README.md#psp-bildkonzept).

## Phasenübersicht

| | Phase 0 | Phase 1 | Phase 2 | Phase 3 |
| --- | --- | --- | --- | --- |
| Name | Die Thronende | Die Kämpfende | Die Erwachte | Die Wurzelgestalt |
| Lebensleiste | – | **Rot** | **Orange** | **Lila** |
| Zustand | Intro, Dialoge, Warten, Abwesenheit des Helden | Kampf | Kampf | Kampf |
| Bewegung | Sitzt auf dem Thron | Schreitet, läuft | Gleitet, 5 px über dem Boden | Schwebt, 20 px über dem Boden |
| Aussehen | Wie Entwurf v5 | Wie Phase 0 | **Helm gerissen, aber geschlossen**, Gesicht weiter verborgen, Augen leuchten türkis-weiß, Risse auf der Rüstung leuchten türkis, verdorbene Wurzeln aus den Helmrissen | **Helm zerfallen, Gesicht sichtbar**, Teile der Rüstung zu Wurzelholz, Flügel aus Wurzeln |
| Sense | In der Hand | In der Hand | Wurzeln umschlingen den Unterarm | Mit dem Arm verschmolzen, Stielwurzeln gehen in die Flügel über |
| Aura | Keine | Keine | Wenige eisblaue Partikel | Blätter, Licht, Wurzeln im Saal |
| Angriffe | – | 3 Sensenangriffe | 3 magische Angriffe mit Flächenschaden | 3 Wurzel- und Erinnerungsangriffe mit Flächenschaden |
| Sprite | 64 × 96 | 64 × 96 | 64 × 96 | 80 × 112 + Flügel |
| Thronsaal | Normal | Normal | Fackeln brennen türkis | Boden bricht auf, Wurzeln leuchten, Decke zeigt Risse |

Die Farben der Magie folgen [KOENIGIN.md](KOENIGIN.md): **Eisblau und Türkis**. Lila bleibt der Lebensleiste von Phase 3 und den Kristallen vorbehalten, damit sich Effekte vom dunkelvioletten Saal abheben. Die **Verderbnis** Yggdrasils erscheint als schwarze Wurzeln mit **magentafarbenen Adern** und bleibt so von ihrer eigenen Magie unterscheidbar. Die Krone bleibt in allen Phasen aus schwarzen Ästen; in Phase 2 sitzt sie auf dem gerissenen Helm, in Phase 3 trägt sie sie direkt über dem freigelegten Gesicht, und es wachsen ihr Blätter.

## Kampftempo

**Festgelegt:**

- Die Phasen wechseln im Kampf, sobald eine Lebensleiste leer ist.
- In jeder Phase ist der Held **mindestens 3 Runden lang leicht zu besiegen**.
- Danach braucht er **mindestens 6 weitere Runden**, bis er die nächste Phase erreichen kann. Wie schnell das geht, hängt davon ab, wie gut der Spieler die Königin spielt.

Daraus ergibt sich als frühester Verlauf:

| Abschnitt | Frühestens ab Runde |
| --- | --- |
| Held erreicht Phase 2 | 10 |
| Held erreicht Phase 3 | 19 |
| Held kann die Königin besiegen | etwa 28 (Vorschlag, gleiches Muster) |

Jeder neue Versuch beginnt wieder in Phase 1 mit vollen Leisten. Der Held muss frühere Phasen also jedes Mal erneut überstehen, wird darin aber immer schneller.

## Phasenwechsel und magischer Impuls

**Festgelegt:**

- Während der Verwandlung **greift der Held nicht an und bleibt stehen**.
- Jede Verwandlung endet mit dem **magischen Impuls**. Trifft er den Helden, stirbt dieser sofort, unabhängig von seinen Herzen.
- Der Held überlebt den Impuls erst, wenn er ihm begegnen kann. **Festgelegt:**
  1. **Impuls beim Wechsel zu Phase 2: Sprung.** Er erkennt das Signal und springt im richtigen Moment über die Welle. Das lernt er, dafür braucht er keine Ausrüstung.
  2. **Impuls beim Wechsel zu Phase 3: Amulett-Schild.** Beim ersten Mal versucht der Held zu springen und stirbt im Nebel; danach holt er in einer eigenen Quest das Amulett ([SPIELKONZEPT.md](SPIELKONZEPT.md#die-amulett-quest)). Das Amulett erzeugt einen Schild, der ihn golden leuchten lässt. **Lila Nebel flutet den ganzen Bildschirm**, nur der Bereich, in dem der Held steht, bleibt frei, geschützt vom Schild. Ohne Amulett stirbt er im Nebel.

Mockup: [mockup-impuls2-amulett-2x.png](../assets/konzept/psp/mockup-impuls2-amulett-2x.png).

**Vorschlag zur Dauer:** Beim ersten Mal läuft die volle Sequenz (1→2 etwa 4 Sekunden, 2→3 etwa 8 Sekunden). Bei späteren Versuchen wird sie gekürzt (etwa 2 und 3 Sekunden), damit Wiederholungen flüssig bleiben. Der Impuls selbst bleibt immer gleich lang, damit der Held ihn lernen kann.

## Phase 0 — Die Thronende

Die Königin sitzt auf ihrem Thron, das Gesicht hinter dem geschlossenen Helm, nur die türkisen Augen im Sehschlitz. Die Sense lehnt an der Armlehne. Kalt, ruhig, erhaben. Nur der Atem und gelegentlich ein Tippen der Finger auf der Armlehne. Keine Magie, keine Aura. Ihre Existenz ist die Drohung.

Phase 0 zeigt sie auch in der Szene, in der der Held auf Quest ist und **bewusst nichts geschieht**.

| Animation | Bilder | Schleife | Beschreibung |
| --- | --- | --- | --- |
| p0_idle | 8 | ja | Langsamer Atem: Brust 1 px hoch in Bild 2–4, zurück in Bild 5–8. Mantel minimal bewegt |
| p0_finger_tap | 12 | selten | Rechte Hand tippt auf die Armlehne, etwa alle 8 Sekunden |
| p0_head_turn | 6 | nein | Kopf dreht sich leicht, wenn der Held eintritt |
| p0_dialog_talk | 4 | ja | Kleine Geste während eines Dialogs |

Pixel-Art kennt keine halben Pixel: Atembewegungen sind 1 px groß oder entstehen durch einen Wechsel der Schattenfarbe.

**Ebenen in Aseprite** (von unten nach oben): CAPE_BACK, SCYTHE_BACK, BODY_BASE, ARMOR_DETAIL, ARMOR_SHINE, HANDS, HEAD (Gesicht, erst für Phase 3), HAIR, HELMET, CROWN, SCYTHE_FRONT, CAPE_FRONT. Helm und Sense liegen auf eigenen Ebenen, damit Helmbruch und Verschmelzung getrennt animiert werden können. Der Thron gehört zum Hintergrund, nicht zum Sprite.

## Phase 1 — Die Kämpfende (rote Leiste)

Die Königin erhebt sich und betritt das Kampffeld. Schwer, kraftvoll, beherrschend. Gleiche Farben wie Phase 0, keine Aura, keine Magie. Ihre Waffe ist die **Sense**.

### Angriffe — Vorschlag

Die drei Angriffe aus dem ursprünglichen Vorschlag (Thronschlag mit der Faust, Schattengreifer, Dunkelring) wurden zu Sensenangriffen umgebaut. So bleiben sie erkennbar und nutzen die Form der Sense:

| Angriff | Bilder | Wirkung | Treffer aktiv |
| --- | --- | --- | --- |
| **Richtschlag** | 10 | Sense hoch über den Kopf, das Blatt fährt in einem Bogen vor ihr in den Boden. Kurze Reichweite, viel Wucht | Bild 6–7 |
| **Sensenzug** | 14 | Sie wirft das Blatt weit nach vorn und zieht es zurück. Getroffen wird erst beim **Zurückziehen**; die Verzögerung muss der Held lernen | Bild 9–11 |
| **Kreisschnitt** | 14 | Sie dreht die Sense einmal um sich selbst, das Blatt trifft auf beiden Seiten. Nur Nahbereich, kein Flächenschaden | Bild 8–10 |

Jeder Angriff beginnt mit einer deutlichen **Ausholbewegung ohne Trefferzone**. Daran lernt der Held.

Beispiel Richtschlag:

```
Bild 1–3:  Sense hebt sich über den Kopf (Warnung)
Bild 4–5:  Höchster Punkt, kurzes Halten
Bild 6–7:  TREFFER AKTIV, das Blatt schlägt in den Boden
Bild 8–10: Erholung, Blatt wird aus dem Boden gezogen, zurück in Kampfhaltung
```

### Animationen

| Animation | Bilder | Schleife | Beschreibung |
| --- | --- | --- | --- |
| p1_idle | 6 | ja | Aufrecht, minimale Atembewegung, Mantel weht |
| p1_walk | 8 | ja | Schwerer Schritt, Schulterplatten wippen gegenläufig, Mantel folgt 2 Bilder verzögert |
| p1_run | 8 | ja | Schneller Schritt, Mantel fliegt hinter ihr |
| p1_turn | 4 | nein | Dreht sich zum Helden |
| p1_atk_richtschlag | 10 | nein | Siehe oben |
| p1_atk_sensenzug | 14 | nein | Siehe oben |
| p1_atk_kreisschnitt | 14 | nein | Siehe oben |
| p1_hit | 4 | nein | Leichtes Zurückweichen, kaum sichtbar |
| p1_recover | 3 | nein | Zurück in Kampfhaltung |

### Bewegungsbereich

Königin und Held stehen **mittig und hinten** im Saal, also am hinteren Rand des Bodens und nicht am unteren Bildrand. So bleiben Thron, Eingang und die Veränderungen des Saals in den Phasen 2 und 3 sichtbar, und vor den Figuren bleibt Boden frei für Spiegelungen, Runen und Wurzeln.

```
Bildschirm 480 × 272
Kampflinie:  Füße bei Y ≈ 240 (hinterer Rand des Bodens)
Königin:     X 140–380
Held:        X 80–400
Vor der Kampflinie (Y 240–272): Spiegelungen, Bodenrunen, aufbrechende Wurzeln, Herzanzeige
Die Königin folgt dem Helden langsam, nicht 1:1.
Angriffe richten sich immer zum Helden aus.
Nach einem Angriff bleibt sie für die Erholungsbilder stehen.
```

Schwebehöhen (Phase 2: 5 px, Phase 3: 20 px) werden von dieser Kampflinie aus gemessen.

## Verwandlung 0 → 1 — Das Aufstehen

Etwa 2 Sekunden (24 Bilder). Auslöser: Der Held betritt den Saal. **Kein Impuls**, da noch keine Phase wechselt.

```
Bild 1–4:   Fingertippen hört auf, Hände auf den Armlehnen
Bild 5–8:   Oberkörper lehnt sich nach vorn
Bild 9–12:  Sie erhebt sich
Bild 13–16: Steht aufrecht, kurze Pause
Bild 17–20: Schulterplatten setzen sich, Mantel fällt neu
Bild 21–24: Greift die Sense und nimmt Kampfhaltung ein
→ p1_idle
```

## Verwandlung 1 → 2 — Der Helm reißt (rote Leiste leer)

Etwa 4 Sekunden (48 Bilder). Der Held steht still. **Wendepunkt der Geschichte:** Im Helm wohnt der verdorbene Teil Yggdrasils (siehe [KOENIGIN.md](KOENIGIN.md#der-verdorbene-yggdrasil--wendepunkt)).

```
Bild 1–8:   Krone pulsiert, Kristalle leuchten magenta. Sie greift sich mit der freien Hand an den Helm
Bild 9–16:  Erste Risse laufen über den Helm, magentafarbenes Licht dringt heraus
Bild 17–24: Die Risse werden breiter, kleine Splitter fallen ab, der Helm bleibt aber geschlossen.
            Die Augen im Sehschlitz leuchten heller, türkis-weiß
Bild 25–32: Schwarze Wurzeln mit magentafarbenen Adern wachsen aus den Helmrissen;
            feine Risse auf Rüstung und Haut leuchten türkis auf
Bild 33–40: Wurzeln aus dem Sensenstiel umschlingen ihren Unterarm.
            Sie hebt 5 px vom Boden ab, der Mantel weht nach oben
Bild 41–44: Sammeln: Licht zieht sich in ihrer Brust zusammen
Bild 45–48: IMPULS: Ring aus eisblauem Licht mit magentafarbenem Rand breitet sich über den Saal aus
→ p2_idle
```

**Wenn der Helm zum ersten Mal reißt,** folgt nach dem Impuls ein kurzer Erkenntnismoment (Dialog oder Kommentar des Helden). Bei späteren Versuchen läuft nur die gekürzte Verwandlung.

Thronsaal: Die Fackeln wechseln von Orange zu Türkis (eigene Hintergrundebene).

## Phase 2 — Die Erwachte (orange Leiste)

Sie gleitet, statt zu laufen. Der Mantel weht magisch nach oben und hinten. Der Helm ist gerissen, aber noch geschlossen; ihr Gesicht bleibt verborgen. Aus den Rissen wachsen verdorbene Wurzeln. Die Risse ihres Körpers leuchten türkis; das ist der Preis ihrer Magie (siehe [KOENIGIN.md](KOENIGIN.md)). Sense und Unterarm sind durch Wurzeln verbunden.

### Angriffe — Vorschlag, mit Flächenschaden

| Angriff | Bilder | Wirkung |
| --- | --- | --- |
| **Sternschauer** | 20 | Beide Arme heben sich, Licht sammelt sich. Geschosse fallen auf mehrere markierte Stellen des Bodens |
| **Windklinge** | 14 | Waagerechter Sensenhieb, eine Sichel aus Licht in der Form des Sensenblatts fliegt über den ganzen Boden. Der Held muss springen |
| **Todesurteil** | 8 + 12 | Sie zeigt auf den Boden, eine Rune erscheint unter dem Helden. Kurz darauf schlägt sie zu, die ganze Runenfläche wird getroffen |

### Animationen

| Animation | Bilder | Schleife | Beschreibung |
| --- | --- | --- | --- |
| p2_idle | 10 | ja | Schwebt ±3 px. Risse pulsieren 2 Bilder hell, 2 Bilder dunkel |
| p2_glide | 8 | ja | Gleitet ohne Schritte, Füße 5 px über dem Boden |
| p2_atk_sternschauer | 20 | nein | Siehe oben |
| p2_atk_windklinge | 14 | nein | Siehe oben |
| p2_atk_todesurteil_mark | 8 | nein | Zeigefinger senkt sich, Rune erscheint |
| p2_atk_todesurteil_hit | 12 | nein | Sense fährt nach unten, Einschlag |
| p2_hit | 4 | nein | Kurzes Zurückgleiten, weniger Reaktion als in Phase 1 |

### Effekte

- **Leuchtende Risse:** eigene Ebene über der Rüstung, 1 px breite türkise Linien, im Wechsel hell und dunkel.
- **Augen:** 2 × 1 px türkis-weiß, ohne Pupille, mit 1 px schwachem Schein.
- **Verdorbene Wurzeln:** wenige schwarze Ranken an den Helmrissen, magentafarbene Adern pulsieren langsamer als die türkisen Risse.
- **Partikel:** 6–8 eisblaue Punkte (1 × 1 oder 2 × 2 px) auf langsamen Kreisbahnen, 6–10 Sekunden pro Umlauf.

## Verwandlung 2 → 3 — Die Wurzelgestalt erwacht (orange Leiste leer)

Etwa 8 Sekunden (96 Bilder). Der Held steht still.

```
Bild 1–12:  Der Boden bebt (Hintergrund ±2 px)
Bild 13–24: Wurzeln Yggdrasils brechen durch den Boden, Steinsplitter fliegen
Bild 25–36: Sie hebt die Arme, Wurzeln winden sich um sie. Wechsel zur Palette von Phase 3.
            Sprite wächst von 64 auf 80 px Breite
Bild 37–48: Der Helm zerfällt in Splitter und gibt zum ersten Mal ihr dunkles Gesicht frei;
            die Krone bleibt über ihrem Kopf. Teile der Rüstung verhärten zu dunklem Wurzelholz.
            Die Sense verschmilzt mit ihrem Arm, das Blatt wächst aus dem Unterarm
            Der Krone wachsen neue Äste und Blätter
Bild 49–60: Flügel aus verschlungenen Wurzeln wachsen aus den Schultern; die Wurzeln des Sensenstiels gehen in sie über
Bild 61–72: Sprite wächst von 96 auf 112 px Höhe, sie schwebt 20 px über dem Boden
Bild 73–84: Blätter leuchten auf, Licht dringt aus den Rissen
Bild 85–92: Sammeln: Die Flügel öffnen sich vollständig
Bild 93–96: IMPULS: Lila Nebel flutet den ganzen Bildschirm. Nur der Schild des Helden (falls er das Amulett trägt)
            bleibt als goldene Blase frei
→ p3_idle
```

Thronsaal: Neue Hintergrundebenen werden aktiv. Die Decke zeigt Risse, dahinter Nachthimmel; die Wurzeln im Boden leuchten.

## Phase 3 — Die Wurzelgestalt (lila Leiste)

Die Königin ist zur Verkörperung ihrer Bindung an Yggdrasil geworden. Halb Königin, halb Baum. Sie schwebt frei. Flügel aus Wurzeln und Licht tragen sie. Je stärker sie eingreift, desto mehr wird sie Teil des Baums. Das ist auch erzählerisch wichtig (siehe [KOENIGIN.md](KOENIGIN.md)).

### Flügel

- Drei asymmetrische Ausläufer pro Seite, von der Schulter nach hinten oben.
- Innen verschlungene dunkle Wurzeln, Außenkante türkis leuchtend, 8–12 Blätter (2 × 3 oder 3 × 4 px), von denen einzelne aufleuchten und abfallen.
- Je Flügel etwa 40 × 60 px, gesamt etwa 160 × 112 px.
- **Eigene Ebene und eigener Export**, damit Flügel und Körper unabhängig animiert werden.

### Angriffe — Vorschlag, mit Flächenschaden

| Angriff | Bilder | Wirkung |
| --- | --- | --- |
| **Ranken** | 28 | Arme nach unten, Wurzeln brechen an mehreren angekündigten Stellen aus dem Boden |
| **Erinnerungsriss** | 18 | Eine Hand öffnet einen Riss in der Luft, Bilder vergangener Reiche strömen als Welle hervor |
| **Weltgericht** | 24 + 24 | Großer Angriff über den ganzen Saal (siehe unten) |

### Weltgericht

```
Aufladen (24 Bilder, 2 Sekunden):
Bild 1–4:   Arme heben sich langsam
Bild 5–8:   Flügel öffnen sich maximal, Saal beginnt sich zu verdunkeln
Bild 9–16:  Lichtkugel zwischen den Händen wächst auf 16 px
Bild 17–20: Kugel pulsiert, Krone leuchtet maximal
Bild 21–24: Stille vor der Entladung

Entladung (24 Bilder):
Bild 1–4:   Hände stoßen nach vorn
Bild 5–8:   Welle breitet sich aus, Bild hellt kurz auf
Bild 9–16:  Helligkeit klingt ab, neue Risse im Saal
Bild 17–24: Sie sinkt 1–2 px ab, Flügel hängen kurz, dann zurück zu p3_idle
```

Kein Schutz hält das Weltgericht auf, auch nicht der Amulett-Schild, der beim Impuls zu Phase 3 noch hilft. Der Held übersteht es nur, wenn sie zögert (G8).

**Helligkeit:** Kein voller weißer Blitz. Die Aufhellung bleibt bei höchstens etwa 50 % Deckkraft und dauert länger als 2 Animationsbilder. Das ist angenehmer und verträglicher für lichtempfindliche Spieler.

**Zögern** (8 Bilder): Wie das Aufladen, aber in Bild 21 zittern ihre Hände, die Flügel falten sich, das Licht erlischt. Kein Angriff, stattdessen beginnt ein Dialog. **Vorschlag:** Dieser Moment hängt von früheren Gesprächsentscheidungen ab und öffnet einen eigenen Zweig der Geschichte.

### Animationen

| Animation | Bilder | Schleife | Beschreibung |
| --- | --- | --- | --- |
| p3_idle | 12 | ja | Schwebt ±5 px, Blätter leuchten auf |
| p3_glide | 8 | ja | Gleitet, schneller als Phase 2 |
| p3_atk_ranken | 28 | nein | Siehe oben |
| p3_atk_erinnerungsriss | 18 | nein | Siehe oben |
| p3_atk_weltgericht_charge | 24 | nein | Siehe oben |
| p3_atk_weltgericht_release | 24 | nein | Siehe oben |
| p3_weltgericht_zoegern | 8 | nein | Siehe oben |
| p3_hit | 4 | nein | Kaum Reaktion, kurzes Aufflackern |
| p3_wings_loop | 8 | ja | Flügel öffnen und schließen sich leicht (70–100 %), eigene Ebene |

Animationen für Enden werden erst festgelegt, wenn die Enden geschrieben sind.

## Farbpaletten

Grundlage sind die Entwürfe v4 und v5 (gleiche Rüstungs-, Haar- und Mantelfarben). Übersicht als Bild: [paletten-phasen.png](../assets/konzept/psp/paletten-phasen.png).

### Phase 0 und 1 — aus den Entwürfen v4 und v5

| Name | Hex | Verwendung |
| --- | --- | --- |
| Tiefschwarz | `#020007` | Tiefste Schatten, Umrisse |
| Nachtschwarz | `#070418` | Rüstung dunkel |
| Schattenviolett | `#1b1433` | Rüstung Mitteltöne |
| Rüstungsgrau | `#292248` | Rüstung hell |
| Kantengrau | `#514d81` | Kanten der Rüstung |
| Mantel dunkel | `#1f0341` | Mantel Grundton |
| Mantel mittel | `#300462` | Mantel |
| Mantel hell | `#5a10aa` | Mantel Faltenlicht |
| Mantel Glanz | `#7914c7` | Mantel Kanten |
| Eisblau | `#95abf8` | Haar |
| Eisweiß | `#dbd7ea` | Haar Glanz |
| Türkis | `#59c3c3` | Augen |
| Magenta | `#ee20fb` | Kronenkristalle |
| Kristallviolett | `#cc32f2` | Sensenkristalle, Blüten |
| Gold dunkel | `#805e45` | Bänder am Sensenstiel |
| Gold hell | `#dbb176` | Gold Glanz |
| Sensenblatt | `#c4bce2` | Sensenblatt |
| Schneidenstreifen | `#6004c7` | Streifen entlang der Schneide |
| Blattgrün | `#49bcbb` | Blätter an den Blüten |
| Blütenmitte | `#e16366` | Blütenmitte |

### Phase 2 — zusätzlich

| Name | Hex | Verwendung |
| --- | --- | --- |
| Risslicht | `#a8fff4` | Leuchtende Risse |
| Rissglanz | `#e8fffb` | Hellste Punkte, Augen |
| Türkis dunkel | `#2a8f9a` | Schein um die Risse |
| Eisblau hell | `#7fd8ff` | Partikel, Fackeln |
| Verderbnis | `#ee20fb` | Adern der verdorbenen Wurzeln (gleiche Farbe wie die Kronenkristalle) |
| Verderbnis dunkel | `#3a0640` | Verdorbene Wurzeln, Schatten in den Helmrissen |

### Phase 3 — zusätzlich

| Name | Hex | Verwendung |
| --- | --- | --- |
| Wurzelholz dunkel | `#2b1a14` | Verholzte Rüstung, Flügel innen |
| Wurzelholz | `#5a3a28` | Holz Mitteltöne |
| Wurzelholz hell | `#8a5f3f` | Holz Kanten |
| Blattgrün | `#49bcbb` | Blätter |
| Blattlicht | `#7ff0c0` | Leuchtende Blätter |
| Blatt dunkel | `#1e6b4f` | Blätter Schatten |
| Kristall hell | `#ff6bff` | Kristalle leuchten stärker |

## Export und PSP-Umwandlung

Gegenüber dem ursprünglichen Vorschlag gibt es drei wichtige Änderungen:

1. **Indiziert statt 32-Bit-RGBA.** Alle Animationen der Königin zusammen haben etwa 4 Millionen Pixel. Als RGBA wären das etwa 16 MB, mehr als zwei Drittel des gesamten Spielspeichers. Mit 8 Bit pro Pixel sind es **etwa 4 MB**.
2. **Atlanten statt langer Streifen.** Die PSP verarbeitet Texturen nur bis 512 × 512 Pixel. Ein Streifen wie die Verwandlung 2→3 mit 96 Bildern wäre 7680 px breit. Aseprite exportiert deshalb als gepacktes Sprite-Sheet mit höchstens 512 × 512 und einer JSON-Datei mit den Bildpositionen.
3. **Laden vom Memory Stick statt `png2c`.** Ein Umwandlungsprogramm erzeugt aus PNG und JSON ein PSP-taugliches Format (8-Bit-Palette, für die Grafikeinheit umsortiert). Das Spiel lädt es beim Start.

### Umfang und Speicher (Vorschlag)

| Gruppe | Bilder | Größe | Speicher bei 8 Bit |
| --- | --- | --- | --- |
| Phase 0 | 30 | 64 × 96 | 0,18 MB |
| Verwandlung 0→1 | 24 | 64 × 96 | 0,14 MB |
| Phase 1 | 69 | 64 × 96 | 0,40 MB |
| Verwandlung 1→2 | 48 | 64 × 96 | 0,28 MB |
| Phase 2 | 76 | 64 × 96 | 0,45 MB |
| Verwandlung 2→3 | 96 | 80 × 112 | 0,82 MB |
| Phase 3 | 118 | 80 × 112 | 1,01 MB |
| Flügel | etwa 28 | 160 × 112 | 0,48 MB |
| Effekte (Impuls, Geschosse, Runen) | – | – | etwa 0,3 MB |
| **Summe** | | | **etwa 4,1 MB** |

Die breiteren Sensenangriffe (96 × 96) kommen mit etwa 0,3 MB hinzu, zusammen also **etwa 4,4 MB**. Das passt in das Budget von 6 MB für alle Figuren in [PSP1000.md](PSP1000.md), lässt aber nur etwa 2 MB für den Held mit seinen Ausrüstungsstufen. Wird es eng, können gekürzte Verwandlungen und weniger Bilder bei langen Angriffen (Ranken, Verwandlung 2→3) helfen.

### Dateinamen

```
queen_p0_idle.png, queen_p0_finger_tap.png, …
queen_p1_atk_richtschlag.png, queen_p1_atk_sensenzug.png, queen_p1_atk_kreisschnitt.png
queen_p2_atk_sternschauer.png, queen_p2_atk_windklinge.png, queen_p2_atk_todesurteil_mark.png, …
queen_p3_atk_ranken.png, queen_p3_atk_erinnerungsriss.png, queen_p3_atk_weltgericht_charge.png, …
queen_p3_wings_loop.png
queen_transform_0to1.png, queen_transform_1to2.png, queen_transform_2to3.png
fx_impuls_p2.png, fx_impuls_p3.png
```

Jede Datei kommt mit einer gleichnamigen `.json` für die Bildpositionen im Atlas.

## Offene Punkte

- Animationen für das Totenritual (magisches Feuer, In-den-Arm-nehmen, lila Portal), Umfang siehe [DIALOGE.md](DIALOGE.md#umsetzung-des-totenrituals).
- Konkrete Bildzahlen nach ersten Tests auf dem Gerät anpassen.
- Animationen für die Enden, sobald die Zweige der Geschichte stehen.
- Thronsaal Phase 3 mit Wurzeln und Rissen: Prompt `thronsaal-p3-v1` in [assets/PROMPTS.md](../assets/PROMPTS.md); Phase 2 liegt als `assets/konzept/psp/thronsaal-p2.png` vor.
