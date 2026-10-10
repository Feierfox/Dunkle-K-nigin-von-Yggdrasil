/* Testszene: steuerbare Königin, lernender Held, Tod, Totenritual, Rückkehr.
 * Werte nach docs/ANGRIFFE.md, docs/SPIELKONZEPT.md und docs/DIALOGE.md. */
#include <pspctrl.h>
#include <stdlib.h>
#include <string.h>

#include "spiel.h"
#include "grafik.h"
#include "assets_gen.h"

#define BODEN 240
#define TICKS_JE_BILD 5          /* Animationen mit 12 Bildern pro Sekunde */
#define K_MIN 140
#define K_MAX 380
#define H_MIN 40
#define H_MAX 440
#define LEISTE 60                /* Lebenspunkte je Leiste */
#define HIEB_SCHADEN 4
/* Aus assets_gen.h (tools/cutout/entwuerfe.py): UMARM_ABSTAND = Kniepunkt der Königin vom
 * Fußpunkt des Toten, TOD_MITTE = Mitte des liegenden Körpers, TOD_SCHWERT_BILD = ab diesem
 * Bild liegt das Schwert am Boden. Der Körper liegt mit dem Kopf in Blickrichtung. */

/* Umarmung: Haltezeit je Bild in 12tel Sekunden (animation.json des Entwurfs) */
static const int UMARM_DAUER[8] = {3, 3, 3, 4, 8, 8, 6, 8};

enum { ANG_RICHTSCHLAG, ANG_SENSENZUG, ANG_KREISSCHNITT, ANG_IMPULS, ANG_ANZAHL };

enum { K_BEREIT, K_ANGRIFF, K_VERWANDLUNG };
enum { H_KOMMT, H_KAMPF, H_HIEBT, H_ROLLT, H_SPRINGT, H_GETROFFEN, H_TOT, H_WEG };
enum { L_KAMPF, L_RITUAL, L_ABWESEND };

typedef struct {
    int x, zustand, tick, angriff, phase;
    int lp[3];                    /* drei Leisten: rot, orange, lila */
    int getroffen_in_schwung;
    int blick;                    /* außerhalb des Kampfs: 1 = nach rechts (gespiegelt) */
} Koenigin;

typedef struct {
    float x;
    int zustand, tick, herzen, max_herzen, stufe;
    int unverwundbar, plan_tick, plan_art, plan_angriff, plan_richtung, roll_richtung;
    int hieb_getroffen;
    int getroffen[ANG_ANZAHL];    /* Lernen: wie oft dieser Angriff ihn getroffen hat */
    int tode, letzte_ursache, leiche_x, verbrannt, feuer_tick;
    int leiche_spiegel;           /* 1: er blickte nach links, Kopf liegt links */
    int umarm_geht, umarm_tick, aufsteh_tick, umarmungen, zuletzt_umarmt;
} Held;

static Koenigin K;
static Held H;
static int lage, lage_tick, runde, text_tick, impuls_tick, ring_tick;
static const char *text_zeile[2];
static unsigned int text_farbe[2];
static unsigned int zufall = 12345;

static int zuf(int n) { zufall = zufall * 1103515245u + 12345u; return (zufall >> 16) % n; }

static void sage(const char *a, unsigned int fa, const char *b, unsigned int fb)
{
    text_zeile[0] = a; text_farbe[0] = fa;
    text_zeile[1] = b; text_farbe[1] = fb;
    text_tick = 60 * 5;
}

#define WEISS 0xFFFFFFFF
#define KOENIGIN_TEXT 0xFFF8E0E0  /* leicht eisblau (ABGR) */
#define HELD_TEXT 0xFFB8F0C8      /* leicht grün */

