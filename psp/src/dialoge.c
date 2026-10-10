/* Texte aus docs/DIALOGE.md. Jedes Gespräch hat zwei oder drei Antworten;
 * die erste ist immer die Rolle des Endbosses. */
#include <stddef.h>
#include "dialoge.h"

#define N(a) ((int)(sizeof(a) / sizeof((a)[0])))
#define K SP_KOENIGIN
#define H SP_HELD
#define V SP_VERDERBNIS
#define E SP_ERZAEHLER

static const Zeile g1z[] = {
    {H, "„Okay. Endboss. Sieht genau so aus wie beschrieben.“"},
    {K, "„Du stehst in der Halle der Wurzeln. Niemand betritt sie ohne Grund.“"},
    {H, "„Ich hab einen Grund. Und einen Guide.“"},
};
static const Wahl g1w[] = {
    {K, "„Dein Grund endet hier.“", "„Klassischer Satz. Steht auch im Guide.“", -1, 0, 0, 0, 0},
    {K, "„Dann nenne deinen Grund.“", "„Erst wenn ich gewonnen hab. Ist so eine Regel.“", 1, 0, 0, 0, 0},
    {E, "Schweigen. Etwas im Helm flüstert.", "„…Okay. Schweigsamer Boss. Das ist neu.“", 0, 1, 0, 0, 0},
};

static const Zeile g2z[] = {
    {K, "„Du kehrst mit bemerkenswerter Beharrlichkeit zurück.“"},
    {H, "„Ja. Ich lerne. Langsam, aber ich lerne.“"},
};
static const Wahl g2w[] = {
    {K, "„Lernen ändert nichts am Ende.“", "„Doch. Das Ende kommt später.“", -1, 0, 0, 0, 0},
    {K, "„Dann lerne schneller.“", "„Das ist… fast nett. Danke?“", 1, 0, 0, 0, 0},
    {K, "„Woher hast du dieses Wissen?“", "„Aus einem Guide. Wer ihn geschrieben hat, weiß ich nicht. Er ist ziemlich alt.“", 0, 0, 1, 0, 0},
};

static const Zeile g3z[] = {
    {H, "„Ich brauch bessere Ausrüstung. Mit einem Herz geht das nicht.“"},
    {H, "„Ich komm wieder. Lauf nicht weg.“"},
};
static const Wahl g3w[] = {
    {K, "„Geh. Und komm nicht zurück.“", "„Netter Versuch.“", -1, 0, 0, 0, 0},
    {K, "„Die Halle wird warten.“", "„Die Halle. Klar. Nur die Halle.“", 1, 0, 0, 0, 0},
};

static const Zeile g4z[] = {
    {H, "„Neuer Umhang. Zwei Herzen. Diesmal hab ich einen Plan.“"},
    {K, "„Die Halle war still, während du fort warst.“"},
};
static const Wahl g4w[] = {
    {K, "„Dein Plan wird scheitern. Wie alle vor ihm.“", "„Wahrscheinlich. Der nächste nicht.“", -1, 0, 0, 0, 0},
    {K, "„Still ist sie immer. Ich habe es nur nie bemerkt.“", "„Dann stör ich jetzt gern.“", 1, 0, 0, 0, 0},
    {K, "„Steht das in deinem Guide? Die Stille?“", "„Nein. Komisch, oder? Da steht viel über dich. Aber nichts darüber, wie es hier ist, wenn keiner kommt.“", 0, 0, 1, 0, 0},
};

static const Zeile g5z[] = {
    {H, "„Moment. Das war gar nicht sie.“"},
    {K, "„Was redest du?“"},
    {H, "„Eben. Die Stimme, kurz bevor das Licht kam. Das klang nicht nach dir.“"},
    {V, "„Er lügt. Er will, dass du zweifelst.“"},
};
static const Wahl g5w[] = {
    {K, "„Es gibt nur eine Stimme in dieser Halle. Meine.“", "„Okay. Dann red ich mit der, die gerade antwortet.“", -1, 0, 0, 0, 0},
    {K, "„Was hast du gehört?“", "„Etwas, das dich ‚mein‘ genannt hat.“", 1, -1, 0, 0, 0},
    {V, "„Er lügt.“", "„…Das war jetzt wieder die andere.“", 0, 1, 0, 0, 0},
};

static const Zeile r2z[] = {
    {K, "„Du warst länger fort als sonst.“"},
    {H, "„Quest. Ein Schneider, ein Brunnen, vierzig Fingerhüte. Lange Geschichte.“"},
    {K, "„Draußen vergeht die Zeit. Ich habe davon gehört.“"},
};
static const Wahl r2w[] = {
    {K, "„Dann vergeude sie nicht hier.“", "„Ist meine Zeit. Ich vergeude sie, wo ich will.“", -1, 0, 0, 0, 0},
    {K, "„Wie ist es, wenn sie vergeht?“", "„Eilig. Man will was schaffen, bevor sie rum ist. Deshalb komm ich ja wieder.“", 1, 0, 0, 0, 0},
    {V, "„Zeit ist ein Fehler. Wir bereinigen ihn.“", "„Okay. Das war wieder die andere. Die mag keine Uhren.“", 0, 1, 0, 0, 0},
};

