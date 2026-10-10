# Dialoge

Entwurf vom 09.10.2026. Alle Texte sind **Vorschläge** auf Grundlage von [SPIELKONZEPT.md](SPIELKONZEPT.md), [KOENIGIN.md](KOENIGIN.md) und [HELD.md](HELD.md).

## Grundsätze

- **Die Königin** spricht ruhig, knapp und würdevoll. Sie duzt den Helden. Sie benutzt nie die Spielersprache des Helden.
- **Der Held** spricht kurz und natürlich, wie jemand, der einen schweren Bosskampf übt: Timing, Muster, Phase, Combo, Guide. Keine modernen Gegenstände.
- **Die Verderbnis** spricht ab dem ersten Helmriss gelegentlich *durch* die Königin. Ihre Sätze klingen besitzergreifend, nie würdevoll. **Im Spiel ist sie farblich und an der Schrift erkennbar:** magentafarbener Text (`#ee20fb`) in einer eigenen, kantig-zittrigen Bitmap-Schrift; der Rand der Textbox bekommt dabei Risse. In diesem Dokument sind ihre Sätze kursiv gesetzt.
- **Während des Kampfes wird nicht gesprochen.** Gesprochen wird nur in Phase 0, bei der Rückkehr des Helden, in Gesprächsabschnitten und beim Totenritual. Verwandlungen und das Zögern beim Weltgericht unterbrechen den Kampf und dürfen einen Satz enthalten.
- Gespräche sind kurz: höchstens etwa sechs Zeilen bis zur Auswahl. Ein Durchlauf soll in einer Sitzung spielbar bleiben.
- Der Held kommentiert nur, was er schon erlebt hat, und verrät keine unbekannten Angriffe.
- Auf der PSP passen etwa 2 Zeilen à 40 Zeichen in die Textbox. Längere Sätze werden auf mehrere Boxen verteilt.

## Aufbau der Entscheidungen

**Festgelegt:** Jedes Gespräch und jedes Totenritual bietet **zwei oder drei Möglichkeiten**. **Eine davon ist immer die Rolle des Endbosses**: kalt, überlegen, unnahbar. Die anderen öffnen Wege zu verschiedenen Enden.

| Kennzeichen | Haltung | Führt in Richtung |
| --- | --- | --- |
| **[Endboss]** | Sie bleibt die unbezwingbare Herrscherin | E1 Ewige Königin, E6 Die neue Krone |
| **[Nähe]** | Sie lässt den Helden an sich heran | E3 Befreiung, E4 Loslösung, E5 Zwei Wächter |
| **[Verderbnis]** | Sie gibt der Stimme im Helm nach | E2 Die Wurzel herrscht, E6 Die neue Krone |
| **[Neugier]** | Sie fragt nach, was der Held weiß | wirkt unscheinbar, siehe verborgenes Ende |

Im Spiel selbst stehen diese Kennzeichen nicht dabei. Der Spieler sieht nur die Sätze.

### Werte

| Wert | Bereich | Start | Bedeutung |
| --- | --- | --- | --- |
| `vertrauen` | −3 bis +3 | 0 | Wie die Königin dem Helden begegnet: Verachtung bis Achtung |
| `einfluss` | 0 bis 5 | 2 | Wie stark die Verderbnis sie lenkt |

Dazu kommen Merker wie `riss_gesehen`, `impuls_ueberlebt`, `gesicht_gesehen`, `opfer` (Zahl) und `guide_gefragt` (Zahl). In den Tabellen steht die Wirkung in Klammern, zum Beispiel (vertrauen +1).

---

## Rückkehr des Helden

Nach jedem Tod kehrt der Held in den Thronsaal zurück. Die Welt erklärt nicht, warum er das kann. Für die Königin ist das ohne Bedeutung: Sie lebt ewig und hat sich nie mit Vergänglichkeit befasst.

**Festgelegt:** Die Kommentare zur Rückkehr kommen **vorrangig von der Königin**. Sie kann nie wirklich verstehen, warum jemand an den Ort seines Scheiterns zurückkehrt, denn sie selbst kann nicht vergehen.

