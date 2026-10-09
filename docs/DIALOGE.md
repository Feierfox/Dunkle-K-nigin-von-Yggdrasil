# Dialoge

Entwurf vom 09.10.2026. Alle Texte sind **Vorschläge** auf Grundlage von [SPIELKONZEPT.md](SPIELKONZEPT.md), [KOENIGIN.md](KOENIGIN.md) und [HELD.md](HELD.md).

## Grundsätze

- **Die Königin** spricht ruhig, knapp und würdevoll. Sie duzt den Helden. Sie benutzt nie die Spielersprache des Helden.
- **Der Held** spricht kurz und natürlich, wie jemand, der einen schweren Bosskampf übt: Timing, Muster, Phase, Combo, Guide. Keine modernen Gegenstände.
- **Die Verderbnis** spricht ab dem ersten Helmriss gelegentlich *durch* die Königin. Ihre Sätze sind kursiv gesetzt und klingen besitzergreifend, nie würdevoll.
- Gespräche sind kurz: höchstens etwa sechs Zeilen bis zur Auswahl. Ein Durchlauf soll in einer Sitzung spielbar bleiben.
- Der Held kommentiert nur, was er schon erlebt hat, und verrät keine unbekannten Angriffe.
- Auf der PSP passen etwa 2 Zeilen à 40 Zeichen in die Textbox. Längere Sätze werden auf mehrere Boxen verteilt.

## Werte für die Verzweigung

| Wert | Bereich | Start | Bedeutung |
| --- | --- | --- | --- |
| `vertrauen` | −3 bis +3 | 0 | Wie die Königin dem Helden begegnet: Verachtung bis Achtung |
| `einfluss` | 0 bis 5 | 2 | Wie stark die Verderbnis sie lenkt |

Dazu kommen Merker wie `riss_gesehen`, `impuls_ueberlebt`, `gesicht_gesehen` und `guide_gefragt` (Zahl). Antworten verändern die Werte; in den Tabellen steht die Wirkung in Klammern, zum Beispiel (vertrauen +1).

---

## Rückkehrkommentare des Helden

Nach jedem Tod kehrt der Held in den Thronsaal zurück. **Nicht jeder Tod braucht einen Kommentar**: Vorschlag ist etwa jeder zweite, nie dieselbe Zeile zweimal hintereinander. Die Auswahl richtet sich nach dem, was ihn zuletzt getötet hat.

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
| Weltgericht | „Das kann man nicht ausweichen. Das muss man aushalten.“ · „Ich brauch was Besseres als einen Schild.“ |
| Allgemein | „Dritte Phase. Im Guide steht hier nur: ‚Viel Glück.‘“ |

### Allgemein und ohne klare Ursache

„Okay. Noch mal.“ · „Im Guide sah das deutlich einfacher aus.“ · „Ich hab das Muster verstanden. Meine Hände offenbar noch nicht.“ · „Das war knapp. Also, für sie nicht.“ · „Laut Guide gibt es hier eine Lücke. Der Guide lügt nicht. Meistens.“

---

## Gesprächsabschnitte

Jeder Abschnitt läuft einmal pro Durchlauf. Die Auswahl hat der Spieler, er spricht als Königin.

### G1 — Die erste Audienz

**Auslöser:** Runde 1, bevor sie sich vom Thron erhebt (Phase 0).

> **Held:** „Okay. Endboss. Sieht genau so aus wie beschrieben.“
> **Königin:** „Du stehst in der Halle der Wurzeln. Niemand betritt sie ohne Grund.“
> **Held:** „Ich hab einen Grund. Und einen Guide.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Dann nenne deinen Grund.“ | „Erst wenn ich gewonnen hab. Ist so eine Regel.“ | vertrauen +1 |
| „Dein Grund endet hier.“ | „Klassischer Satz. Steht auch im Guide.“ | – |
| *Schweigen.* | „…Okay. Schweigsamer Boss. Das ist neu.“ | einfluss +1 |

### G2 — Beharrlichkeit

**Auslöser:** nach dem dritten Tod des Helden.

