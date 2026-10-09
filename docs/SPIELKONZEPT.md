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

| Phase | Inhalt |
| --- | --- |
| 1 | Noch festzulegen |
| 2 | Noch festzulegen |
| 3 | Noch festzulegen |

Was sich in jeder Phase ändert, ist noch offen. Ein naheliegender Vorschlag: Jede Phase schaltet neue Angriffe frei, ohne die bisherigen stärker zu machen.

## Herzen und Ausrüstung des Helden

**Festgelegt:**

- Der Held beginnt mit **1 Herz**. Im Lauf des Spiels steigt die Zahl auf **bis zu 5 Herzen**.
- Neue Herzen und bessere Ausrüstung holt er sich über eine **Questreihe** außerhalb des Thronsaals.
- Während er diese Quests erledigt, bleibt er dem Thronsaal länger fern als nach einer gewöhnlichen Niederlage.
- Sein Fortschritt kommt also aus zwei Quellen: Er lernt die Angriffe der Königin, und er wird durch Ausrüstung und Herzen widerstandsfähiger.

Noch offen:

- Wie viel hält ein Herz aus, ein Treffer oder mehr?
- Wann bricht er zu einer Quest auf, und wie viele Herzen bringt er jeweils mit zurück?
- Wie erlebt der Spieler die Abwesenheit des Helden: als Zeitsprung, als Szene mit der Königin allein im Thronsaal oder als Bericht bei seiner Rückkehr?
- Welche Ausrüstungsteile gibt es, und wie sieht man sie am Sprite?

## Lernen des Helden — Planungsmaßstab

- Der Held merkt sich, welche Angriffe ihn getroffen haben, und weicht ihnen später häufiger oder früher aus.
- Er lernt nur, was er erlebt hat. Ein Angriff, den die Königin noch nie eingesetzt hat, trifft ihn unvorbereitet.
- Sein Fortschritt muss für den Spieler sichtbar sein: Ausweichen, das vorher nicht gelang, neue Ausrüstung oder ein veränderter Kampfstil.
- Sein Lernen bleibt nachvollziehbar und berechenbar. Es soll kein Zufall sein, wenn er einem Angriff ausweicht.

Die konkrete Umsetzung der Helden-KI ist noch nicht festgelegt.

## Ton und Dialogplanung

Der Humor entsteht aus dem Lernprozess des Helden und dem Gegensatz zur würdevollen Königin. Die Welt und die Königin behalten ihre Würde. Kommentare sind kurz und variieren.

Rückkehrkommentare des Helden lassen sich nach diesen Kategorien planen:

| Kategorie | Beispiel | Voraussetzung |
| --- | --- | --- |
| Timingfehler | „Ahh. Wieder falsches Timing.“ | Er ist einem bekannten Angriff zu früh oder zu spät ausgewichen |
| Ungeeignete Strategie | „Diese Combo hilft mir hier nicht weiter.“ | Seine Angriffsfolge wurde unterbrochen |
| Theorie gegen Praxis | „Im Guide sah das deutlich einfacher aus.“ | Allgemeiner Rückkehrkommentar, sparsam einsetzen |
| Neuer Angriff | „Okay, *das* kannte ich noch nicht.“ | Die Königin hat einen neuen Angriff eingesetzt |
| Bekannte Phase | „Erste Phase sitzt. Jetzt muss ich nur noch den Rest überleben.“ | Er hat eine bekannte Phase überstanden |
| Unklare Niederlage | „Okay. Noch mal.“ | Keine eindeutige Zuordnung |

Die Kategorien sind ein Planungswerkzeug, keine bereits umgesetzte Fehlererkennung.

## Verzweigte Geschichte

Die Geschichte soll **einer von vielen möglichen Zweigen** sein. Jeder Durchlauf zeigt nur einen Teil davon.

- Zwischen Kampfabschnitten wählt der Spieler in Gesprächen die Antworten der Königin.
- Entscheidungen verändern die Beziehung zwischen Königin und Held, die Gespräche danach und das Ende.
- Mögliche Richtungen, als Vorschlag: Die Königin hält an ihrer Herrschaft fest; sie versteht das Anliegen des Helden; sie löst ihre Bindung an Yggdrasil; der Held gibt auf; beide finden einen dritten Weg.
- Ein Durchlauf bleibt kurz und in einer Sitzung spielbar. Die Vielfalt entsteht durch Wiederholen mit anderen Entscheidungen.

Die Vorgeschichte der Königin in [KOENIGIN.md](KOENIGIN.md) (Hüterin der Erinnerungen, Bindung an die Wurzeln, Angst vor dem Vergessen) bietet dafür die erzählerische Grundlage.

## Gestaltung der Angriffe — Planungsmaßstab

Die Königin besitzt zu Beginn wenige, wuchtige Angriffe. In späteren Phasen kommen weitere hinzu. Jeder Angriff braucht eine deutlich erkennbare Ankündigung, damit auch der Spieler sieht, wann der Held ausweicht und warum.

Anzahl und Art der Angriffe sowie ihre Verteilung auf die drei Phasen sind noch nicht festgelegt.

## Darstellung

**Festgelegt:** 2D-Pixel-Art in fester Seitenansicht. Der ganze Kampf spielt in einem Thronsaal, der auf einen Bildschirm passt. Der Eingang liegt links, der Thron rechts. Entwürfe liegen in [assets/](../assets/README.md).

## Offene Entscheidungen

- Was ändert sich in jeder der drei Phasen?
- Ablauf der Questreihe des Helden und Darstellung seiner Abwesenheit.
- Wie genau lernt der Held, und wie wird sein Fortschritt sichtbar?
- Welche Angriffe besitzt die Königin in welcher Phase?
- Wie viele Gesprächsabschnitte und Enden gibt es?
- Wie wird die Rückkehr des Helden innerhalb der Welt erklärt?
- Wie häufig kommentiert der Held, und wie werden Wiederholungen vermieden?

## Reihenfolge der weiteren Planung

1. Die drei Phasen festlegen und die Angriffe der ersten Phase mit Ankündigung und Wirkung beschreiben.
2. Das Lernverhalten des Helden für diese Angriffe festlegen.
3. Den ersten Gesprächsabschnitt mit zwei bis drei Antwortmöglichkeiten schreiben.
4. Die Hauptzweige der Geschichte und ihre Enden skizzieren.
5. Danach die technische Umsetzung für die PSP-1000 beginnen ([PSP1000.md](PSP1000.md)).