### Worte der Königin (vorrangig)

Bei etwa zwei von drei Rückkehren spricht die Königin eine Zeile, nie dieselbe zweimal hintereinander. Die Zeilen werden mit der Zeit nachdenklicher.

| Abschnitt | Zeilen |
| --- | --- |
| Frühe Rückkehren (bis Runde 5) | „Du bist wieder hier. Hier, wo du gefallen bist.“ · „Ich habe dich verbrannt. Und doch stehst du dort.“ · „Die Toten bleiben, wo sie fallen. Du nicht.“ · „Warum kehrt man an den Ort zurück, an dem man gestorben ist?“ |
| Mittlere Rückkehren | „Du hast nur ein Leben. Warum gibst du es immer wieder hier aus?“ · „Ich habe alle Zeit der Welt. Du nicht. Und doch hast du es eiliger.“ · „Jedes Mal ein wenig weniger Furcht in deinem Schritt. Ist das, was ihr Lernen nennt?“ · „Kehrt auch die Flut zurück, um wieder zu weichen?“ |
| Späte Rückkehren (ab Phase 3) | „Ich zähle nicht mehr, wie oft. Ich merke nur, dass ich warte.“ · „Der Ort deines Scheiterns ist dir vertrauter geworden als mir mein Thron.“ · „Vielleicht muss man vergehen können, um so wiederzukommen.“ |
| Bei hoher Verderbnis (`einfluss ≥ 3`) | *„Wieder er. Wieder mehr für die Wurzeln.“* · *„Er kommt, weil er uns gehört.“* |
| Bei hohem Vertrauen (`vertrauen ≥ 2`) | „Du bist zurück. Gut.“ · „Ich habe die Stufen gefegt. Ich weiß nicht, warum.“ |

### Antworten des Helden (nur bei Anlass)

Der Held spricht bei der Rückkehr **nur bei einem bestimmten Anlass**: beim ersten Tod durch einen neuen Angriff, nach neuer Ausrüstung, bei den Impulsen und nach dem Totenritual. Dann antwortet er auf die Zeile der Königin oder spricht statt ihr. Die Zeilen unten richten sich nach dem, was ihn zuletzt getötet hat.

### Phase 1 (rote Leiste)

| Anlass | Zeilen |
| --- | --- |
| Richtschlag | „Okay. Wenn die Sense oben ist, bin ich nicht mehr vorne.“ · „Zu früh ausgewichen. Sie hält kurz an.“ · „Das war Timing. Nur halt das falsche.“ |
| Sensenzug | „Moment, die trifft beim Zurückziehen?“ · „Ich bin dem Wurf ausgewichen. Dem Rückweg nicht.“ · „Raus, warten, *dann* rein. Merk dir das.“ |
| Kreisschnitt | „Nah ran war offensichtlich die falsche Idee.“ · „Wer dreht sich bitte mit einer Sense?“ · „Zwei Schritte Abstand. Mindestens.“ |
| Fortschritt | „Erste Leiste fast leer. Fast.“ · „Ich hab sie getroffen. Zweimal! Das zählt.“ · „Bis hier passt es. Danach verliere ich den Rhythmus.“ |

### Phasenwechsel und Impuls

| Anlass | Zeilen |
| --- | --- |
| Erster Tod durch Impuls | „Ich hab nichts gemacht. Ich hab nur *gewartet*.“ |
| Weitere Tode durch Impuls | „Okay, beim Phasenwechsel muss ich weg.“ · „Das Leuchten heißt nicht ‚schön‘. Das Leuchten heißt ‚lauf‘.“ · „Das braucht kein Timing. Das braucht einen Schild.“ |
| Impuls überlebt, danach gestorben | „Den Impuls hab ich. Den Rest noch nicht.“ |
| Erster Tod im lila Nebel (ohne Amulett) | „Ich bin gesprungen. Wie beim letzten Mal. Drüberspringen geht hier nicht. Da ist kein Drüber.“ |
| Aufbruch zur Amulett-Quest (direkt danach) | „Okay. Springen reicht nicht mehr. Ich brauch was, das mich *schützt*. Bin bald zurück. Also, relativ bald.“ |
| Erstes Mal mit Amulett-Schild überlebt | „Okay, das Amulett kann *das*? Gold steht mir.“ |