> **Königin:** „Du kehrst mit bemerkenswerter Beharrlichkeit zurück.“
> **Held:** „Ja. Ich lerne. Langsam, aber ich lerne.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Woher hast du dieses Wissen?“ | „Aus einem Guide. Wer ihn geschrieben hat, weiß ich nicht. Er ist ziemlich alt.“ | guide_gefragt +1 |
| „Lernen ändert nichts am Ende.“ | „Doch. Das Ende kommt später.“ | vertrauen −1 |
| „Dann lerne schneller.“ | „Das ist… fast nett. Danke?“ | vertrauen +1 |

### G3 — Der Aufbruch

**Auslöser:** vor der ersten Quest, zum Beispiel nach dem sechsten Tod in Phase 1.

> **Held:** „Ich brauch bessere Ausrüstung. Mit einem Herz geht das nicht.“
> **Held:** „Ich komm wieder. Lauf nicht weg.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Ich laufe nie.“ | „Stimmt. Du schreitest.“ | – |
| „Geh. Und komm nicht zurück.“ | „Netter Versuch.“ | vertrauen −1 |
| „Die Halle wird warten.“ | „Die Halle. Klar. Nur die Halle.“ | vertrauen +1 |

Danach folgt die **Abwesenheit**: Die Königin steht allein im Thronsaal, und es geschieht bewusst nichts. Kein Dialog, keine Musikänderung, kein Hinweis.

### G4 — Die Rückkehr

**Auslöser:** Rückkehr von der ersten Quest, mit 2 Herzen und Schild.

> **Held:** „Neuer Schild. Zwei Herzen. Diesmal hab ich einen Plan.“
> **Königin:** „Die Halle war still, während du fort warst.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Steht das in deinem Guide? Die Stille?“ | „Nein. Komisch, oder? Da steht viel über dich. Aber nichts darüber, wie es hier ist, wenn keiner kommt.“ | guide_gefragt +1, vertrauen +1 |
| „Still ist sie am schönsten.“ | „Dann stör ich jetzt gern.“ | – |
| „Dein Plan wird scheitern.“ | „Wahrscheinlich. Der nächste nicht.“ | einfluss +1 |

### G5 — Der erste Riss

**Auslöser:** Der Held erreicht zum ersten Mal Phase 2, der Helm reißt, der Impuls tötet ihn. Gespräch nach seiner Rückkehr.

> **Held:** „Moment. Das war gar nicht sie.“
> **Königin:** „Was redest du?“
> **Held:** „Eben. Die Stimme, kurz bevor das Licht kam. Das klang nicht nach dir.“
> ***Stimme:*** *„Er lügt. Er will, dass du zweifelst.“*

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Was hast du gehört?“ | „Etwas, das dich ‚mein‘ genannt hat.“ | vertrauen +1, einfluss −1 |
| „Es gibt keine andere Stimme.“ | „Okay. Dann red ich mit der, die gerade antwortet.“ | – |
| *„Er lügt.“* | „…Das war jetzt wieder die andere.“ | einfluss +1 |

### G6 — Stand gehalten

**Auslöser:** Der Held überlebt den Impuls zum ersten Mal.

> **Held:** „Ha! Steh noch! Okay, das hat gedauert.“
> **Königin:** „Kein Held vor dir hat das Licht überstanden.“
> **Held:** „Dann hatten die keinen Guide.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Zeig mir diesen Guide.“ | „Später. Die letzte Seite fehlt eh.“ | guide_gefragt +1 |
| „Es gab andere vor dir. Ich erinnere mich an jeden.“ | „An jeden? Das muss schwer sein.“ | vertrauen +1 |
| *„Das Licht wird stärker.“* | „Das sagt die andere wieder. Sie redet viel, wenn sie Angst hat.“ | einfluss +1 |

### G7 — Das Gesicht

**Auslöser:** Der Held erreicht zum ersten Mal Phase 3, der Helm zerfällt.

> **Held:** „Oh.“
> **Held:** „Du siehst nicht aus wie ein Endboss.“
> **Königin:** „Wie sieht ein Endboss aus?“
> **Held:** „Wie jemand, der nie müde wird.“