static const Zeile g6z[] = {
    {H, "„Ha! Steh noch! Okay, das hat gedauert.“"},
    {K, "„Kein Held vor dir hat das Licht überstanden.“"},
    {H, "„Dann hatten die keinen Guide.“"},
};
static const Wahl g6w[] = {
    {K, "„Einmal. Das Licht hat Geduld.“", "„Ich auch. Mittlerweile.“", -1, 0, 0, 0, 0},
    {K, "„Es gab andere vor dir. Ich erinnere mich an jeden.“", "„An jeden? Das muss schwer sein.“", 1, 0, 0, 0, 0},
    {K, "„Zeig mir diesen Guide.“", "„Später. Die letzte Seite fehlt eh.“", 0, 0, 1, 0, 0},
};

static const Zeile r3z[] = {
    {H, "„Diesmal komm ich durch den Nebel.“"},
    {K, "„Kein Lebender ist durch diesen Nebel gegangen.“"},
    {H, "„Die hatten auch kein Amulett.“"},
    {V, "„Nimm es ihm. Es glänzt wie etwas, das mir gehört hat.“"},
};
static const Wahl r3w[] = {
    {K, "„Dann holt dich der Nebel eben langsamer.“", "„Klingt nach einem Plan. Für dich.“", -1, 0, 0, 0, 0},
    {K, "„Dieses Gold. Ich habe es schon einmal gesehen.“", "„Echt? Es lag in einem Fisch.“", 1, 0, 0, 0, 0},
    {V, "„Gib es her.“", "„Nein. Und jetzt weiß ich, dass es funktioniert.“", 0, 1, 0, 0, 0},
};

static const Zeile g7z[] = {
    {H, "„Oh.“"},
    {H, "„Du siehst nicht aus wie ein Endboss.“"},
    {K, "„Wie sieht ein Endboss aus?“"},
    {H, "„Wie jemand, der nie müde wird.“"},
};
static const Wahl g7w[] = {
    {K, "„Dann sieh gut hin. Es ist das Letzte, was du siehst.“", "„Sagst du jedes Mal.“", -1, 0, 0, 0, 0},
    {K, "„Ich bin seit sehr langer Zeit müde.“", "„Dann lass mich das zu Ende bringen. Irgendwie.“", 1, 0, 0, 0, 0},
    {V, "„Sie ist, was ich aus ihr gemacht habe.“", "„Nein. Sie ist, was übrig ist. Das ist ein Unterschied.“", 0, 1, 0, 0, 0},
};

static const Zeile r4z[] = {
    {H, "„Letzte Ausrüstung. Legendär.“"},
    {K, "„Jede Klinge, die je hier lag, war die letzte.“"},
    {H, "„Ja, aber diese ist golden.“"},
};
static const Wahl r4w[] = {
    {K, "„Ich werde sie zu den anderen legen.“", "„Zu den anderen? Wie viele waren denn… nein, sag's nicht.“", -1, 0, 0, 0, 0},
    {K, "„Warum kommst du zurück, wenn du doch sterben kannst?“", "„Gerade deshalb. Wenn es ewig dauern würde, hätte ich keine Eile.“", 1, 0, 0, 0, 0},
    {V, "„Gold schmilzt auch.“", "„Das war jetzt eine Drohung an mein Schwert. Notiert.“", 0, 1, 0, 0, 0},
};

static const Zeile g8z[] = {
    {V, "„Entlade es. Er ist nur einer von vielen.“"},
    {H, "„Wenn du jetzt loslässt, bin ich weg. Ich weiß. Ich hab's oft genug gesehen.“"},
    {K, "„Warum bleibst du dann stehen?“"},
    {H, "„Weil du auch stehen bleibst.“"},
};
/* ende 9 = Ende nach Werten bestimmen (E3, E5 oder E6) */
static const Wahl g8w[] = {
    {E, "Weltgericht entladen.", NULL, -2, 0, 0, 0, 0},
    {K, "„Dann bleib stehen.“", NULL, 0, 0, 0, 0, 9},
    {K, "„Nimm sie. Die Krone.“", NULL, 0, 0, 0, 1, 4},
};

/* Der Held steckt fest und hält die Mechanik für fehlerhaft; die Königin hält das für Schwäche. */
static const Zeile patchz[] = {
    {H, "„Okay. Das ist verbuggt. Die Hitbox ist eindeutig kaputt.“"},
    {H, "„Ich warte auf den Patch. Mit dem Fix spiel ich weiter.“"},
    {K, "„Ein Patch?“"},
    {H, "„Ein Fix. Irgendwann flickt das jemand.“"},
};
static const Wahl patchw[] = {
    {K, "„Niemand flickt, was ich zerbrochen habe. Geh.“", "„Ja, ja. Bis zum Patch.“", 0, 0, 0, 0, 1},
    {K, "„Dann flicke es selbst.“", "„…Workaround. Okay. Einer geht noch.“", 0, 0, 0, 0, 0},
    {V, "„Er ist zerbrochen. Lass ihn liegen.“", "„Und jetzt redet die andere. Gut, ich bleib. Aus Trotz.“", 0, 1, 0, 0, 0},
};