### Phase 2 (orange Leiste)

| Anlass | Zeilen |
| --- | --- |
| Sternschauer | „Die Markierungen am Boden sind keine Deko.“ · „Ich stand genau zwischen zwei Kreisen. Dachte ich.“ |
| Windklinge | „Springen. Man springt über die Sichel.“ · „Unten durch geht offenbar nicht.“ |
| Todesurteil | „Wenn eine Rune unter mir leuchtet, bleib ich nicht stehen. Notiert.“ |
| Allgemein | „Neue Phase, neue Regeln. Klassisch.“ · „Sie schwebt jetzt. Natürlich schwebt sie jetzt.“ |

### Phase 3 (lila Leiste)

| Anlass | Zeilen |
| --- | --- |
| Ranken | „Der Boden selbst ist ein Angriff. Fair.“ |
| Erinnerungsriss | „Ich hab kurz was gesehen. Eine Stadt? Dann war ich tot.“ |
| Weltgericht | „Da hilft kein Amulett. Da hilft nur, dass sie es nicht tut.“ · „Das kann man nicht ausweichen. Und aushalten auch nicht.“ |
| Allgemein | „Dritte Phase. Im Guide steht hier nur: ‚Viel Glück.‘“ |

### Neue Ausrüstung

Beim **ersten Tod nach einer Quest** kommentiert der Held seine neue Ausrüstung und die umständliche Quest, mit der er sie bekommen hat. Danach kann eine zweite Zeile gelegentlich wiederkommen.

| Stufe | Ausrüstung | Erster Tod danach | Später gelegentlich |
| --- | --- | --- | --- |
| 2 | Tannengrüner Umhang | „Für den Umhang musste ich zwölf Wolfsfelle sammeln. Nur jeder dritte Wolf hatte eins dabei. Wie geht das bei einem *Wolf*?“ | „Neuer Umhang, gleiches Ergebnis.“ |
| 3 | Smaragdgrüner Umhang | „Den hat mir ein Schneider genäht. Vorher sollte ich seinen Fingerhut aus dem Brunnen holen. Im Brunnen lagen vierzig Fingerhüte.“ | „Der Umhang ist schön. Hilft nur nicht gegen Sensen.“ |
| 4 | Amulett | „Das Amulett? Ein alter Mann hat mir eine Angel geschenkt. Und dann hatte ein riesiger Fisch das Amulett verschluckt. Welcher Gamedesigner kommt auf sowas?“ | „Das Amulett riecht immer noch nach Fisch.“ |
| 5 | Legendäres goldenes Schwert | „Legendäres Schwert. Steckte in einem Stein. Der Stein wollte, dass ich ihm vorher drei Fragen beantworte. Eine davon war: ‚Bist du sicher?‘“ | „Goldenes Schwert, und trotzdem tot. Der Schaden steht da nicht dran.“ |

### Allgemein und ohne klare Ursache

„Okay. Noch mal.“ · „Im Guide sah das deutlich einfacher aus.“ · „Ich hab das Muster verstanden. Meine Hände offenbar noch nicht.“ · „Das war knapp. Also, für sie nicht.“ · „Laut Guide gibt es hier eine Lücke. Der Guide lügt nicht. Meistens.“

---

## Totenritual

Nach jedem Sieg über den Helden liegt sein Körper im Thronsaal, und es ist still (siehe [AUDIO.md](AUDIO.md)).

**Festgelegt:**