static const char *const WORTE_FRUEH[] = {
    "„Du bist wieder hier. Hier, wo du gefallen bist.“",
    "„Ich habe dich verbrannt. Und doch stehst du dort.“",
    "„Die Toten bleiben, wo sie fallen. Du nicht.“",
    "„Warum kehrt man an den Ort zurück, an dem man gestorben ist?“",
};
static const char *const WORTE_MITTE[] = {
    "„Du hast nur ein Leben. Warum gibst du es immer wieder hier aus?“",
    "„Ich habe alle Zeit der Welt. Du nicht. Und doch hast du es eiliger.“",
    "„Jedes Mal ein wenig weniger Furcht in deinem Schritt.“",
    "„Kehrt auch die Flut zurück, um wieder zu weichen?“",
};
static const char *const HELD_ERSTER_TOD[ANG_ANZAHL] = {
    "„Okay. Wenn die Sense oben ist, bin ich nicht mehr vorne.“",
    "„Ich bin dem Wurf ausgewichen. Dem Rückweg nicht.“",
    "„Nah ran war offensichtlich die falsche Idee.“",
    "„Ich hab nichts gemacht. Ich hab nur *gewartet*.“",
};

/* ---------------------------------------------------------------- Start */

void spiel_start(void)
{
    memset(&K, 0, sizeof K);
    memset(&H, 0, sizeof H);
    K.x = 330;
    K.lp[0] = K.lp[1] = K.lp[2] = LEISTE;
    H.x = -20;
    H.zustand = H_KOMMT;
    H.herzen = H.max_herzen = 1;
    lage = L_KAMPF;
    runde = 1;
    sage("Testszene: □ Richtschlag  △ Sensenzug  ○ Kreisschnitt  ← → gehen", WEISS,
         "Nach dem Tod: zu ihm gehen, ✕ Verbrennen, ○ Umarmen. Select: Neustart.", WEISS);
}

/* ---------------------------------------------------------------- Hilfen */

static int richtung_zum_held(void) { return H.x < K.x ? -1 : 1; }
static int abstand(void) { int d = (int)H.x - K.x; return d < 0 ? -d : d; }
static int held_in_der_luft(void)
{
    if (H.zustand != H_SPRINGT) return 0;
    int b = H.tick / TICKS_JE_BILD;
    return b >= 2 && b <= 6;
}

static int kopfseite(void) { return H.leiche_spiegel ? -1 : 1; }
static int koerper_mitte(void) { return H.leiche_x + kopfseite() * TOD_MITTE; }
static int kniepunkt(void) { return H.leiche_x + kopfseite() * UMARM_ABSTAND; }

static int ritual_moeglich(void)
{
    return !H.verbrannt && H.feuer_tick == 0 && !H.umarm_geht && H.umarm_tick == 0
        && abs(K.x - koerper_mitte()) < 45;
}

static int umarm_ende(void)
{
    int t = 0;
    for (int i = 0; i < 8; i++) t += UMARM_DAUER[i] * TICKS_JE_BILD;
    return t;
}

static int umarm_bild(void)
{
    int t = H.umarm_tick;
    for (int i = 0; i < 8; i++) {
        t -= UMARM_DAUER[i] * TICKS_JE_BILD;
        if (t < 0) return i;
    }
    return 7;
}

static void held_trifft_treffer(int ursache)
{
    if (H.unverwundbar > 0 || H.zustand == H_TOT || H.zustand == H_WEG || H.zustand == H_KOMMT) return;
    if (H.zustand == H_ROLLT) {
        int b = H.tick / TICKS_JE_BILD;
        if (b >= 1 && b <= 5) return;  /* Rolle: Bilder 2-6 unverwundbar */
    }
    if (ursache != ANG_IMPULS && held_in_der_luft() && ursache == ANG_SENSENZUG) return;
    H.getroffen[ursache]++;
    H.letzte_ursache = ursache;
    H.herzen = (ursache == ANG_IMPULS) ? 0 : H.herzen - 1;
    if (H.herzen <= 0) {
        H.zustand = H_TOT;
        H.tick = 0;
        H.tode++;
        H.leiche_x = (int)H.x;
        H.leiche_spiegel = H.x > K.x;   /* fällt nach vorn, zur Königin hin */
        K.blick = H.leiche_spiegel;     /* sie blickt noch zu ihm */
        H.verbrannt = 0;
        H.feuer_tick = 0;
        H.umarm_geht = 0;
        H.umarm_tick = 0;
        H.aufsteh_tick = 0;
        H.zuletzt_umarmt = 0;
        lage = L_RITUAL;
        lage_tick = 0;
        K.zustand = K_BEREIT;
    } else {
        H.zustand = H_GETROFFEN;
        H.tick = 0;
        H.unverwundbar = 60;
    }
}

