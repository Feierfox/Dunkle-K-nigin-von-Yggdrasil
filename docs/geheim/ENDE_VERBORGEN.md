# ⚠️ Spoiler: Das verborgene Ende

**Nicht weiterlesen, wenn du das Ende selbst entdecken willst.**

Entwurf vom 09.10.2026, Vorschlag. Grundlage: [DIALOGE.md](../DIALOGE.md), [KOENIGIN.md](../KOENIGIN.md).

&nbsp;

&nbsp;

&nbsp;

---

## E7 — Die letzte Seite

### Die Idee

Der Held spricht das ganze Spiel über von seinem **Guide**. Für den Spieler ist das ein Running Gag: die Sprache eines Spielers, der Bosskämpfe übt.

**Der Guide existiert wirklich.** Der Held hat ihn in den versunkenen Bibliotheken im Reich der Königin gefunden. Er ist alt, und die letzte Seite fehlt (G6).

Geschrieben hat ihn **die Königin selbst**, vor Jahrhunderten. Damals war sie noch Hüterin der Erinnerungen und spürte, wie der Baum im Helm verdarb und sie veränderte. Bevor die Verderbnis ihr den Willen nahm, schrieb sie auf, wie man sie besiegen kann: jeden Angriff, jedes Muster, jede Lücke. Diese Anleitung war für jemanden gedacht, der eines Tages kommen und nicht aufgeben würde. Danach vergaß sie es. Die Verderbnis hat dafür gesorgt.

Damit fügt sich vieles zusammen:
- **Warum der Held so schnell lernt:** Er lernt nicht nur, er liest nach.
- **Warum die Halle in seinem Guide nicht vorkommt, wenn keiner da ist** (G4): Sie hat nie aufgeschrieben, wie einsam es ist.
- **Die beschädigte fünfte Kronenspitze**, „Loslassen“: Sie ist der Schwur, den sie gebrochen hat, als sie die Anleitung vergaß.

### Bedingungen

Alle müssen im selben Durchlauf erfüllt sein:

1. **`guide_gefragt ≥ 3`:** Die Königin hat in G2, G4 und G6 nach dem Guide gefragt. Die Antwortoptionen wirken harmlos und neugierig.
2. **`impuls_ueberlebt`:** Der Held hat den Impuls mindestens einmal überstanden.
3. **Die Tür:** Während einer Abwesenheit des Helden (ab der zweiten Quest) geht die Königin zum Eingang links und bleibt dort stehen, bis er zurückkommt. In der Abwesenheit geschieht weiterhin bewusst nichts; es gibt keinen Hinweis, dass man das tun kann. Erst bei seiner Rückkehr zeigt sich die Folge.
4. **`einfluss ≤ 3`:** Sonst lässt die Verderbnis das Gespräch an der Tür nicht zu.

### Szene an der Tür (G4b)

**Auslöser:** Bedingung 3. Der Held kommt zurück und findet die Königin direkt am Eingang statt auf dem Thron.

> **Held:** „Whoa. Okay. Du stehst… an der Tür. Das ist neu. Das steht nirgends.“
> **Königin:** „Gib ihn mir. Deinen Guide.“
> **Held:** „…Na gut. Aber nichts rausreißen.“

*Sie blättert. Bei einer Seite hält sie inne.*

> **Königin:** „Diese Schrift.“
> ***Stimme:*** *„Gib ihn zurück.“*
> **Königin:** „Das ist meine.“
> **Held:** „Moment. *Du* hast den Guide geschrieben? Gegen dich selbst?“
> **Königin:** „Ich erinnere mich nicht daran. Aber ich erkenne, wie ich ein ‚R‘ schreibe.“

Merker `letzte_seite_gesucht` wird gesetzt. Der Kampf läuft danach normal weiter.

### Bei G8 — eine vierte Antwort

Wenn `letzte_seite_gesucht` gesetzt ist, erscheint beim Zögern eine zusätzliche Antwort:

| Antwort der Königin | Folge |
| --- | --- |
| „Ich weiß, was auf der letzten Seite steht.“ | Ende E7 |

> **Königin:** „Auf der letzten Seite stand: Brich nicht mich. Brich, was in der Krone wohnt. Ich halte still.“
> ***Stimme:*** *„Du hast es vergessen. Ich habe dafür gesorgt.“*
> **Königin:** „Ja. Und jetzt erinnere ich mich. Das ist mein Amt.“

### Das Finale

Das Ende wird **gespielt**, nicht nur gezeigt:

1. Die Verderbnis übernimmt kurz die Kontrolle und greift den Helden an. Das ist ein normaler Angriff der Phase 3.
2. Der Spieler muss die Königin **stillhalten**: fünf Sekunden lang keine Taste außer ↓, „sich beugen“. Greift der Spieler an, geht der Kampf normal weiter, und das Ende ist für diesen Durchlauf verloren.
3. Hält sie still, weicht der Held nicht mehr aus. Er springt und trifft die Krone. Vier der fünf Astspitzen zerspringen. Die verdorbenen Wurzeln verdorren.
4. Nur die beschädigte fünfte Spitze, „Loslassen“, bleibt. An ihr wächst ein einzelnes Blatt.

### Schluss

> **Held:** „Okay. Das ist das erste Mal, dass ein Guide recht hatte.“
> **Königin:** „Ich wusste nicht, wer kommen würde. Nur, dass jemand kommt.“
> **Held:** „Und jetzt?“
> **Königin:** „Jetzt schreibe ich die letzte Seite neu.“

*Letztes Bild: Die Königin sitzt auf den Stufen vor dem Thron, nicht auf ihm. Sie schreibt. Der Held sitzt eine Stufe tiefer und liest mit.*

*Auf der Seite steht: „Für den Nächsten. Er wird nicht kämpfen müssen.“*

### Umsetzung

- **Neue Animationen:** Königin am Eingang stehend (aus `p1_idle`), Blättern im Buch (8 Bilder), Stillhalten/Beugen (6 Bilder), Sitzen auf den Stufen und Schreiben (8 Bilder, Schleife). Held lesend (6 Bilder).
- **Neue Effekte:** Zerspringen der vier Kronenspitzen (Partikel, sparsam), wachsendes Blatt an der fünften Spitze.
- **Requisit:** ein kleines Buch (Guide), 8 × 6 Pixel, in der Hand des Helden ab G4b sichtbar.
- **Speicherstand:** Ist E7 einmal erreicht, könnte der Guide im Hauptmenü als lesbares Extra erscheinen: alle Angriffsbeschreibungen in der Handschrift der Königin. Das ist eine Belohnung für Wiederholer.