1. Der Spieler **steuert die Königin zu Fuß** zum Körper des Helden.
2. Steht sie bei ihm, erscheinen die verfügbaren Tasten: **✕ Verbrennen**, **○ Umarmen** (danach verbrennen), **□ Opfern** (lila Portal).
3. Nach dem Ritual geht sie zurück. **Der Held kehrt zurück, sobald die Königin wieder Richtung Thron läuft bzw. sich in der rechten Hälfte des Saals aufhält.**

Solange sie beim Körper steht oder links bleibt, kommt er nicht. Es gibt kein Zeitlimit.

| Möglichkeit | Verfügbar | Ablauf | Wirkung |
| --- | --- | --- | --- |
| **[Endboss] ✕ Magisches Feuer** | immer | Sie hebt die Hand, eisblaues Feuer verbrennt den Körper. Sie sieht nicht hin. | – |
| **[Nähe] ○ In den Arm nehmen** | ab G2, solange `vertrauen ≥ 0` | Sie kniet nieder, hebt den Körper auf und hält ihn einen Moment. Dann verbrennt sie ihn in ihren Armen. | vertrauen +1 |
| **[Verderbnis] □ Das lila Portal** | ab G5 (erster Helmriss) | Unter dem Körper öffnet sich ein lila Portal. Er fällt hinein, Yggdrasil als Opfer. Die verdorbenen Wurzeln pulsieren. | einfluss +1, opfer +1 |

- **Ohne es zu verstehen:** Das Feuer ist ein Ritual aus ihrer Zeit als Hüterin der Erinnerungen. Sie weiß nicht mehr, warum sie es tut. Ihre Hand tut es einfach. Erst wenn sie den Helden in den Arm nimmt, bekommt die Geste eine Bedeutung.
- **Begrenzung:** Nähe und Verderbnis wirken höchstens einmal zwischen zwei Gesprächsabschnitten. Wer jedes Mal dieselbe Möglichkeit wählt, verändert die Werte also nicht schneller.
- Beim **ersten** Mal jeder Möglichkeit spricht die Verderbnis oder die Königin einen Satz:
  - Feuer: **Königin:** „Brenne. Und werde erinnert.“ (Sie stockt kurz, als wüsste sie nicht, woher der Satz kommt.)
  - Arm: **Königin:** „…Du bist leichter, als ich dachte.“
  - Portal: ***Stimme:*** *„Endlich. Gib ihn mir. Alle, die kommen.“*

### Rückkehrkommentare nach dem Ritual

Beim ersten Mal nach jeder Möglichkeit ersetzt eine dieser Zeilen den normalen Rückkehrkommentar:

| Ritual | Zeile des Helden |
| --- | --- |
| Feuer | „Ich riech nach Rauch. Das ist neu.“ |
| Arm | „Ich hab geträumt, dass mich jemand festhält. Komisch.“ |
| Portal | „Ich war woanders. Unter den Wurzeln. Da war etwas, das mich kannte.“ |
| Portal, ab dem dritten Mal | „Jedes Mal komm ich ein bisschen kälter zurück. Mach das nicht mehr.“ |

---

## Eröffnung

**Ablauf:** Beim Spielbeginn tritt zuerst ein Untertan der Königin ein: gebeugt, in fahl-violetter Kutte, ohne Waffe. Er verneigt sich tief vor ihr und warnt sie, demütig und unterwürfig. Danach richtet er sich auf und stellt sich dem Helden in den Weg, der ihn mit einem Hieb erschlägt. Erst dann beginnt G1, und danach erscheinen die Steuerungshinweise. Start überspringt die Szene.

> **Untertan:** „Herrin … verzeiht, dass ich es wage, Euren Thronsaal zu betreten.“
> **Untertan:** „Ein Fremder ist durch das Wurzeltor gekommen. Grüne Kapuze, blanke Klinge.“
> **Untertan:** „Er fragt nach Euch, Herrin. Er sagt … er habe einen Guide.“
> **Königin:** „Dann lass ihn kommen.“
> **Untertan:** „Ich – ich halte ihn auf, Herrin! Für Euch! Ich …“
> *Der Held tritt ein und erschlägt ihn.*
> **Held:** „Tutorial-Gegner. Erledigt.“