/* ---------------------------------------------------------------- Held-KI */

/* Plant die Reaktion auf einen Angriff, der gerade beginnt (docs/ANGRIFFE.md, "Lernen des Helden"). */
static void held_plant(int angriff)
{
    if (H.zustand != H_KAMPF && H.zustand != H_HIEBT) return;
    int stufe = H.getroffen[angriff];
    if (stufe == 0) return;                     /* neu: reagiert gar nicht */
    int ideal, art;
    switch (angriff) {
    case ANG_RICHTSCHLAG: ideal = 12; art = H_ROLLT; break;
    case ANG_SENSENZUG: ideal = 15; art = H_SPRINGT; break;
    case ANG_KREISSCHNITT: ideal = 6; art = H_ROLLT; break;
    default: ideal = 90; art = H_SPRINGT; break;     /* Impuls: Welle erreicht ihn etwa bei Tick 105 */
    }
    /* lernend (1-2 Mal getroffen): richtige Art, aber zu früh und bei der Rolle in die falsche
     * Richtung, auf die Königin zu. Ab dem dritten Mal: richtig. */
    int lernend = stufe < 3;
    int zu_frueh = lernend ? (angriff == ANG_IMPULS ? 30 : 15) : 0;
    H.plan_richtung = lernend ? -1 : 1;
    H.plan_tick = ideal - zu_frueh;
    if (H.plan_tick < 0) H.plan_tick = 0;
    H.plan_art = art;
    H.plan_angriff = angriff;
}

static void held_aktion(int art)
{
    H.roll_richtung = H.plan_richtung ? H.plan_richtung : 1;
    H.zustand = art;
    H.tick = 0;
    H.plan_tick = -1;
}

static void held_schritt(void)
{
    if (H.unverwundbar > 0) H.unverwundbar--;
    int rz = richtung_zum_held();
    switch (H.zustand) {
    case H_KOMMT:
        H.x += 1.2f;
        if (H.x >= 90) { H.zustand = H_KAMPF; H.plan_tick = -1; }
        break;
    case H_KAMPF: {
        if (K.zustand == K_VERWANDLUNG) break;     /* während der Verwandlung bleibt er stehen */
        int d = abstand();
        if (d > 40) H.x += (H.x < K.x) ? 1.0f : -1.0f;
        else if (d < 30) H.x -= (H.x < K.x) ? 0.8f : -0.8f;
        else if (K.zustand == K_BEREIT && zuf(40) == 0) { held_aktion(H_HIEBT); H.hieb_getroffen = 0; }
        break;
    }
    case H_HIEBT: {
        H.tick++;
        int b = H.tick / TICKS_JE_BILD;
        if ((b == 4 || b == 5) && !H.hieb_getroffen && abstand() <= 48 && K.zustand != K_VERWANDLUNG) {
            H.hieb_getroffen = 1;
            K.lp[K.phase] -= HIEB_SCHADEN;
        }
        if (H.tick >= 8 * TICKS_JE_BILD) H.zustand = H_KAMPF;
        break;
    }
    case H_ROLLT:
        H.tick++;
        if (H.tick < 6 * TICKS_JE_BILD) H.x += rz * H.roll_richtung * 2.0f;  /* 1 = weg von ihr */
        if (H.tick >= 8 * TICKS_JE_BILD) H.zustand = H_KAMPF;
        break;
    case H_SPRINGT:
        H.tick++;
        if (H.tick >= 8 * TICKS_JE_BILD) H.zustand = H_KAMPF;
        break;
    case H_GETROFFEN:
        H.tick++;
        H.x += rz * 0.6f;
        if (H.tick >= 4 * TICKS_JE_BILD) H.zustand = H_KAMPF;
        break;
    case H_TOT:
        if (H.tick < 8 * TICKS_JE_BILD - 1) H.tick++;
        break;
    }
    if (H.x < H_MIN && H.zustand != H_KOMMT) H.x = H_MIN;
    if (H.x > H_MAX) H.x = H_MAX;
}