| Antwort der Königin | Antwort des Helden | Wirkung |
| --- | --- | --- |
| „Ich bin seit sehr langer Zeit müde.“ | „Dann lass mich das zu Ende bringen. Irgendwie.“ | vertrauen +1 |
| „Sieh weg.“ | „Nein. Diesmal nicht.“ | – |
| *„Sie ist, was ich aus ihr gemacht habe.“* | „Nein. Sie ist, was übrig ist. Das ist ein Unterschied.“ | einfluss +1 |

### G8 — Das Zögern

**Auslöser:** frühestens ab Runde 25, Phase 3, beim Aufladen des Weltgerichts, wenn `vertrauen ≥ 1`. Die Königin hält inne (Animation `p3_weltgericht_zoegern`).

> ***Stimme:*** *„Entlade es. Er ist nur einer von vielen.“*
> **Held:** „Wenn du jetzt loslässt, bin ich weg. Ich weiß. Ich hab's oft genug gesehen.“
> **Königin:** „Warum bleibst du dann stehen?“
> **Held:** „Weil du auch stehen bleibst.“

| Antwort der Königin | Folge |
| --- | --- |
| „Dann bleib stehen.“ (Weltgericht wird zurückgenommen) | Weiter zum Ende nach Werten (siehe unten) |
| *Weltgericht entladen.* | einfluss +2; der Kampf geht weiter |
| „Nimm sie. Die Krone.“ | Nur wenn `vertrauen ≥ 2`: Ende E4 |

---

## Enden

Ein Durchlauf endet, sobald der Held die Königin besiegt oder eine Bedingung unten erfüllt ist. Die Bedingungen sind Vorschläge und werden beim Testen abgestimmt.

| Ende | Bedingung | Inhalt |
| --- | --- | --- |
| **E1 Ewige Königin** | Held stirbt 40-mal, ohne Phase 3 zu erreichen, oder `vertrauen ≤ −2` bei G8 | Der Held kehrt nicht mehr zurück. Die Königin setzt sich auf den Thron. Die Halle bleibt still, wie in der Abwesenheit, nur diesmal für immer. |
| **E2 Die Wurzel herrscht** | `einfluss = 5` | Die Verderbnis übernimmt ganz. Die Königin spricht nur noch kursiv. Die Wurzeln brechen aus der Halle in die Welt. Der Held: „Okay. Dafür gibt es keinen Guide.“ |
| **E3 Befreiung** | Held besiegt sie in Phase 3, `vertrauen ≥ 2`, `einfluss ≤ 2` | Sein letzter Schlag trifft nicht sie, sondern die verdorbenen Äste der Krone. Sie lebt, bleibt aber an den Baum gebunden. Diesmal aus eigenem Willen. |
| **E4 Loslösung** | Bei G8 „Nimm sie. Die Krone.“ | Sie löst ihre Bindung an Yggdrasil selbst und reicht dem Helden die Krone, damit er sie zerbricht. Die Erinnerungen der Wurzeln strömen frei. Sie verlässt die Halle durch den Eingang, zum ersten Mal. |
| **E5 Zwei Wächter** | Held besiegt sie, `vertrauen = 3`, `einfluss ≤ 1` | Keiner zerbricht etwas. Der Held bleibt. Sie bewachen die Wurzeln gemeinsam. Er: „Endboss und Held im selben Team. Das ist mal ein Twist.“ |
| **E6 Die neue Krone** | Held besiegt sie, `einfluss ≥ 3` | Die Krone fällt, der Held hebt sie auf. Er sagt nichts mehr. Der Spieler sieht ihn auf dem Thron, und ein neuer Held betritt die Halle. |

Es gibt **ein weiteres, verborgenes Ende**. Es steht in [geheim/ENDE_VERBORGEN.md](geheim/ENDE_VERBORGEN.md). **Achtung, Spoiler.** Einige Zeilen in diesem Dokument bereiten es unauffällig vor; sie sind hier nicht gekennzeichnet.

## Offen

- Genaue Rundenzahlen für G3 und die weiteren Quests (Herzen 3 bis 5).
- Gespräche nach der zweiten bis vierten Quest.
- Verteilung der Rückkehrkommentare auf feste und zufällige Auswahl.
- Ob die Verderbnis auch mitten im Kampf spricht oder nur in Gesprächen.