Keine Auswahl: Die Szene stellt Königin, Held und seine Spielersprache vor. Die Figur des Untertans entsteht in `tools/cutout/diener.py` aus dem Helden-Entwurf (Schwert entfernt, umgefärbt, kleiner und gebeugt).

## Gesprächsabschnitte

Jeder Abschnitt läuft einmal pro Durchlauf. Der Spieler wählt als Königin.

### G1 — Die erste Audienz

**Auslöser:** Runde 1, bevor sie sich vom Thron erhebt (Phase 0).

> **Held:** „Okay. Endboss. Sieht genau so aus wie beschrieben.“
> **Königin:** „Du stehst in der Halle der Wurzeln. Niemand betritt sie ohne Grund.“
> **Held:** „Ich hab einen Grund. Und einen Guide.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Dein Grund endet hier.“ | „Klassischer Satz. Steht auch im Guide.“ | vertrauen −1 |
| [Nähe] | „Dann nenne deinen Grund.“ | „Erst wenn ich gewonnen hab. Ist so eine Regel.“ | vertrauen +1 |
| [Verderbnis] | *Schweigen. Etwas im Helm flüstert.* | „…Okay. Schweigsamer Boss. Das ist neu.“ | einfluss +1 |

### G2 — Beharrlichkeit

**Auslöser:** nach dem dritten Tod des Helden.

> **Königin:** „Du kehrst mit bemerkenswerter Beharrlichkeit zurück.“
> **Held:** „Ja. Ich lerne. Langsam, aber ich lerne.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Lernen ändert nichts am Ende.“ | „Doch. Das Ende kommt später.“ | vertrauen −1 |
| [Nähe] | „Dann lerne schneller.“ | „Das ist… fast nett. Danke?“ | vertrauen +1 |
| [Neugier] | „Woher hast du dieses Wissen?“ | „Aus einem Guide. Wer ihn geschrieben hat, weiß ich nicht. Er ist ziemlich alt.“ | guide_gefragt +1 |

### G3 — Der Aufbruch

**Auslöser:** vor der ersten Quest, zum Beispiel nach dem sechsten Tod in Phase 1.

> **Held:** „Ich brauch bessere Ausrüstung. Mit einem Herz geht das nicht.“
> **Held:** „Ich komm wieder. Lauf nicht weg.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Geh. Und komm nicht zurück.“ | „Netter Versuch.“ | vertrauen −1 |
| [Nähe] | „Die Halle wird warten.“ | „Die Halle. Klar. Nur die Halle.“ | vertrauen +1 |

Danach folgt die **Abwesenheit**: Die Königin steht allein im Thronsaal, und es geschieht bewusst nichts. Kein Dialog, keine Musikänderung, kein Hinweis.

### G4 — Die Rückkehr

**Auslöser:** Rückkehr von der ersten Quest, mit 2 Herzen und neuem Umhang.

> **Held:** „Neuer Umhang. Zwei Herzen. Diesmal hab ich einen Plan.“
> **Königin:** „Die Halle war still, während du fort warst.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Dein Plan wird scheitern. Wie alle vor ihm.“ | „Wahrscheinlich. Der nächste nicht.“ | vertrauen −1 |
| [Nähe] | „Still ist sie immer. Ich habe es nur nie bemerkt.“ | „Dann stör ich jetzt gern.“ | vertrauen +1 |
| [Neugier] | „Steht das in deinem Guide? Die Stille?“ | „Nein. Komisch, oder? Da steht viel über dich. Aber nichts darüber, wie es hier ist, wenn keiner kommt.“ | guide_gefragt +1 |

### G5 — Der erste Riss

**Auslöser:** Der Held erreicht zum ersten Mal Phase 2, der Helm reißt, der Impuls tötet ihn. Gespräch nach seiner Rückkehr.