/* ---------------------------------------------------------------- Königin */

static const int ANGRIFF_ANIM[3] = {Q_RICHTSCHLAG, Q_SENSENZUG, Q_KREISSCHNITT};
static const int ANGRIFF_BILDER[3] = {10, 14, 14};

static void angriff_pruefen(void)
{
    int b = K.tick / TICKS_JE_BILD;           /* Bild 0-basiert */
    int d = abstand();   /* die Königin blickt immer zum Helden */
    switch (K.angriff) {
    case ANG_RICHTSCHLAG:                      /* Bilder 6-7: vorn, Nahbereich */
        if (b >= 5 && b <= 6 && d <= 60) held_trifft_treffer(ANG_RICHTSCHLAG);
        break;
    case ANG_SENSENZUG:                        /* Bilder 7-9: beim Zurückziehen, bodennah */
        if (b >= 6 && b <= 8 && d >= 15 && d <= 115) held_trifft_treffer(ANG_SENSENZUG);
        break;
    case ANG_KREISSCHNITT:                     /* Bilder 6-9: beidseitig */
        if (b >= 5 && b <= 8 && d <= 62) held_trifft_treffer(ANG_KREISSCHNITT);
        break;
    }
}

static void koenigin_schritt(const Eingabe *e)
{
    int laufen = 0;
    if (e->gedrueckt & PSP_CTRL_LEFT || e->stick_x < -60) laufen = -1;
    if (e->gedrueckt & PSP_CTRL_RIGHT || e->stick_x > 60) laufen = 1;

    switch (K.zustand) {
    case K_BEREIT: {
        int alt = K.x;
        if (H.umarm_geht) {
            /* Sie geht selbst zu ihm, bis sie an seinem Kopf steht */
            int d = kniepunkt() - K.x;
            K.x += (d > 0) - (d < 0);
            if (K.x == kniepunkt()) { H.umarm_geht = 0; H.umarm_tick = 1; }
            K.blick = H.leiche_spiegel;         /* sie blickt zu ihm */
        } else if (H.umarm_tick == 0 && H.aufsteh_tick == 0) {
            K.x += laufen;                      /* während der Umarmung kniet sie */
            if (laufen) K.blick = laufen > 0;
            /* Saalgrenzen: nur nicht weiter hinaus (der Kniepunkt darf außerhalb liegen).
             * Beim Ritual bis an den Rand, damit sie jeden Körper erreicht. */
            int kmin = lage == L_RITUAL ? H_MIN : K_MIN, kmax = lage == L_RITUAL ? H_MAX : K_MAX;
            if ((K.x < kmin && K.x < alt) || (K.x > kmax && K.x > alt)) K.x = alt;
        }
        if (lage == L_KAMPF && H.zustand != H_KOMMT && H.zustand != H_WEG) {
            int neu = -1;
            if (e->neu & PSP_CTRL_SQUARE) neu = ANG_RICHTSCHLAG;
            if (e->neu & PSP_CTRL_TRIANGLE) neu = ANG_SENSENZUG;
            if (e->neu & PSP_CTRL_CIRCLE) neu = ANG_KREISSCHNITT;
            if (neu >= 0) {
                K.zustand = K_ANGRIFF;
                K.angriff = neu;
                K.tick = 0;
                held_plant(neu);
            }
        }
        break;
    }
    case K_ANGRIFF:
        K.tick++;
        angriff_pruefen();
        if (K.tick >= ANGRIFF_BILDER[K.angriff] * TICKS_JE_BILD) K.zustand = K_BEREIT;
        break;
    case K_VERWANDLUNG:
        K.tick++;
        if (K.tick == 1) held_plant(ANG_IMPULS);     /* er sieht die Verwandlung und plant */
        if (K.tick == 100) { ring_tick = 0; impuls_tick = 1; }
        if (K.tick >= 160) {
            K.zustand = K_BEREIT;
            if (H.zustand != H_TOT) {
                sage("Phase 2 folgt in einer späteren Version.", WEISS,
                     "Der Held hat den Impuls überstanden. Der Kampf beginnt von vorn.", WEISS);
                K.lp[0] = K.lp[1] = K.lp[2] = LEISTE;
                K.phase = 0;
            }
        }
        break;
    }
    /* Leiste leer: Verwandlung mit Impuls */
    if (K.zustand != K_VERWANDLUNG && K.phase == 0 && K.lp[0] <= 0 && lage == L_KAMPF) {
        K.lp[0] = 0;
        K.phase = 1;
        K.zustand = K_VERWANDLUNG;
        K.tick = 0;
    }
}

