# Spielkonzept und weitere Planung

## Ausgangspunkt

„Dunkle Königin von Yggdrasil“ ist ein kompaktes Bosskampf-Spiel in dunkler Fantasywelt. **Der Spieler steuert die Königin**, den Endgegner. Der Held ist der Herausforderer, der immer wieder in den Thronsaal zurückkehrt und mit jedem Versuch besser wird.

Der Kern ist ein Souls-artiger Bosskampf aus umgekehrter Sicht: Nicht der Spieler lernt die Muster des Bosses, sondern der Held lernt die Muster des Spielers.

Die Königin trägt die majestätische, ernste Seite des Konzepts. Der Held bringt mit seinen knappen Kommentaren die Sprache eines lernenden Spielers mit: Guides, Timing, Combos, Phasen.

## Referenz und Abgrenzung

Das Spiel orientiert sich bewusst an **„The Dark Queen of Mortholme“**: Spieler als Boss, ein zurückkehrender Held, fester Bildausschnitt in einem Thronsaal, Dialoge zwischen den Kämpfen. Es soll keine Kopie werden. Eigene Elemente sind:

- **Welt und Motive:** Yggdrasil, Wurzeln, Erinnerungen und Schwüre statt einer fremden Welt; eigene Figuren, eigene Namen, eigene Grafiken.
- **Der Held spricht wie ein Spieler.** Seine Rückkehrkommentare über Timing, Combos und Guides sind ein eigener Humoransatz.
- **Die Geschichte verzweigt sich stark.** Sie ist nicht nur ein Weg mit wenigen Enden, sondern ein Geflecht vieler Zweige (siehe unten).
- **Zielplattform PSP-1000** mit den daraus folgenden Grenzen.

Texte, Grafiken, Musik und Namen des Referenzspiels werden nicht übernommen.

## Festgelegte Kampfschleife

1. Der Held betritt den Thronsaal.
2. Der Spieler kämpft als Königin mit ihren Angriffen gegen ihn.
3. Der Held stirbt und kehrt in den Thronsaal zurück.
4. Er kommentiert knapp den letzten Versuch.
5. Beim nächsten Versuch weicht er den Angriffen, die er bereits kennt, besser aus.
6. Zwischen einzelnen Abschnitten führen Königin und Held Gespräche.

Der Held wird mit jedem Versuch spürbar besser. **Die Werte der Königin bleiben dagegen immer gleich.** Ihre anfängliche Überlegenheit schwindet, weil der Held aufholt, nicht weil sie schwächer wird.

## Die drei Phasen der Königin

**Festgelegt:** Die Königin besitzt **drei Phasen** innerhalb eines Kampfes. Ihre Werte, also Schaden, Tempo und Lebenspunkte, ändern sich dabei nicht.

**Lebensbalken:** Die Königin hat einen Lebensbalken aus **drei übereinanderliegenden Leisten**. Ist die oberste Leiste leer, beginnt die nächste Phase mit der darunterliegenden Leiste. Ist die dritte Leiste leer, ist die Königin besiegt. Jede Leiste ist gleich lang, und zu Beginn jedes Kampfes sind alle drei wieder voll.

| Phase | Leiste | Angriffe |
| --- | --- | --- |
| 1 | **Rot** | Sensenangriffe (Vorschlag: Richtschlag, Sensenzug, Kreisschnitt) |
| 2 | **Orange** | Magische Angriffe mit Flächenschaden (Vorschlag: Sternschauer, Windklinge, Todesurteil) |
| 3 | **Lila** | Wurzel- und Erinnerungsangriffe mit Flächenschaden (Vorschlag: Ranken, Erinnerungsriss, Weltgericht) |

Vor Phase 1 sitzt die Königin auf dem Thron („Phase 0“, ohne Kampf). Aussehen, Angriffe und Animationen beschreibt [VISUAL_KOENIGIN.md](VISUAL_KOENIGIN.md).

- Jede Phase hat **eigene Angriffe**.
- Ab Phase 2 kommt **Flächenschaden** hinzu: Angriffe, die einen Bereich des Thronsaals treffen und dem Helden weniger Ausweichraum lassen.
- **Tempo:** In jeder Phase ist der Held mindestens 3 Runden lang leicht zu besiegen. Danach braucht er mindestens 6 weitere Runden, bis er die nächste Phase erreichen kann, je nachdem, wie gut der Spieler die Königin spielt. Frühestens erreicht er Phase 2 in Runde 10 und Phase 3 in Runde 19.