> **Held:** „Moment. Das war gar nicht sie.“
> **Königin:** „Was redest du?“
> **Held:** „Eben. Die Stimme, kurz bevor das Licht kam. Das klang nicht nach dir.“
> ***Stimme:*** *„Er lügt. Er will, dass du zweifelst.“*

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Es gibt nur eine Stimme in dieser Halle. Meine.“ | „Okay. Dann red ich mit der, die gerade antwortet.“ | vertrauen −1 |
| [Nähe] | „Was hast du gehört?“ | „Etwas, das dich ‚mein‘ genannt hat.“ | vertrauen +1, einfluss −1 |
| [Verderbnis] | *„Er lügt.“* | „…Das war jetzt wieder die andere.“ | einfluss +1 |

Ab hier steht im Totenritual das **lila Portal** zur Wahl.

### R2 — Die zweite Rückkehr

**Auslöser:** Rückkehr von der zweiten Quest (Stufe 3, 3 Herzen, smaragdgrüner Umhang), in der Regel nach G5.

> **Königin:** „Du warst länger fort als sonst.“
> **Held:** „Quest. Ein Schneider, ein Brunnen, vierzig Fingerhüte. Lange Geschichte.“
> **Königin:** „Draußen vergeht die Zeit. Ich habe davon gehört.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Dann vergeude sie nicht hier.“ | „Ist meine Zeit. Ich vergeude sie, wo ich will.“ | vertrauen −1 |
| [Nähe] | „Wie ist es, wenn sie vergeht?“ | „Eilig. Man will was schaffen, bevor sie rum ist. Deshalb komm ich ja wieder.“ | vertrauen +1 |
| [Verderbnis] | *„Zeit ist ein Fehler. Wir bereinigen ihn.“* | „Okay. Das war wieder die andere. Die mag keine Uhren.“ | einfluss +1 |

### G6 — Stand gehalten

**Auslöser:** Der Held überlebt den Impuls zum ersten Mal.

> **Held:** „Ha! Steh noch! Okay, das hat gedauert.“
> **Königin:** „Kein Held vor dir hat das Licht überstanden.“
> **Held:** „Dann hatten die keinen Guide.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Einmal. Das Licht hat Geduld.“ | „Ich auch. Mittlerweile.“ | vertrauen −1 |
| [Nähe] | „Es gab andere vor dir. Ich erinnere mich an jeden.“ | „An jeden? Das muss schwer sein.“ | vertrauen +1 |
| [Neugier] | „Zeig mir diesen Guide.“ | „Später. Die letzte Seite fehlt eh.“ | guide_gefragt +1 |

### R3 — Das Amulett