/* ---------------------------------------------------------------- Ablauf */

static void rueckkehr(void)
{
    runde++;
    H.zustand = H_KOMMT;
    H.x = -20;
    H.herzen = H.max_herzen;
    K.lp[0] = K.lp[1] = K.lp[2] = LEISTE;   /* jeder Versuch beginnt mit vollen Leisten */
    K.phase = 0;
    const char *zeile = (runde <= 5) ? WORTE_FRUEH[zuf(4)] : WORTE_MITTE[zuf(4)];
    const char *held = NULL;
    if (H.getroffen[H.letzte_ursache] == 1) held = HELD_ERSTER_TOD[H.letzte_ursache];
    if (H.zuletzt_umarmt && H.umarmungen == 1) held = "„Ich hab geträumt, dass mich jemand festhält. Komisch.“";
    if (zuf(3) != 0 || held) sage(zeile, KOENIGIN_TEXT, held ? held : "", HELD_TEXT);
}

void spiel_schritt(const Eingabe *e)
{
    if (e->neu & PSP_CTRL_SELECT) { spiel_start(); return; }
    if (text_tick > 0) text_tick--;
    lage_tick++;

    koenigin_schritt(e);

    if (lage == L_KAMPF) {
        if (H.plan_tick >= 0 && H.zustand == H_KAMPF) {
            int t = 0;
            (void)t;
        if (K.tick >= H.plan_tick && (K.zustand == K_ANGRIFF || K.zustand == K_VERWANDLUNG)) held_aktion(H.plan_art);
        }
        held_schritt();
        /* Impulswelle läuft vom Körper der Königin über den Boden */
        if (impuls_tick > 0) {
            ring_tick++;
            int radius = 10 + ring_tick * 26 / 5;   /* passt zur gezeichneten Welle (fx_impuls1_ring) */
            if (abs(radius - abstand()) < 8 && !held_in_der_luft()) held_trifft_treffer(ANG_IMPULS);
            if (ring_tick >= 10 * TICKS_JE_BILD) impuls_tick = 0;
        }
    } else if (lage == L_RITUAL) {
        held_schritt();
        /* Königin geht zum Körper; ✕ verbrennt ihn, ○ nimmt ihn in den Arm und verbrennt ihn dort */
        if (ritual_moeglich() && (e->neu & PSP_CTRL_CROSS))
            H.feuer_tick = 1;
        else if (ritual_moeglich() && (e->neu & PSP_CTRL_CIRCLE))
            H.umarm_geht = 1;                  /* sie geht zu seinem Kopf, dann kniet sie */
        if (H.feuer_tick > 0 && ++H.feuer_tick > 90) { H.verbrannt = 1; H.feuer_tick = 0; }
        /* Nach der Umarmung steht sie auf; erst danach nimmt sie die Sense wieder auf */
        if (H.aufsteh_tick > 0 && ++H.aufsteh_tick > 8 * TICKS_JE_BILD) H.aufsteh_tick = 0;
        if (H.umarm_tick > 0 && ++H.umarm_tick > umarm_ende()) {
            H.umarm_tick = 0;
            H.aufsteh_tick = 1;
            H.verbrannt = 1;
            H.zuletzt_umarmt = 1;
            if (++H.umarmungen == 1) sage("„…Du bist leichter, als ich dachte.“", KOENIGIN_TEXT, NULL, 0);
        }
        /* Held kehrt zurück, sobald sie wieder rechts im Saal ist */
        if (H.verbrannt && H.aufsteh_tick == 0 && K.x > 300) {
            if (H.tode == 5 || H.tode == 11) {   /* Quest: Abwesenheit, danach neue Ausrüstung */
                lage = L_ABWESEND;
                lage_tick = 0;
                H.zustand = H_WEG;
            } else {
                lage = L_KAMPF;
                rueckkehr();
            }
        }
    } else if (lage == L_ABWESEND) {
        /* Es geschieht bewusst nichts. */
        if (lage_tick > 60 * 10) {
            H.stufe++;
            H.max_herzen = H.stufe + 1;
            lage = L_KAMPF;
            rueckkehr();
            sage("„Du warst länger fort als sonst.“", KOENIGIN_TEXT,
                 H.stufe == 1 ? "„Neuer Umhang. Zwei Herzen. Diesmal hab ich einen Plan.“"
                              : "„Den hat mir ein Schneider genäht. Lange Geschichte.“", HELD_TEXT);
        }
    }
}