### Phasenwechsel

- Jeder Phasenwechsel beginnt mit einer **sichtbaren Veränderung der Königin**.
- Dabei setzt sie einen **magischen Impuls** frei. Trifft er den Helden, stirbt dieser **sofort**, unabhängig von seinen Herzen.
- Der Impuls kommt am **Ende der Verwandlung**. Während der Verwandlung **greift der Held nicht an und bleibt stehen**.
- **Gegenmaßnahmen (festgelegt):** Den Impuls beim Wechsel zu Phase 2 überspringt der Held, sobald er das Timing gelernt hat. Beim Wechsel zu Phase 3 flutet lila Nebel den Bildschirm; nur ein goldener Schild aus seinem **Amulett** schützt den Bereich, in dem er steht. Gerade dieser Moment eignet sich für Rückkehrkommentare wie „Okay, beim Phasenwechsel muss ich weg.“

**Helm (festgelegt):** Beim Wechsel zu Phase 2 reißt der Helm der Königin, beim Wechsel zu Phase 3 zerfällt er, und erst dann ist ihr Gesicht zu sehen. In ihm wohnt ein Teil Yggdrasils, der durch ihre lange Wacht verdorben wurde und sie beeinflusst. Das ist der Wendepunkt der Geschichte (siehe [KOENIGIN.md](KOENIGIN.md#der-verdorbene-yggdrasil--wendepunkt)).

**Veränderung (Vorschlag):** In Phase 2 leuchten die Risse ihres Körpers türkis, verdorbene Wurzeln wachsen aus den Helmrissen, und sie schwebt leicht. In Phase 3 sind Teile der Rüstung zu Wurzelholz geworden, und Flügel aus Wurzeln tragen sie.

## Herzen und Ausrüstung des Helden

**Festgelegt:**

- Der Held beginnt mit **1 Herz**. Im Lauf des Spiels steigt die Zahl auf **bis zu 5 Herzen**.
- Bessere Ausrüstung holt er sich über eine **Questreihe** außerhalb des Thronsaals. **Mit jeder neuen Ausrüstung kommt automatisch ein Herz dazu**, ohne eigenes Ereignis. Die Stufen stehen in [HELD.md](HELD.md#ausrüstungsstufen--sichtbar-an-umhang-und-schwert).
- **Neue Ausrüstung bedeutet keinen Sieg beim ersten Versuch.** Sie macht ihn widerstandsfähiger, die Muster muss er trotzdem lernen. Das Tempo aus [ANGRIFFE.md](ANGRIFFE.md#lernen-des-helden) gilt weiter.
- Während er diese Quests erledigt, bleibt er dem Thronsaal länger fern als nach einer gewöhnlichen Niederlage.
- **Ein Treffer der Königin kostet ein Herz.** Ausnahme: Der magische Impuls beim Phasenwechsel tötet sofort.
- Sein Fortschritt kommt also aus zwei Quellen: Er lernt die Angriffe der Königin, und er wird durch Ausrüstung und Herzen widerstandsfähiger.

### Die Amulett-Quest

**Festgelegt:** Der Held holt das Amulett erst, **nachdem er am zweiten Impuls gescheitert ist**:

1. Der Held erreicht zum ersten Mal das Ende von Phase 2. Die Königin verwandelt sich, lila Nebel flutet den Bildschirm.
2. Er versucht, dem Impuls wie beim ersten **durch einen Sprung auszuweichen**, und stirbt im Nebel.
3. Nach seiner Rückkehr bricht er zur **Amulett-Quest** auf. Es folgt wieder eine Abwesenheit: Die Königin steht allein im Thronsaal, und es geschieht bewusst nichts.
4. Er kehrt mit dem Amulett (Stufe 4, 4 Herzen) zurück und **überlebt den Impuls diesmal mit dem goldenen Schild**.

Damit sieht der Spieler zuerst, dass das Gelernte nicht mehr reicht, und danach, wie die neue Ausrüstung das Problem löst.

### Abwesenheit des Helden

Während der Held auf Quest ist, sieht der Spieler die **Königin allein im Thronsaal**. Dabei geschieht **bewusst nichts**: kein Gegner, kein Dialog, keine Aufgabe, keine Musik. Die Stille ist gewollt und zeigt, wie leer ihre Herrschaft ohne den Herausforderer ist. Der Spieler kann die Königin dabei frei durch den Saal gehen lassen.

Noch offen:

- Ab welcher Runde er zu den Quests 1, 2 und 4 aufbricht. Quest 3, das Amulett, folgt auf das Scheitern im Nebel.
- Wie lange eine Abwesenheit dauert.

## Nach dem Tod des Helden

**Festgelegt:**

1. Stirbt der Held, wird es **still** (siehe [AUDIO.md](AUDIO.md)).
2. Der Spieler kann die Königin **gehen lassen**. Sie geht zum Körper des Helden.
3. Dort wählt der Spieler das **Totenritual**: **✕ Verbrennen**, **○ Umarmen** (später freigeschaltet, danach verbrennen) oder **□ Opfern** durch ein lila Portal (ab dem ersten Helmriss). Einzelheiten und Folgen stehen in [DIALOGE.md](DIALOGE.md#totenritual).
4. Der Held kehrt zurück, **sobald die Königin wieder Richtung Thron läuft bzw. sich rechts im Saal aufhält**.

**Warum der Held zurückkehren kann, erklärt die Welt nicht genau.** Für die Königin ist es ohne Bedeutung: Sie lebt ewig und hat sich nie mit Vergänglichkeit befasst. Sie kann nicht verstehen, warum jemand an den Ort seines Scheiterns zurückkehrt; genau davon handeln ihre Worte bei seiner Rückkehr.

## Lernen des Helden — Planungsmaßstab

- Der Held merkt sich, welche Angriffe ihn getroffen haben, und weicht ihnen später häufiger oder früher aus.
- Er lernt nur, was er erlebt hat. Ein Angriff, den die Königin noch nie eingesetzt hat, trifft ihn unvorbereitet.
- Sein Fortschritt muss für den Spieler sichtbar sein: Ausweichen, das vorher nicht gelang, neue Ausrüstung oder ein veränderter Kampfstil.
- Sein Lernen bleibt nachvollziehbar und berechenbar. Es soll kein Zufall sein, wenn er einem Angriff ausweicht.

**Festgelegt (10.10.2026): echtes Lernen, garantierter Fortschritt.**

- **Vollständiges Wissen, schrittweise freigeschaltet.** Die KI kennt zu jedem Angriff die richtige Ausweichart und das richtige Bild. Der Lernstand bestimmt nur, wie viel davon sie anwendet (siehe [ANGRIFFE.md](ANGRIFFE.md#lernen-des-helden)). Kein Zufall beim Ausweichen und beim Zuschlagen.
- **Erholungslücke.** Nach jedem Angriff steht die Königin kurz still (etwa 0,7 s) und kann nicht angreifen. Beherrscht der Held den Angriff sicher, bringt er in dieser Lücke immer einen Gegenschlag an; die Lücke endet erst danach. Pausenlose Angriffe halten ihn also nicht für immer auf, gutes Spiel macht ihn nur langsamer.
- **Durchbruch.** Erreicht er 9 Versuche lang keine neue Phase, findet er ihre Lücke: Ab dem 10. Versuch wird sein Hieb stufenweise stärker (bis zum Dreifachen). Eine neue Phase setzt den Zähler zurück.
- **Gescriptet** sind nur die dramaturgischen Schlüsselstellen: Impulse, Amulett, Weltgericht und das Zögern (G8).
- **Aufgeben gibt es nur über das Gespräch „Der Patch“** ([DIALOGE.md](DIALOGE.md#p--der-patch)): Beim Durchbruch hält der Held die Mechanik für fehlerhaft und will auf einen Patch warten. Wählt die Königin die Endboss-Antwort, geht er, und das Spiel endet mit E1. Sie hält das für Schwäche; dass er ein Spieler ist, ahnt sie nicht.

## Ton und Dialogplanung

Der Humor entsteht aus dem Lernprozess des Helden und dem Gegensatz zur würdevollen Königin. Die Welt und die Königin behalten ihre Würde. Kommentare sind kurz und variieren.

Bei der Rückkehr spricht vorrangig die **Königin** (siehe [DIALOGE.md](DIALOGE.md#rückkehr-des-helden)). Der Held antwortet nur bei einem bestimmten Anlass. Seine Kommentare lassen sich nach diesen Kategorien planen:

| Kategorie | Beispiel | Voraussetzung |
| --- | --- | --- |
| Timingfehler | „Ahh. Wieder falsches Timing.“ | Er ist einem bekannten Angriff zu früh oder zu spät ausgewichen |
| Ungeeignete Strategie | „Diese Combo hilft mir hier nicht weiter.“ | Seine Angriffsfolge wurde unterbrochen |
| Theorie gegen Praxis | „Im Guide sah das deutlich einfacher aus.“ | Allgemeiner Rückkehrkommentar, sparsam einsetzen |
| Neuer Angriff | „Okay, *das* kannte ich noch nicht.“ | Die Königin hat einen neuen Angriff eingesetzt |
| Bekannte Phase | „Erste Phase sitzt. Jetzt muss ich nur noch den Rest überleben.“ | Er hat eine bekannte Phase überstanden |
| Unklare Niederlage | „Okay. Noch mal.“ | Keine eindeutige Zuordnung |

Die Kategorien sind ein Planungswerkzeug, keine bereits umgesetzte Fehlererkennung.

**Während des Kampfes wird nicht gesprochen.**

## Verzweigte Geschichte

Die Geschichte soll **einer von vielen möglichen Zweigen** sein. Jeder Durchlauf zeigt nur einen Teil davon.

- Zwischen Kampfabschnitten wählt der Spieler in Gesprächen die Antworten der Königin.
- Entscheidungen verändern die Beziehung zwischen Königin und Held, die Gespräche danach und das Ende.
- **Wendepunkt (festgelegt):** Wenn der Helm zum ersten Mal reißt, wird sichtbar, dass der verdorbene Yggdrasil die Königin beeinflusst. Ab hier stellt sich die Frage, wie viel ihres Handelns ihr eigener Wille ist.
- Mögliche Richtungen, als Vorschlag: Die Königin hält an ihrer Herrschaft fest; die Verderbnis siegt endgültig; der Held befreit sie von der Verderbnis; sie löst sich selbst und ihre Bindung an Yggdrasil; sie versteht das Anliegen des Helden; der Held gibt auf; beide finden einen dritten Weg.
- Ein Durchlauf bleibt kurz und in einer Sitzung spielbar. Die Vielfalt entsteht durch Wiederholen mit anderen Entscheidungen.

Die Vorgeschichte der Königin in [KOENIGIN.md](KOENIGIN.md) (Hüterin der Erinnerungen, Bindung an die Wurzeln, Angst vor dem Vergessen, der verdorbene Yggdrasil im Helm) bietet dafür die erzählerische Grundlage.

## Gestaltung der Angriffe — Planungsmaßstab

Jede Phase hat drei eigene Angriffe. **Jeder Angriff hat ein Zeitfenster zum Reagieren.** Der Held weicht mit einer **Ausweichrolle** oder einem **Sprung** aus; **Flächenschaden markiert vorher den Boden**. Alle neun Angriffe mit Signal, Zeitfenster, Treffer und Ausweichart stehen in [ANGRIFFE.md](ANGRIFFE.md).

## Darstellung

**Festgelegt:** 2D-Pixel-Art in fester Seitenansicht. Der ganze Kampf spielt in einem Thronsaal, der auf einen Bildschirm passt. Der Eingang liegt links, der Thron rechts. Entwürfe liegen in [assets/](../assets/README.md).

## Offene Entscheidungen

- Rundenzahlen für die Quests 1, 2 und 4 und die Dauer der Abwesenheit.
- Zeitwerte der Angriffe nach ersten Tests (Vorschläge in [ANGRIFFE.md](ANGRIFFE.md)).
- Grafik für Phase 3, Thronsaal-Varianten, Totenritual und Gehen (siehe [assets/README.md](../assets/README.md)).
- Technische Umsetzung (siehe [PSP1000.md](PSP1000.md)), Musik und Ton (siehe [AUDIO.md](AUDIO.md)).

## Erledigt

- Angriffe aller drei Phasen mit Zeitfenstern: [ANGRIFFE.md](ANGRIFFE.md).
- Lernverhalten des Helden: [ANGRIFFE.md](ANGRIFFE.md#lernen-des-helden).
- Gespräche, Totenritual und Enden: [DIALOGE.md](DIALOGE.md) (elf Gespräche, sechs Enden plus ein verborgenes).
- Rückkehr des Helden: wird in der Welt bewusst nicht erklärt.