**Auslöser:** Rückkehr von der Amulett-Quest (Stufe 4), nachdem er im lila Nebel gestorben ist (siehe [SPIELKONZEPT.md](SPIELKONZEPT.md#die-amulett-quest)).

> **Held:** „Diesmal komm ich durch den Nebel.“
> **Königin:** „Kein Lebender ist durch diesen Nebel gegangen.“
> **Held:** „Die hatten auch kein Amulett.“
> ***Stimme:*** *„Nimm es ihm. Es glänzt wie etwas, das mir gehört hat.“*

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Dann holt dich der Nebel eben langsamer.“ | „Klingt nach einem Plan. Für dich.“ | vertrauen −1 |
| [Nähe] | „Dieses Gold. Ich habe es schon einmal gesehen.“ | „Echt? Es lag in einem Fisch.“ | vertrauen +1 |
| [Verderbnis] | *„Gib es her.“* | „Nein. Und jetzt weiß ich, dass es funktioniert.“ | einfluss +1 |

Das Amulett stammt, ohne dass es ausgesprochen wird, aus der Zeit der Hüter, also aus der Zeit vor der Verderbnis. Deshalb schützt es gegen den Nebel, und deshalb kommt es der Königin bekannt vor.

### G7 — Das Gesicht

**Auslöser:** Der Held erreicht zum ersten Mal Phase 3, der Helm zerfällt.

> **Held:** „Oh.“
> **Held:** „Du siehst nicht aus wie ein Endboss.“
> **Königin:** „Wie sieht ein Endboss aus?“
> **Held:** „Wie jemand, der nie müde wird.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Dann sieh gut hin. Es ist das Letzte, was du siehst.“ | „Sagst du jedes Mal.“ | vertrauen −1 |
| [Nähe] | „Ich bin seit sehr langer Zeit müde.“ | „Dann lass mich das zu Ende bringen. Irgendwie.“ | vertrauen +1 |
| [Verderbnis] | *„Sie ist, was ich aus ihr gemacht habe.“* | „Nein. Sie ist, was übrig ist. Das ist ein Unterschied.“ | einfluss +1 |

### R4 — Das goldene Schwert

**Auslöser:** Rückkehr von der letzten Quest (Stufe 5, legendäres goldenes Schwert), in Phase 3 und vor G8.

> **Held:** „Letzte Ausrüstung. Legendär.“
> **Königin:** „Jede Klinge, die je hier lag, war die letzte.“
> **Held:** „Ja, aber diese ist golden.“

| | Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- | --- |
| [Endboss] | „Ich werde sie zu den anderen legen.“ | „Zu den anderen? Wie viele waren denn… nein, sag's nicht.“ | vertrauen −1 |
| [Nähe] | „Warum kommst du zurück, wenn du doch sterben kannst?“ | „Gerade deshalb. Wenn es ewig dauern würde, hätte ich keine Eile.“ | vertrauen +1 |
| [Verderbnis] | *„Gold schmilzt auch.“* | „Das war jetzt eine Drohung an mein Schwert. Notiert.“ | einfluss +1 |

### G8 — Das Zögern

**Auslöser:** frühestens ab Runde 25, Phase 3, beim Aufladen des Weltgerichts, wenn `vertrauen ≥ 1`. Die Königin hält inne (Animation `p3_weltgericht_zoegern`).

> ***Stimme:*** *„Entlade es. Er ist nur einer von vielen.“*
> **Held:** „Wenn du jetzt loslässt, bin ich weg. Ich weiß. Ich hab's oft genug gesehen.“
> **Königin:** „Warum bleibst du dann stehen?“
> **Held:** „Weil du auch stehen bleibst.“

| | Antwort der Königin | Folge |
| --- | --- | --- |
| [Endboss] | *Weltgericht entladen.* | vertrauen −2; der Held stirbt, nichts schützt ihn |
| [Nähe] | „Dann bleib stehen.“ | Weltgericht wird zurückgenommen, der Kampf endet nach Werten (siehe Enden) |
| [Nähe] | „Nimm sie. Die Krone.“ | Nur wenn `vertrauen ≥ 2`, sonst fehlt diese Zeile: Ende E4 |

### P — Der Patch

**Auslöser:** Der Held erreicht 9 Versuche lang keine neue Phase; Gespräch bei seiner nächsten Rückkehr, einmal pro Durchlauf. Ab diesem Versuch beginnt sein Durchbruch (siehe [SPIELKONZEPT.md](SPIELKONZEPT.md#lernen-des-helden--planungsmaßstab)). Er ist ein Spieler, der an einer Stelle ständig scheitert und die Schuld bei der Mechanik sucht. Die Königin weiß nicht, dass es ein Spiel ist; sie versteht nur, dass er aufgeben will.

> **Held:** „Okay. Das ist verbuggt. Die Hitbox ist eindeutig kaputt.“
> **Held:** „Ich warte auf den Patch. Mit dem Fix spiel ich weiter.“
> **Königin:** „Ein Patch?“
> **Held:** „Ein Fix. Irgendwann flickt das jemand.“

| | Antwort der Königin | Antwort des Helden | Folge |
| --- | --- | --- | --- |
| [Endboss] | „Niemand flickt, was ich zerbrochen habe. Geh.“ | „Ja, ja. Bis zum Patch.“ | Ende E1 |
| [Nähe] | „Dann flicke es selbst.“ | „…Workaround. Okay. Einer geht noch.“ | er bleibt |
| [Verderbnis] | *„Er ist zerbrochen. Lass ihn liegen.“* | „Und jetzt redet die andere. Gut, ich bleib. Aus Trotz.“ | einfluss +1, er bleibt |

---

## Enden

Ein Durchlauf endet, sobald der Held die Königin besiegt oder eine Bedingung unten erfüllt ist. Die Bedingungen sind Vorschläge und werden beim Testen abgestimmt.

| Ende | Weg | Bedingung | Inhalt |
| --- | --- | --- | --- |
| **E1 Ewige Königin** | Endboss | Im Gespräch „Der Patch“ die Endboss-Antwort | Der Held geht, um auf einen Patch zu warten, und kehrt nicht mehr zurück. Sie hält ihn für zerbrochen und setzt sich auf den Thron. Die Halle bleibt still, wie in der Abwesenheit, nur diesmal für immer. Der Patch kommt nie. |
| **E2 Die Wurzel herrscht** | Verderbnis | `einfluss = 5` und `opfer ≥ 3` | Das letzte Opfer fällt durch das Portal, und das Portal schließt sich nicht mehr. Die Verderbnis übernimmt ganz, die Königin spricht nur noch kursiv. Wurzeln brechen aus der Halle in die Welt. Der Held, ein letztes Mal: „Okay. Dafür gibt es keinen Guide.“ |
| **E3 Befreiung** | Nähe | Held besiegt sie in Phase 3, `vertrauen ≥ 2`, `einfluss ≤ 2` | Sein letzter Schlag trifft nicht sie, sondern die verdorbenen Äste der Krone. Sie lebt, bleibt aber an den Baum gebunden. Diesmal aus eigenem Willen. |
| **E4 Loslösung** | Nähe | Bei G8 „Nimm sie. Die Krone.“ | Sie löst ihre Bindung an Yggdrasil selbst und reicht dem Helden die Krone, damit er sie zerbricht. Die Erinnerungen der Wurzeln strömen frei. Sie verlässt die Halle durch den Eingang, zum ersten Mal. |
| **E5 Zwei Wächter** | Nähe | Held besiegt sie, `vertrauen = 3`, `einfluss ≤ 1`, mindestens dreimal „In den Arm nehmen“ | Keiner zerbricht etwas. Der Held bleibt. Sie bewachen die Wurzeln gemeinsam. Er: „Endboss und Held im selben Team. Das ist mal ein Twist.“ |
| **E6 Die neue Krone** | Endboss oder Verderbnis | Held besiegt sie, und keine Bedingung von E3 oder E5 ist erfüllt | Die Krone fällt, der Held hebt sie auf. Er sagt nichts mehr. Der Spieler sieht ihn auf dem Thron, und ein neuer Held betritt die Halle. |

Es gibt **ein weiteres, verborgenes Ende**. Es steht in [geheim/ENDE_VERBORGEN.md](geheim/ENDE_VERBORGEN.md). **Achtung, Spoiler.** Einige Zeilen in diesem Dokument bereiten es unauffällig vor.

## Umsetzung des Totenrituals

- **Königin:** Hand heben (6 Bilder); Niederknien, Aufheben, Halten (16 Bilder); Hand senken, Portal öffnen (8 Bilder).
- **Held:** liegend (1 Bild); in den Armen gehalten (2 Bilder, eigene Pose).
- **Effekte:** eisblaues Feuer (8 Bilder, Schleife); lila Portal am Boden, aufgehend, fallender Körper, schließend (12 Bilder). Das Portal liegt vor der Kampflinie auf dem Boden (Y 240–260).
- **Speicher:** etwa 0,2 MB zusätzlich bei 8 Bit; Ergänzung in [VISUAL_KOENIGIN.md](VISUAL_KOENIGIN.md) folgt.

## Offen

- Genaue Rundenzahlen, ab denen der Held zu den Quests 1, 2 und 4 aufbricht (Quest 3, das Amulett, folgt auf das Scheitern im Nebel).
- Bitmap-Schriften für Königin, Held und Verderbnis.