/* ---------------------------------------------------------------- Zeichnen */

static void herz(int x, int y, int voll)
{
    static const char *m[6] = {"0110110", "1111111", "1111111", "0111110", "0011100", "0001000"};
    unsigned int f = voll ? 0xFF3C28E6 : 0xFF463C3C;
    for (int yy = 0; yy < 6; yy++)
        for (int xx = 0; xx < 7; xx++)
            if (m[yy][xx] == '1') rechteck(x + xx, y + yy, 1, 1, f);
}

static void hud(void)
{
    static const unsigned int farbe[3] = {0xFF2828D6, 0xFF1E8CF0, 0xFFFF6EBA};  /* rot, orange, lila */
    int x = 140, y = 10, w = 200, h = 8;
    rechteck(x - 2, y - 2, w + 4, h + 4, 0xFF100608);
    int p = K.phase;
    rechteck(x, y, w, h, p < 2 ? farbe[p + 1] : 0xFF281A1E);
    int lp = K.lp[p] < 0 ? 0 : K.lp[p];
    rechteck(x, y, w * lp / LEISTE, h, farbe[p]);
    for (int i = 0; i < 3; i++) rechteck(x + w + 8 + i * 9, y + 1, 6, 6, i >= p ? farbe[i] : 0xFF403038);
    for (int i = 0; i < H.max_herzen; i++) herz(10 + i * 10, 254, i < H.herzen && H.zustand != H_TOT);
}

static void ring(void)
{
    if (impuls_tick <= 0) return;
    int b = ring_tick / TICKS_JE_BILD;
    zeichne_anim(FX_RING, b, K.x, BODEN + 10, 0, 0, 0xFFFFFFFF);
}

static void textbox(void)
{
    if (text_tick <= 0 || !text_zeile[0]) return;
    rechteck(8, 200, 464, 30, 0xC0100608);
    rechteck(8, 200, 464, 1, 0xFF6E4E5A);
    text(text_zeile[0], 14, 203, text_farbe[0]);
    if (text_zeile[1]) text(text_zeile[1], 14, 216, text_farbe[1]);
}