/* Eröffnung: Ein Untertan warnt die Königin vor dem Helden und stellt sich ihm in den Weg. */
static const Zeile introz[] = {
    {SP_DIENER, "„Herrin … verzeiht, dass ich es wage, Euren Thronsaal zu betreten.“"},
    {SP_DIENER, "„Ein Fremder ist durch das Wurzeltor gekommen. Grüne Kapuze, blanke Klinge.“"},
    {SP_DIENER, "„Er tötet unsere Soldaten und kommt immer wieder.“"},
    {K, "„Dann lass ihn kommen.“"},
    {SP_DIENER, "„Ich – ich halte ihn auf, Herrin! Für Euch! Ich …“"},
};

/* Erster Phasenwechsel: Sie wurde getroffen; zum ersten Mal spricht die Verderbnis durch sie. */
static const Zeile verw1z[] = {
    {K, "„…Du hast mich getroffen.“"},
    {K, "„Seit Jahrhunderten hat mich niemand getroffen.“"},
    {V, "„Genug. Er gehört den Wurzeln.“"},
    {H, "„Moment. Das war gar nicht sie.“"},
};
/* Erster Wechsel zu Phase 3: Der Helm hält nicht mehr. */
static const Zeile verw2z[] = {
    {K, "„Der Helm … er hält nicht mehr.“"},
    {V, "„Dann zeig ihm, was darunter ist. Und dann lösch ihn aus.“"},
    {H, "„Okay. Der Nebel da. Der ist neu.“"},
};

const Gespraech GESPRAECH[GESPRAECHE] = {
    {"G1 Die erste Audienz", g1z, N(g1z), g1w, N(g1w)},
    {"G2 Beharrlichkeit", g2z, N(g2z), g2w, N(g2w)},
    {"G3 Der Aufbruch", g3z, N(g3z), g3w, N(g3w)},
    {"G4 Die Rückkehr", g4z, N(g4z), g4w, N(g4w)},
    {"G5 Der erste Riss", g5z, N(g5z), g5w, N(g5w)},
    {"R2 Die zweite Rückkehr", r2z, N(r2z), r2w, N(r2w)},
    {"G6 Stand gehalten", g6z, N(g6z), g6w, N(g6w)},
    {"R3 Das Amulett", r3z, N(r3z), r3w, N(r3w)},
    {"G7 Das Gesicht", g7z, N(g7z), g7w, N(g7w)},
    {"R4 Das goldene Schwert", r4z, N(r4z), r4w, N(r4w)},
    {"G8 Das Zögern", g8z, N(g8z), g8w, N(g8w)},
    {"P Der Patch", patchz, N(patchz), patchw, N(patchw)},
    {"Eröffnung", introz, N(introz), 0, 0},
    {"Phasenwechsel 1", verw1z, N(verw1z), 0, 0},
    {"Phasenwechsel 2", verw2z, N(verw2z), 0, 0},
};

const Ende ENDEN[7] = {
    {0, {0}},
    {"Ewige Königin", {"Der Held kehrt nicht mehr zurück. Er ist zerbrochen,",
                       "glaubt sie. Sie setzt sich auf den Thron.",
                       "Die Halle bleibt still, wie in der Abwesenheit.", "Nur diesmal für immer. Kein Patch kommt."}},
    {"Die Wurzel herrscht", {"Das letzte Opfer fällt, und das Portal schließt sich nicht mehr.",
                             "Die Verderbnis spricht jetzt allein.", "Wurzeln brechen aus der Halle in die Welt.",
                             "„Okay. Dafür gibt es keinen Guide.“"}},
    {"Befreiung", {"Sein letzter Schlag trifft nicht sie,", "sondern die verdorbenen Äste der Krone.",
                   "Sie lebt und bleibt an den Baum gebunden.", "Diesmal aus eigenem Willen."}},
    {"Loslösung", {"Sie löst ihre Bindung an Yggdrasil selbst.", "Er zerbricht die Krone, die Erinnerungen strömen frei.",
                   "Zum ersten Mal verlässt sie die Halle", "durch den Eingang."}},
    {"Zwei Wächter", {"Keiner zerbricht etwas. Der Held bleibt.", "Sie bewachen die Wurzeln gemeinsam.",
                      "„Endboss und Held im selben Team.", "Das ist mal ein Twist.“"}},
    {"Die neue Krone", {"Die Krone fällt, der Held hebt sie auf.", "Er sagt nichts mehr.",
                        "Er sitzt auf dem Thron,", "und ein neuer Held betritt die Halle."}},
};