void spiel_zeichnen(void)
{
    bild_beginnen(0xFF180A0E);
    hintergrund_zeichnen();

    /* Königin */
    int k_spiegel = richtung_zum_held() > 0;
    int k_anim, k_bild;
    if (K.zustand == K_ANGRIFF) { k_anim = ANGRIFF_ANIM[K.angriff]; k_bild = K.tick / TICKS_JE_BILD; }
    else if (K.phase >= 1 || K.zustand == K_VERWANDLUNG) { k_anim = Q_P2_IDLE; k_bild = (lage_tick / TICKS_JE_BILD) % 10; }
    else { k_anim = Q_P1_IDLE; k_bild = (lage_tick / TICKS_JE_BILD / 2) % 6; }
    /* Außerhalb des Kampfs blickt sie in die Richtung, in die sie zuletzt gegangen ist.
     * Beim Umarmen zu ihm: Liegt sein Kopf links, steht sie rechts und blickt nach links. */
    if (lage == L_ABWESEND || lage == L_RITUAL) k_spiegel = K.blick;
    if (H.umarm_tick > 0) { k_anim = Q_UMARMUNG; k_bild = umarm_bild(); }
    if (H.aufsteh_tick > 0) { k_anim = Q_AUFSTEHEN; k_bild = 0; }

    /* Held */
    int h_spiegel = H.x > K.x;
    int clut = H.stufe;
    if (H.zustand == H_TOT) {
        int ls = H.leiche_spiegel;
        /* Das Schwert bleibt liegen, bis er verbrannt ist (bei der Umarmung: bis er zerfällt) */
        if (!H.verbrannt && H.tick / TICKS_JE_BILD >= TOD_SCHWERT_BILD && !(H.umarm_tick > 0 && umarm_bild() == 7))
            zeichne_anim(H_SCHWERT_BODEN, 0, H.leiche_x, BODEN, ls, clut, 0xFFFFFFFF);
        if (!H.verbrannt && H.umarm_tick == 0) zeichne_anim(H_TOD, H.tick / TICKS_JE_BILD, H.leiche_x, BODEN, ls, clut, 0xFFFFFFFF);
        if (H.feuer_tick > 0) zeichne_anim(FX_FEUER, (H.feuer_tick / TICKS_JE_BILD) % 8, koerper_mitte(), BODEN + 2, 0, 0, 0xFFFFFFFF);
    }
    if (H.umarm_tick > 0 || H.aufsteh_tick > 0)
        zeichne_anim(Q_SENSE_BODEN, 0, K.x, BODEN, k_spiegel, 0, 0xFFFFFFFF);  /* abgelegt */
    zeichne_anim(k_anim, k_bild, K.x, BODEN, k_spiegel, 0, 0xFFFFFFFF);
    /* Umhang des Helden in der Umarmung mit der Farbtabelle seiner Ausrüstungsstufe */
    if (H.umarm_tick > 0) zeichne_anim(H_UMARMUNG_UMHANG, k_bild, K.x, BODEN, k_spiegel, clut, 0xFFFFFFFF);
    if (H.zustand != H_TOT && H.zustand != H_WEG) {
        int a = H_IDLE, b = (lage_tick / TICKS_JE_BILD / 2) % 6;
        switch (H.zustand) {
        case H_HIEBT: a = H_HIEB; b = H.tick / TICKS_JE_BILD; break;
        case H_ROLLT: a = H_ROLLE; b = H.tick / TICKS_JE_BILD; break;
        case H_SPRINGT: a = H_SPRUNG; b = H.tick / TICKS_JE_BILD; break;
        case H_GETROFFEN: a = H_TREFFER; b = H.tick / TICKS_JE_BILD; break;
        }
        unsigned int f = (H.unverwundbar > 0 && (H.unverwundbar / 4) % 2) ? 0x80FFFFFF : 0xFFFFFFFF;
        zeichne_anim(a, b, (int)H.x, BODEN, h_spiegel, clut, f);
    }
    ring();
    hud();
    if (lage == L_RITUAL && ritual_moeglich())
        text("✕ Verbrennen  ○ Umarmen", koerper_mitte() - 69, BODEN - 70, WEISS);
    textbox();
    bild_zeigen();
}

#ifdef DEMO
int demo_held_tot(void) { return lage == L_RITUAL; }
int demo_abstand(void) { return abstand(); }
int demo_koenigin_x(void) { return K.x; }
int demo_leiche_x(void) { return H.verbrannt ? 1000 : koerper_mitte(); }
int demo_tode(void) { return H.tode; }
#endif
