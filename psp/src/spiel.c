/* Spielablauf: drei Phasen, lernender Held, Totenritual, Gespräche mit Auswahl, Enden.
 * Werte nach docs/ANGRIFFE.md, docs/SPIELKONZEPT.md und docs/DIALOGE.md.
 * Phase 3 nutzt bis zum Bild der Königin in Phase 3 die eingefärbte Phase-2-Grafik. */
#include <pspctrl.h>
#include <stdlib.h>
#include <string.h>

#include "spiel.h"
#include "grafik.h"
#include "assets_gen.h"
#include "dialoge.h"

#define BODEN 240
#define TPB 5                    /* Logikschritte je Animationsbild (12 Bilder/s bei 60 Schritten/s) */
#define K_MIN 140
#define K_MAX 380
#define K_FREI_MIN 20
#define K_FREI_MAX 460
#define H_MIN 40
#define H_MAX 440
#define HIEB_SCHADEN 4
#define ERHOLUNG 40              /* Pause der Königin nach jedem Angriff (Logikschritte) */
#define ERHOLUNG_MAX 150         /* längste Pause, falls er seinen Gegenschlag nicht anbringt */
#define HIEB_PAUSE 40            /* Abstand zwischen zwei gewöhnlichen Hieben des Helden */
#define RUECKKEHR_STILLE 480     /* nach dem Ritual mindestens 8 s Stille, bevor er zurückkehrt */
/* Phasenwechsel: Schock (sie wankt, der Saal verdunkelt sich), Worte, Aufladen, dann die
 * Welle (Phase 2: Impulsring, Phase 3: Nebel), hinter deren Front der verwandelte Saal erscheint. */
#define V_REDE 60                /* Worte: beim ersten Mal Gespräch, später ein Satz */
#define V_RISS 110               /* Helm reißt (Phase 2) bzw. Wurzelholz (Phase 3) */
#define V_WELLE 150              /* Impulsring bzw. Nebel brechen los */
#define V_ENDE1 240
#define V_ENDE2 250
/* Aus assets_gen.h (tools/cutout/entwuerfe.py): UMARM_ABSTAND = Kniepunkt der Königin vom
 * Fußpunkt des Toten, TOD_MITTE = Mitte des liegenden Körpers, TOD_SCHWERT_BILD = ab diesem
 * Bild liegt das Schwert am Boden. Der Körper liegt mit dem Kopf in Blickrichtung. */

/* Umarmung: Haltezeit je Bild in 12tel Sekunden (animation.json des Entwurfs) */
static const int UMARM_DAUER[8] = {3, 3, 3, 4, 8, 8, 6, 8};

#ifdef DEMO
#define LEISTE 12                /* im Demo-Lauf kürzer, damit alle Phasen vorkommen */
#define G8_AB_RUNDE 3
#define WELT_AB_TICK 120
#define DURCHBRUCH_AB 3
#else
#define LEISTE 60
#define G8_AB_RUNDE 25
#define WELT_AB_TICK (20 * 60)
#define DURCHBRUCH_AB 9          /* Versuche ohne neue Phase, ab denen sein Hieb stärker wird */
#endif

/* Angriffe und Impulse */
enum { A_RICHT, A_SENSE, A_KREIS, A_STERN, A_WIND, A_URTEIL, A_RANKEN, A_RISS, A_WELT, A_IMPULS1, A_IMPULS2, ANG_N };
/* womit der Held einem Angriff entgeht */
enum { SCHUTZ_ROLLE, SCHUTZ_SPRUNG, SCHUTZ_AMULETT, SCHUTZ_KEINER };
enum { AKT_KEINE, AKT_ROLLE, AKT_SPRUNG };

typedef struct { int anim, dauer, schutz, richtig; } AngriffDef;
static const AngriffDef ANG[ANG_N] = {
    {Q_RICHTSCHLAG, 10 * TPB, SCHUTZ_ROLLE, AKT_ROLLE},
    {Q_SENSENZUG, 14 * TPB, SCHUTZ_SPRUNG, AKT_SPRUNG},
    {Q_KREISSCHNITT, 14 * TPB, SCHUTZ_ROLLE, AKT_ROLLE},
    {Q_STERNSCHAUER, 12 * TPB, SCHUTZ_ROLLE, AKT_ROLLE},
    {Q_WINDKLINGE, 10 * TPB + 80, SCHUTZ_SPRUNG, AKT_SPRUNG},
    {Q_TODESURTEIL, 12 * TPB, SCHUTZ_ROLLE, AKT_ROLLE},
    {Q_STERNSCHAUER, 90, SCHUTZ_ROLLE, AKT_ROLLE},     /* Ranken */
    {Q_TODESURTEIL, 30 + 100, SCHUTZ_ROLLE, AKT_ROLLE}, /* Erinnerungsriss */
    {Q_STERNSCHAUER, 150, SCHUTZ_KEINER, AKT_KEINE},    /* Weltgericht: nur das Zögern (G8) rettet ihn */
    {0, 0, SCHUTZ_SPRUNG, AKT_SPRUNG},                   /* Impuls 1 */
    {0, 0, SCHUTZ_AMULETT, AKT_KEINE},                   /* Impuls 2 */
};

enum { KZ_BEREIT, KZ_ANGRIFF, KZ_VERWANDLUNG };
enum { HZ_KOMMT, HZ_KAMPF, HZ_HIEBT, HZ_ROLLT, HZ_SPRINGT, HZ_GETROFFEN, HZ_TOT, HZ_WEG };
enum { L_KAMPF, L_RITUAL, L_ABWESEND, L_GESPRAECH, L_ENDE, L_TITEL, L_INTRO };
enum { R_NICHTS, R_FEUER, R_UMARMEN, R_PORTAL, R_FERTIG };
enum { NACH_KAMPF, NACH_ABWESEND, NACH_WELT, NACH_INTRO };

typedef struct {
    int x, zustand, tick, angriff, phase, blick, verw, phase_tick, welt_benutzt;
    int erholung, erholung_tick;  /* Pause nach einem Angriff; erholung = welcher Angriff (+1) */
    int geht, geh_weg;            /* geht: in diesem Schritt bewegt; geh_weg: Weg in Blickrichtung */
    int lp[3];
    int ziel[3], ziele;          /* Bodenstellen von Flächenangriffen */
    float geschoss;              /* Lichtsichel oder Erinnerungswelle */
    int geschoss_dir, geschoss_aktiv;
} Koenigin;

typedef struct {
    float x;
    int zustand, tick, herzen, stufe, unverwundbar;
    int plan_tick, plan_art, roll_dir, hieb_getroffen;
    int getroffen[ANG_N];
    int tode, tode_p3, ursache, leiche_x, ritual, ritual_tick;
    int leiche_spiegel;           /* 1: er blickte nach links, Kopf liegt links */
    int umarm_geht, aufsteh_tick;
    int hieb_pause, konter;       /* konter: 1 Gegenschlag läuft, 2 angebracht */
    int geht;                     /* in diesem Schritt gegangen (nicht gerollt) */
    int stille;                   /* Schritte seit dem Ende des Rituals */
    float geh_weg;                /* Weg in Blickrichtung, für das Gehen-Bild */
} Held;

static Koenigin K;
static Held H;
static int lage, lage_tick, runde, max_phase, ring_tick, ring_aktiv, ende_nr;
static int seit_fortschritt;     /* Versuche, seit er zuletzt eine neue Phase erreicht hat */
static int vertrauen, einfluss, guide, opfer, umarmt, wirkung_frei;
static int erledigt[GESPRAECHE];
static int erst_ritual[4];
static int quest;                /* 0 = keine, 1..4 = Quest nach diesem Tod */
static int zurueck_von_quest;    /* Gespräch nach der Rückkehr */
static int erster_tod_impuls1;

/* Textanzeige außerhalb von Gesprächen */
static const char *t_zeile[2];
static int t_sprecher[2];
static int t_tick;

/* Eröffnung: der Untertan */
enum { DZ_KOMMT, DZ_KNIET, DZ_STEHT, DZ_TOT, DZ_FORT };
#define D_ZIEL_X 236              /* hier verneigt er sich vor der Königin */
static struct { float x; int zustand, tick; } D;
static const char *const STEUERUNG_1 = "□ △ ○ Angriffe (Phase 3: □ △, L+R Weltgericht)  ← → gehen";
static const char *const STEUERUNG_2 = "Nach dem Tod: ✕ Verbrennen, später ○ Umarmen, □ Opfern. Select: Menü";

/* Hauptmenü */
enum { M_NEU, M_OPTIONEN, M_CREDITS, M_ANZAHL };
enum { S_TITEL, S_MENUE, S_OPTIONEN, S_CREDITS };
static int m_wahl, m_schirm;

/* Gespräch */
static int g_nr, g_schritt, g_wahl, g_antwort, g_nach;
static unsigned int zufall = 12345;
static int zuf(int n) { zufall = zufall * 1103515245u + 12345u; return (zufall >> 16) % n; }

#define FARBE_K 0xFFF8E0E0
#define FARBE_H 0xFFB8F0C8
#define FARBE_V 0xFFFB20EE        /* Magenta #ee20fb (ABGR) */
#define FARBE_E 0xFFB0A8A8
#define FARBE_D 0xFFD8C0C8        /* Untertan: fahles Lila */
#define WEISS 0xFFFFFFFF
#define P3_FARBE 0xFFF8A8E8       /* Platzhalter Phase 3: lila eingefärbt */

static unsigned int farbe_von(int sp)
{
    return sp == SP_KOENIGIN ? FARBE_K : sp == SP_HELD ? FARBE_H : sp == SP_VERDERBNIS ? FARBE_V :
           sp == SP_DIENER ? FARBE_D : FARBE_E;
}

static void sage(const char *a, int sa, const char *b, int sb)
{
    t_zeile[0] = a; t_sprecher[0] = sa;
    t_zeile[1] = b; t_sprecher[1] = sb;
    t_tick = 60 * 5;
}

static int klemme(int v, int lo, int hi) { return v < lo ? lo : v > hi ? hi : v; }

/* ------------------------------------------------------------------ Texte */

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
static const char *const WORTE_SPAET[] = {
    "„Ich zähle nicht mehr, wie oft. Ich merke nur, dass ich warte.“",
    "„Der Ort deines Scheiterns ist dir vertrauter als mir mein Thron.“",
    "„Vielleicht muss man vergehen können, um so wiederzukommen.“",
};
static const char *const WORTE_VERDERBNIS[] = {
    "„Wieder er. Wieder mehr für die Wurzeln.“",
    "„Er kommt, weil er uns gehört.“",
};
static const char *const WORTE_VERTRAUEN[] = {
    "„Du bist zurück. Gut.“",
    "„Ich habe die Stufen gefegt. Ich weiß nicht, warum.“",
};
static const char *const HELD_ERSTER_TOD[ANG_N] = {
    "„Okay. Wenn die Sense oben ist, bin ich nicht mehr vorne.“",
    "„Ich bin dem Wurf ausgewichen. Dem Rückweg nicht.“",
    "„Nah ran war offensichtlich die falsche Idee.“",
    "„Die Markierungen am Boden sind keine Deko.“",
    "„Springen. Man springt über die Sichel.“",
    "„Wenn eine Rune unter mir leuchtet, bleib ich nicht stehen. Notiert.“",
    "„Der Boden selbst ist ein Angriff. Fair.“",
    "„Ich hab kurz was gesehen. Eine Stadt? Dann war ich tot.“",
    "„Da hilft kein Amulett. Da hilft nur, dass sie es nicht tut.“",
    "„Ich hab nichts gemacht. Ich hab nur gewartet.“",
    "„Ich bin gesprungen. Geht hier nicht. Da ist kein Drüber.“",
};
static const char *const VERW_WORTE[2][2] = {
    {"„Noch einmal. Du zwingst mich noch einmal dazu.“", "„Weiche. Oder vergehe.“"},
    {"„Der Nebel kennt dich schon.“", "„Sieh hin. Dann geh.“"},
};
static const char *const HELD_RITUAL[4] = {
    0,
    "„Ich riech nach Rauch. Das ist neu.“",
    "„Ich hab geträumt, dass mich jemand festhält. Komisch.“",
    "„Ich war woanders. Unter den Wurzeln. Da war etwas, das mich kannte.“",
};

/* ------------------------------------------------------------------ Hilfen */

static int dir_zum_held(void) { return H.x < K.x ? -1 : 1; }
/* wie in koenigin_zeichnen: im Kampf zum Helden, sonst in Gehrichtung */
static int koenigin_blickt_rechts(void)
{
    return (lage == L_ABWESEND || lage == L_RITUAL) ? K.blick > 0 : dir_zum_held() > 0;
}
#define GEH_PX 4                  /* Pixel Weg je Gehen-Bild (8 Bilder je Doppelschritt) */
static int geh_bild(float weg) { int b = (int)(weg / GEH_PX) % 8; return b < 0 ? b + 8 : b; }

static int kopfseite(void) { return H.leiche_spiegel ? -1 : 1; }
static int koerper_mitte(void) { return H.leiche_x + kopfseite() * TOD_MITTE; }
static int kniepunkt(void) { return H.leiche_x + kopfseite() * UMARM_ABSTAND; }

#define TOD_LIEGT_BILD 6  /* ab diesem Bild von held_tod liegt er (genau die Pose aus der Umarmung) */
#define ARM_HEBEN 20      /* Phase 2/3: Ticks, bis er in ihren Armen liegt */
#define ARM_HOEHE 24      /* so hoch hält sie ihn (Pixel über dem Boden) */
#define ARM_ABSTAND 4     /* sein Kopf liegt so weit vor ihrer Mitte */

/* Die gezeichnete Umarmung gibt es bisher nur für Phase 1; in Phase 2 und 3 hält sie ihn wie bisher.
 * Zuerst geht sie selbst an seinen Kopf (umarm_geht), dann kniet sie. */
static int umarm_anim(void)
{
    return H.zustand == HZ_TOT && H.ritual == R_UMARMEN && K.phase == 0 && !H.umarm_geht;
}

static int umarm_ende(void)
{
    int t = 0;
    for (int i = 0; i < 8; i++) t += UMARM_DAUER[i] * TPB;
    return t;
}

static int umarm_bild(void)
{
    int t = H.ritual_tick;
    for (int i = 0; i < 8; i++) {
        t -= UMARM_DAUER[i] * TPB;
        if (t < 0) return i;
    }
    return 7;
}
/* Rituale erst, wenn er liegt: sonst würde er mitten im Fallen angehoben bzw. ersetzt */
static int ritual_moeglich(void)
{
    return lage == L_RITUAL && H.ritual == R_NICHTS && H.tick / TPB >= TOD_LIEGT_BILD && K.zustand != KZ_VERWANDLUNG
        && abs(K.x - koerper_mitte()) < 45;
}
static int abstand(void) { int d = (int)H.x - K.x; return d < 0 ? -d : d; }
static int in_der_luft(void)
{
    if (H.zustand != HZ_SPRINGT) return 0;
    int b = H.tick / TPB;
    return b >= 2 && b <= 6;
}
static int rollt_unverwundbar(void)
{
    if (H.zustand != HZ_ROLLT) return 0;
    int b = H.tick / TPB;
    return b >= 1 && b <= 5;
}
static int hat_amulett(void) { return H.stufe >= 3; }

static void gespraech_starten(int nr, int nach);

static void held_stirbt(void)
{
    H.zustand = HZ_TOT;
    H.tick = 0;
    H.tode++;
    if (K.phase == 2) H.tode_p3++;
    H.leiche_x = (int)H.x;
    H.leiche_spiegel = H.x > K.x;   /* fällt nach vorn, zur Königin hin */
    K.blick = H.leiche_spiegel ? 1 : -1;   /* sie blickt noch zu ihm */
    H.umarm_geht = 0;
    H.aufsteh_tick = 0;
    H.ritual = R_NICHTS;
    H.ritual_tick = 0;
    lage = L_RITUAL;
    lage_tick = 0;
    K.geschoss_aktiv = 0;
    if (K.zustand != KZ_VERWANDLUNG) {   /* eine Verwandlung läuft zu Ende, auch wenn er tot ist */
        K.zustand = KZ_BEREIT;
        ring_aktiv = 0;
    }
    /* Quest nach diesem Tod? */
    if (H.ursache == A_IMPULS2 && H.stufe < 3) quest = 3;           /* Amulett */
    else if (H.tode == 5 && H.stufe == 0) quest = 1;
    else if (H.tode == 11 && H.stufe == 1) quest = 2;
    else if (H.tode_p3 >= 3 && H.stufe == 3) quest = 4;               /* goldenes Schwert */
    if (H.ursache == A_IMPULS1 && !erster_tod_impuls1) erster_tod_impuls1 = 1;
}

static void treffer(int a)
{
    if (H.unverwundbar > 0 || H.zustand == HZ_TOT || H.zustand == HZ_WEG || H.zustand == HZ_KOMMT) return;
    int schutz = ANG[a].schutz;
    if (schutz == SCHUTZ_ROLLE && rollt_unverwundbar()) return;
    if (schutz == SCHUTZ_SPRUNG && in_der_luft()) return;
    if (schutz == SCHUTZ_AMULETT && hat_amulett()) return;
    H.getroffen[a]++;
    H.ursache = a;
    int toedlich = (a == A_IMPULS1 || a == A_IMPULS2 || a == A_WELT);
    H.herzen = toedlich ? 0 : H.herzen - 1;
    if (H.herzen <= 0) held_stirbt();
    else { H.zustand = HZ_GETROFFEN; H.tick = 0; H.unverwundbar = 60; }
}

/* ------------------------------------------------------------------ Held-KI */

/* Neu (0 Treffer): keine Reaktion. Lernend (1-2): falsche Art. Ab 3: richtige Art.
 * Die Rolle schützt nicht vor bodennahen Angriffen, der Sprung nicht vor allen anderen. */
static void held_plant(int a, int ideal)
{
    if (H.zustand != HZ_KAMPF && H.zustand != HZ_HIEBT) return;
    H.plan_art = AKT_KEINE;
    int n = H.getroffen[a];
    if (n == 0 || ANG[a].richtig == AKT_KEINE) return;
    int richtig = ANG[a].richtig;
    H.plan_art = (n >= 3) ? richtig : (richtig == AKT_ROLLE ? AKT_SPRUNG : AKT_ROLLE);
    H.plan_tick = ideal < 0 ? 0 : ideal;
}

static void held_handelt(int art)
{
    H.zustand = (art == AKT_ROLLE) ? HZ_ROLLT : HZ_SPRINGT;
    H.tick = 0;
    H.roll_dir = (H.x < K.x) ? -1 : 1;    /* weg von der Königin */
    H.plan_art = AKT_KEINE;
}

static void held_angekommen(void);

/* Ein Angriff, den er sicher beherrscht (ab dem dritten Treffer), lässt ihm in ihrer Erholung
 * immer einen Gegenschlag: Die Pause endet erst, wenn sein Hieb vorbei ist. So kann sie ihn
 * nicht mit pausenlosen Angriffen für immer aufhalten (docs/ANGRIFFE.md, Erholungslücke). */
static int konter_offen(void)
{
    if (!K.erholung || H.konter == 2) return 0;
    int a = K.erholung - 1;
    return ANG[a].richtig != AKT_KEINE && H.getroffen[a] >= 3;
}

/* Steckt er lange ohne neue Phase fest, findet er ihre Lücke: Sein Hieb wird stufenweise stärker. */
static int hieb_schaden(void)
{
    int stufe = seit_fortschritt - DURCHBRUCH_AB;
    if (stufe < 0) stufe = 0;
    if (stufe > 4) stufe = 4;
    return HIEB_SCHADEN + stufe * 2;
}

static void held_schritt(void)
{
    if (H.unverwundbar > 0) H.unverwundbar--;
    float alt_x = H.x;
    int zustand = H.zustand;
    switch (H.zustand) {
    case HZ_KOMMT:
        H.x += 1.2f;
        if (H.x >= 90) { H.zustand = HZ_KAMPF; H.plan_art = AKT_KEINE; held_angekommen(); }
        break;
    case HZ_KAMPF: {
        if (K.zustand == KZ_VERWANDLUNG) break;   /* während der Verwandlung bleibt er stehen */
        int d = abstand();
        int konter = konter_offen();
        if (H.hieb_pause > 0) H.hieb_pause--;
        if (d > 40) H.x += ((H.x < K.x) ? 1.0f : -1.0f) * (konter ? 2.5f : 1.0f);   /* zum Gegenschlag eilt er */
        else if (d < 30) H.x -= (H.x < K.x) ? 0.8f : -0.8f;
        else if (K.zustand == KZ_BEREIT && (konter || H.hieb_pause == 0)) {
            H.zustand = HZ_HIEBT; H.tick = 0; H.hieb_getroffen = 0;
            H.hieb_pause = HIEB_PAUSE;
            if (konter) H.konter = 1;
        }
        break;
    }
    case HZ_HIEBT: {
        H.tick++;
        int b = H.tick / TPB;
        if ((b == 4 || b == 5) && !H.hieb_getroffen && abstand() <= 48 && K.zustand != KZ_VERWANDLUNG) {
            H.hieb_getroffen = 1;
            K.lp[K.phase] -= hieb_schaden();
        }
        if (H.tick >= 8 * TPB) {
            H.zustand = HZ_KAMPF;
            if (H.konter == 1) H.konter = 2;
        }
        break;
    }
    case HZ_ROLLT:
        H.tick++;
        if (H.tick < 6 * TPB) H.x += H.roll_dir * 2.0f;
        if (H.tick >= 8 * TPB) H.zustand = HZ_KAMPF;
        break;
    case HZ_SPRINGT:
        H.tick++;
        if (H.tick >= 8 * TPB) H.zustand = HZ_KAMPF;
        break;
    case HZ_GETROFFEN:
        H.tick++;
        H.x += dir_zum_held() * 0.6f;
        if (H.tick >= 4 * TPB) H.zustand = HZ_KAMPF;
        break;
    case HZ_TOT:
        if (H.tick < 8 * TPB - 1) H.tick++;
        break;
    }
    if (H.x < H_MIN && H.zustand != HZ_KOMMT) H.x = H_MIN;
    if (H.x > H_MAX) H.x = H_MAX;
    /* Gehen: nur aus eigenem Antrieb (Kommen, Kampf), nicht beim Rollen oder Zurückweichen */
    H.geht = (zustand == HZ_KOMMT || zustand == HZ_KAMPF) && H.x != alt_x;
    if (H.geht) H.geh_weg += (H.x > K.x) ? alt_x - H.x : H.x - alt_x;   /* rückwärts, wenn er von ihr weggeht */
}

/* ------------------------------------------------------------------ Angriffe */

static void angriff_starten(int a)
{
    K.zustand = KZ_ANGRIFF;
    K.angriff = a;
    K.tick = 0;
    K.ziele = 0;
    K.geschoss_aktiv = 0;
    int d = abstand();
    int ideal = 0;
    switch (a) {
    case A_RICHT: ideal = 12; break;
    case A_SENSE: ideal = 15; break;
    case A_KREIS: ideal = 16; break;   /* Rolle schützt über das ganze Trefferfenster, auch an der Wand */
    case A_STERN: ideal = 25; break;
    case A_WIND: ideal = 25 + d / 5 - 20; break;
    case A_URTEIL: ideal = 15; break;
    case A_RANKEN: ideal = 45; break;  /* Rolle schützt bei der ersten Stelle; die zweite liegt zur Königin hin */
    case A_RISS: ideal = 30 + d / 5 - 15; break;
    case A_WELT: K.welt_benutzt = 1; break;
    }
    held_plant(a, ideal);
}

static void angriff_schritt(void)
{
    int t = ++K.tick;
    int d = abstand();
    int weg = dir_zum_held();     /* von der Königin aus gesehen: Richtung zum Helden */
    switch (K.angriff) {
    case A_RICHT:
        if (t >= 25 && t <= 34 && d <= 60) treffer(A_RICHT);
        break;
    case A_SENSE:
        if (t >= 30 && t <= 44 && d >= 15 && d <= 115) treffer(A_SENSE);
        break;
    case A_KREIS:
        if (t >= 25 && t <= 44 && d <= 62) treffer(A_KREIS);
        break;
    case A_STERN:
        if (t == 10) {
            K.ziel[0] = (int)H.x; K.ziel[1] = (int)H.x - weg * 50; K.ziel[2] = (int)H.x + weg * 110; K.ziele = 3;
        }
        if (t == 50)
            for (int i = 0; i < K.ziele; i++) if (abs((int)H.x - K.ziel[i]) < 15) treffer(A_STERN);
        break;
    case A_WIND:
        if (t == 25) { K.geschoss = K.x; K.geschoss_dir = weg; K.geschoss_aktiv = 1; }
        if (K.geschoss_aktiv) {
            K.geschoss += K.geschoss_dir * 5;
            if (abs((int)K.geschoss - (int)H.x) < 10) treffer(A_WIND);
            if (K.geschoss < 0 || K.geschoss > 480) K.geschoss_aktiv = 0;
        }
        break;
    case A_URTEIL:
        if (t == 10) { K.ziel[0] = (int)H.x; K.ziele = 1; }
        if (t >= 30 && t <= 44 && K.ziele && abs((int)H.x - K.ziel[0]) < 26) treffer(A_URTEIL);
        break;
    case A_RANKEN:
        if (t == 10) { K.ziel[0] = (int)H.x; K.ziel[1] = (int)H.x - weg * 40; K.ziele = 2; }
        if (t >= 50 && t <= 64 && abs((int)H.x - K.ziel[0]) < 12) treffer(A_RANKEN);
        if (t >= 70 && t <= 84 && abs((int)H.x - K.ziel[1]) < 12) treffer(A_RANKEN);
        break;
    case A_RISS:
        if (t == 30) { K.geschoss = K.x; K.geschoss_dir = weg; K.geschoss_aktiv = 1; }
        if (K.geschoss_aktiv) {
            K.geschoss += K.geschoss_dir * 5;
            if (abs((int)K.geschoss - (int)H.x) < 8) treffer(A_RISS);
            if (K.geschoss < 0 || K.geschoss > 480) K.geschoss_aktiv = 0;
        }
        break;
    case A_WELT:
        if (t == 100 && runde >= G8_AB_RUNDE && vertrauen >= 1 && !erledigt[G_G8]) {
            gespraech_starten(G_G8, NACH_WELT);
            return;
        }
        if (t == 120) treffer(A_WELT);
        break;
    }
    if (t >= ANG[K.angriff].dauer) {
        K.zustand = KZ_BEREIT;
        K.geschoss_aktiv = 0;
        K.erholung = K.angriff + 1;
        K.erholung_tick = 0;
        H.konter = 0;
    }
}

/* ------------------------------------------------------------------ Verwandlung */

static void verwandlung_starten(int v)
{
    K.zustand = KZ_VERWANDLUNG;
    K.verw = v;
    K.tick = 0;
    /* Die Verwandlung beendet ihre Erholung; danach greift sie ohne Pause wieder an */
    K.erholung = 0;
    H.konter = 0;
    H.plan_art = AKT_KEINE;
    if (v == 1) held_plant(A_IMPULS1, V_WELLE - 10);   /* der Ring erreicht ihn etwa 5 Schritte nach V_WELLE */
}

/* Nach der Welle: verwandelt, auch wenn er gestorben ist (dann beginnt das Ritual danach) */
static void verwandlung_fertig(int phase)
{
    K.zustand = KZ_BEREIT;
    K.phase = phase;
    K.phase_tick = 0;
    if (phase == 2) K.welt_benutzt = 0;
    if (lage != L_KAMPF) return;
    if (max_phase < phase) { max_phase = phase; seit_fortschritt = 0; }
    int g = phase == 1 ? G_G6 : G_G7;
    if (!erledigt[g]) gespraech_starten(g, NACH_KAMPF);
}

static void verwandlung_schritt(void)
{
    int t = ++K.tick;
    if (t == V_REDE) {
        int g = K.verw == 1 ? G_VERW1 : G_VERW2;
        if (!erledigt[g] && lage == L_KAMPF) { gespraech_starten(g, NACH_KAMPF); return; }
        sage(VERW_WORTE[K.verw - 1][zuf(2)], einfluss >= 3 ? SP_VERDERBNIS : SP_KOENIGIN, "", SP_HELD);
    }
    if (K.verw == 1) {
        if (t == V_WELLE) { ring_aktiv = 1; ring_tick = 0; }
        if (ring_aktiv) {
            ring_tick++;
            int radius = 10 + ring_tick * 26 / 5;
            if (abs(radius - abstand()) < 8) treffer(A_IMPULS1);
            if (ring_tick >= 10 * TPB) ring_aktiv = 0;
        }
        if (t >= V_ENDE1) verwandlung_fertig(1);
    } else {
        if (t == V_WELLE + 50) treffer(A_IMPULS2);   /* der Nebel hat ihn erreicht */
        if (t >= V_ENDE2) verwandlung_fertig(2);
    }
}

/* ------------------------------------------------------------------ Gespräche */

static int wahl_erlaubt(const Wahl *w) { return w->bedingung == 0 || vertrauen >= 2; }

static void gespraech_starten(int nr, int nach)
{
    g_nr = nr;
    g_schritt = 0;
    g_wahl = 0;
    g_antwort = 0;
    g_nach = nach;
    lage = L_GESPRAECH;
    erledigt[nr] = 1;
    wirkung_frei = 1;   /* Ritual darf zwischen zwei Gesprächen wieder einmal wirken */
    t_tick = 0;
}

static void ende_setzen(int nr) { ende_nr = nr; lage = L_ENDE; }

static int ende_nach_werten(void)
{
    if (vertrauen >= 3 && einfluss <= 1 && umarmt >= 3) return 5;
    if (vertrauen >= 2 && einfluss <= 2) return 3;
    return 6;
}

static void abwesenheit_starten(void)
{
    lage = L_ABWESEND;
    lage_tick = 0;
    H.zustand = HZ_WEG;
}

static void gespraech_ende(void)
{
    const Gespraech *g = &GESPRAECH[g_nr];
    if (g_nach == NACH_INTRO) { lage = L_INTRO; D.zustand = DZ_STEHT; D.tick = 0; return; }
    if (g_nr == G_G1) sage(STEUERUNG_1, SP_ERZAEHLER, STEUERUNG_2, SP_ERZAEHLER);   /* jetzt beginnt der Kampf */
    if (g->anzahl_wahl == 0) { lage = L_KAMPF; return; }
    const Wahl *w = &g->wahl[g_wahl];
    if (w->ende == 9) { ende_setzen(ende_nach_werten()); return; }
    if (w->ende) { ende_setzen(w->ende); return; }
    if (g_nach == NACH_ABWESEND) { abwesenheit_starten(); return; }
    lage = L_KAMPF;
    /* NACH_WELT: Endboss-Antwort, das Weltgericht wird entladen; der Angriff läuft weiter */
}

static void gespraech_schritt(const Eingabe *e)
{
    const Gespraech *g = &GESPRAECH[g_nr];
    if (g_schritt < g->anzahl_zeilen) {
        if (e->neu & PSP_CTRL_CROSS) g_schritt++;
        return;
    }
    if (g->anzahl_wahl == 0) { gespraech_ende(); return; }
    if (!g_antwort) {
        int n = g->anzahl_wahl;
        if (e->neu & PSP_CTRL_DOWN) do { g_wahl = (g_wahl + 1) % n; } while (!wahl_erlaubt(&g->wahl[g_wahl]));
        if (e->neu & PSP_CTRL_UP) do { g_wahl = (g_wahl + n - 1) % n; } while (!wahl_erlaubt(&g->wahl[g_wahl]));
        if (e->neu & PSP_CTRL_CROSS) {
            const Wahl *w = &g->wahl[g_wahl];
            vertrauen = klemme(vertrauen + w->vertrauen, -3, 3);
            einfluss = klemme(einfluss + w->einfluss, 0, 5);
            guide += w->guide;
            if (w->antwort) g_antwort = 1;
            else gespraech_ende();
        }
        return;
    }
    if (e->neu & PSP_CTRL_CROSS) gespraech_ende();
}

/* ------------------------------------------------------------------ Ablauf */

static void held_angekommen(void)
{
    if (runde == 1 && !erledigt[G_G1]) { gespraech_starten(G_G1, NACH_KAMPF); return; }
    if (zurueck_von_quest) {
        int nr = zurueck_von_quest == 1 ? G_G4 : zurueck_von_quest == 2 ? G_R2 : zurueck_von_quest == 3 ? G_R3 : G_R4;
        zurueck_von_quest = 0;
        if (!erledigt[nr]) { gespraech_starten(nr, NACH_KAMPF); return; }
    }
    if (erster_tod_impuls1 && !erledigt[G_G5]) { gespraech_starten(G_G5, NACH_KAMPF); return; }
    if (H.tode == 3 && !erledigt[G_G2]) { gespraech_starten(G_G2, NACH_KAMPF); return; }
    /* Er steckt fest und gibt der Mechanik die Schuld; die Endboss-Antwort führt zu E1 */
    if (seit_fortschritt > DURCHBRUCH_AB && !erledigt[G_PATCH]) { gespraech_starten(G_PATCH, NACH_KAMPF); return; }
}

static void rueckkehr(void)
{
    runde++;
    seit_fortschritt++;
    K.erholung = 0;
    H.konter = 0;
    H.hieb_pause = 0;
    H.zustand = HZ_KOMMT;
    H.x = -20;
    H.herzen = H.stufe + 1;
    K.lp[0] = K.lp[1] = K.lp[2] = LEISTE;   /* jeder Versuch beginnt mit vollen Leisten */
    K.phase = 0;
    K.zustand = KZ_BEREIT;
    if (K.x < K_MIN) K.x = K_MIN;
    if (K.x > K_MAX) K.x = K_MAX;
    lage = L_KAMPF;

    /* Worte der Königin, vorrangig; der Held antwortet nur bei Anlass */
    const char *k = 0;
    int ks = SP_KOENIGIN;
    if (einfluss >= 3 && zuf(2)) { k = WORTE_VERDERBNIS[zuf(2)]; ks = SP_VERDERBNIS; }
    else if (vertrauen >= 2 && zuf(2)) k = WORTE_VERTRAUEN[zuf(2)];
    else if (max_phase >= 2) k = WORTE_SPAET[zuf(3)];
    else if (runde <= 5) k = WORTE_FRUEH[zuf(4)];
    else k = WORTE_MITTE[zuf(4)];
    const char *h = 0;
    if (H.ritual >= R_FEUER && H.ritual <= R_PORTAL && !erst_ritual[H.ritual]) {
        erst_ritual[H.ritual] = 1;
        h = HELD_RITUAL[H.ritual];
    } else if (H.getroffen[H.ursache] == 1) {
        h = HELD_ERSTER_TOD[H.ursache];
    }
    if (h || zuf(3)) sage(k, ks, h ? h : "", SP_HELD);
}

static void ritual_schritt(const Eingabe *e)
{
    if (ritual_moeglich()) {
        int umarmen = erledigt[G_G2] && vertrauen >= 0;
        int portal = erledigt[G_G5];
        if (e->neu & PSP_CTRL_CROSS) { H.ritual = R_FEUER; H.ritual_tick = 0; }
        else if (umarmen && (e->neu & PSP_CTRL_CIRCLE)) {
            H.ritual = R_UMARMEN; H.ritual_tick = 0; umarmt++;
            if (K.phase == 0) H.umarm_geht = 1;   /* sie geht zu seinem Kopf, dann kniet sie */
            if (wirkung_frei) { vertrauen = klemme(vertrauen + 1, -3, 3); wirkung_frei = 0; }
            if (!erst_ritual[R_UMARMEN]) sage("„…Du bist leichter, als ich dachte.“", SP_KOENIGIN, "", SP_HELD);
        } else if (portal && (e->neu & PSP_CTRL_SQUARE)) {
            H.ritual = R_PORTAL; H.ritual_tick = 0; opfer++;
            if (wirkung_frei) { einfluss = klemme(einfluss + 1, 0, 5); wirkung_frei = 0; }
            if (!erst_ritual[R_PORTAL]) sage("„Endlich. Gib ihn mir. Alle, die kommen.“", SP_VERDERBNIS, "", SP_HELD);
        }
        if (H.ritual == R_FEUER && !erst_ritual[R_FEUER])
            sage("„Brenne. Und werde erinnert.“", SP_KOENIGIN, "", SP_HELD);
    }
    /* Nach der Umarmung steht sie auf; erst danach nimmt sie die Sense wieder auf */
    if (H.aufsteh_tick > 0 && ++H.aufsteh_tick > 8 * TPB) H.aufsteh_tick = 0;
    if (H.ritual > R_NICHTS && H.ritual < R_FERTIG && !H.umarm_geht) {
        H.ritual_tick++;
        int dauer = H.ritual == R_UMARMEN ? (K.phase == 0 ? umarm_ende() : 150) : H.ritual == R_PORTAL ? 12 * TPB + 20 : 90;
        if (H.ritual_tick >= dauer) {
            if (H.ritual == R_PORTAL && einfluss >= 5 && opfer >= 3) { ende_setzen(2); return; }
            if (umarm_anim()) H.aufsteh_tick = 1;
            H.ritual_tick = H.ritual;   /* merkt sich die Art für den Rückkehrkommentar */
            H.ritual = R_FERTIG;
            H.stille = 0;
        }
    }
    /* Der Held kehrt zurück, sobald sie wieder rechts im Saal ist */
    if (H.ritual == R_FERTIG) H.stille++;
    if (H.ritual == R_FERTIG && H.aufsteh_tick == 0 && K.x > 300 && H.stille >= RUECKKEHR_STILLE) {
        H.ritual = H.ritual_tick;
        if (quest) {
            int q = quest;
            /* Er ist fort: Sonst würde während G3 das Ritual noch einmal gezeichnet */
            H.zustand = HZ_WEG;
            if (q == 1) gespraech_starten(G_G3, NACH_ABWESEND);
            else {
                if (q == 3) sage("„Okay. Springen reicht nicht mehr. Ich brauch was, das mich schützt.“", SP_HELD,
                                 "„Bin bald zurück. Also, relativ bald.“", SP_HELD);
                abwesenheit_starten();
            }
        } else {
            rueckkehr();
        }
    }
}

/* ------------------------------------------------------------------ Start und Schritt */

void spiel_start(void)
{
    memset(&K, 0, sizeof K);
    memset(&H, 0, sizeof H);
    memset(erledigt, 0, sizeof erledigt);
    memset(erst_ritual, 0, sizeof erst_ritual);
    K.x = 330;
    K.blick = -1;
    K.lp[0] = K.lp[1] = K.lp[2] = LEISTE;
    H.x = -20;
    H.zustand = HZ_WEG;          /* er kommt erst nach dem Untertan */
    H.herzen = 1;
    lage = L_INTRO;
    lage_tick = 0;
    D.x = -20; D.zustand = DZ_KOMMT; D.tick = 0;
    runde = 1;
    max_phase = 0;
    seit_fortschritt = 0;
    vertrauen = 0; einfluss = 2; guide = 0; opfer = 0; umarmt = 0; wirkung_frei = 1;
    quest = 0; zurueck_von_quest = 0; erster_tod_impuls1 = 0; ende_nr = 0; ring_aktiv = 0;
    t_tick = 0;
}

static void intro_ende(void)
{
    lage = L_KAMPF;
    H.zustand = HZ_KOMMT;   /* steht schon im Saal: im nächsten Schritt Kampf und Gespräch G1 */
    if (D.zustand != DZ_TOT) D.zustand = DZ_FORT;
}

/* Der Untertan kommt, verneigt sich und warnt sie (Gespräch), dann kommt der Held und erschlägt ihn. */
static void intro_schritt(const Eingabe *e)
{
    if (e->neu & PSP_CTRL_START) { H.x = H.x < 60 ? 60 : H.x; intro_ende(); return; }   /* überspringen */
    D.tick++;
    switch (D.zustand) {
    case DZ_KOMMT:
        D.x += 1.4f;
        if (D.x >= D_ZIEL_X) { D.x = D_ZIEL_X; D.zustand = DZ_KNIET; D.tick = 0; }
        break;
    case DZ_KNIET:
        if (D.tick == 50) gespraech_starten(G_INTRO, NACH_INTRO);
        break;
    case DZ_STEHT:
        /* Er richtet sich auf und wendet sich dem Eingang zu; der Held tritt ein */
        if (H.zustand == HZ_WEG && D.tick > 20) { H.zustand = HZ_KOMMT; H.x = -20; }
        if (H.zustand == HZ_KOMMT) {
            float alt = H.x;
            H.x += 1.6f;
            H.geht = 1;
            H.geh_weg += H.x - alt;
            if (H.x >= D.x - 36) { H.zustand = HZ_HIEBT; H.tick = 0; }
        } else if (H.zustand == HZ_HIEBT) {
            H.tick++;
            if (H.tick == 4 * TPB) { D.zustand = DZ_TOT; D.tick = 0; }
        }
        break;
    case DZ_TOT:
        if (H.zustand == HZ_HIEBT && ++H.tick >= 8 * TPB) {
            H.zustand = HZ_KAMPF;
            sage("„Tutorial-Gegner. Erledigt.“", SP_HELD, "", SP_HELD);
        }
        if (D.tick >= 110) intro_ende();
        break;
    }
}

static void koenigin_schritt(const Eingabe *e)
{
    int laufen = 0;
    if (e->gedrueckt & PSP_CTRL_LEFT || e->stick_x < -60) laufen = -1;
    if (e->gedrueckt & PSP_CTRL_RIGHT || e->stick_x > 60) laufen = 1;
    K.phase_tick++;
    int alt_x = K.x;
    switch (K.zustand) {
    case KZ_BEREIT:
        /* Erholung nach einem Angriff: Sie steht still und greift nicht an. Beherrscht er den
         * Angriff sicher, dauert sie, bis sein Gegenschlag vorbei ist (höchstens ERHOLUNG_MAX). */
        if (K.erholung) {
            int lebt = H.zustand != HZ_TOT && H.zustand != HZ_WEG && H.zustand != HZ_KOMMT;
            int halten = lebt && konter_offen();
            if (lage != L_KAMPF || ++K.erholung_tick >= ERHOLUNG_MAX || (K.erholung_tick >= ERHOLUNG && !halten))
                K.erholung = 0;
        }
        if (K.erholung) laufen = 0;
        if (H.zustand == HZ_TOT && H.umarm_geht) {
            /* Sie geht selbst zu ihm, bis sie an seinem Kopf steht */
            int d = kniepunkt() - K.x;
            laufen = (d > 0) - (d < 0);
            if (!laufen) H.umarm_geht = 0;
        } else if (umarm_anim() || H.aufsteh_tick) {
            laufen = 0;                         /* während der Umarmung kniet sie */
        }
        K.x += laufen;
        if (H.zustand == HZ_TOT && H.umarm_geht) K.blick = H.leiche_spiegel ? 1 : -1;   /* sie blickt zu ihm */
        else if (laufen) K.blick = laufen;
        if (lage == L_KAMPF && !K.erholung && H.zustand != HZ_KOMMT && H.zustand != HZ_WEG && H.zustand != HZ_TOT) {
            int a = -1;
            static const int TASTE_ANGRIFF[3][3] = {
                {A_RICHT, A_SENSE, A_KREIS}, {A_STERN, A_WIND, A_URTEIL}, {A_RANKEN, A_RISS, -1}};
            if (e->neu & PSP_CTRL_SQUARE) a = TASTE_ANGRIFF[K.phase][0];
            if (e->neu & PSP_CTRL_TRIANGLE) a = TASTE_ANGRIFF[K.phase][1];
            if (e->neu & PSP_CTRL_CIRCLE) a = TASTE_ANGRIFF[K.phase][2];
            if (K.phase == 2 && (e->gedrueckt & PSP_CTRL_LTRIGGER) && (e->gedrueckt & PSP_CTRL_RTRIGGER) &&
                !K.welt_benutzt && K.phase_tick >= WELT_AB_TICK)
                a = A_WELT;
            if (a >= 0) angriff_starten(a);
        }
        break;
    case KZ_ANGRIFF:
        angriff_schritt();
        break;
    case KZ_VERWANDLUNG:
        verwandlung_schritt();
        break;
    }
    int frei = (lage != L_KAMPF);
    int lo = frei ? K_FREI_MIN : K_MIN, hi = frei ? K_FREI_MAX : K_MAX;
    /* Der Kniepunkt an einem Körper am Saalrand darf außerhalb liegen */
    if (!(H.zustand == HZ_TOT && (H.umarm_geht || umarm_anim() || H.aufsteh_tick))) {
        if (K.x < lo) K.x = lo;
        if (K.x > hi) K.x = hi;
    }

    K.geht = K.x != alt_x;
    if (K.geht) K.geh_weg += (K.x - alt_x) * (koenigin_blickt_rechts() ? 1 : -1);

    if (lage == L_KAMPF && K.zustand != KZ_VERWANDLUNG && K.lp[K.phase] <= 0) {
        K.lp[K.phase] = 0;
        if (K.phase == 0) verwandlung_starten(1);
        else if (K.phase == 1) verwandlung_starten(2);
        else ende_setzen(ende_nach_werten());   /* der Held hat sie besiegt */
    }
}

void spiel_titel(void)
{
    D.zustand = DZ_FORT;
    lage = L_TITEL;
    lage_tick = 0;
    m_wahl = M_NEU;
    m_schirm = S_TITEL;
    t_tick = 0;
}

/* Bildschirme vor dem Spiel: Titel ("Start drücken"), Hauptmenü, Optionen, Credits */
static void titel_schritt(const Eingabe *e)
{
    if (lage_tick < 30) return;   /* kurzes Einblenden, bevor etwas reagiert */
    int weiter = e->neu & (PSP_CTRL_CROSS | PSP_CTRL_START);
    int zurueck = e->neu & PSP_CTRL_CIRCLE;
    switch (m_schirm) {
    case S_TITEL:
        if (weiter) { m_schirm = S_MENUE; m_wahl = M_NEU; }
        break;
    case S_MENUE:
        if (e->neu & PSP_CTRL_UP) m_wahl = (m_wahl + M_ANZAHL - 1) % M_ANZAHL;
        if (e->neu & PSP_CTRL_DOWN) m_wahl = (m_wahl + 1) % M_ANZAHL;
        if (zurueck) m_schirm = S_TITEL;
        else if (weiter) {
            if (m_wahl == M_NEU) spiel_start();
            else m_schirm = m_wahl == M_OPTIONEN ? S_OPTIONEN : S_CREDITS;
        }
        break;
    default:
        if (weiter || zurueck) m_schirm = S_MENUE;
        break;
    }
}

void spiel_schritt(const Eingabe *e)
{
    if (lage == L_TITEL) { lage_tick++; titel_schritt(e); return; }
    if (e->neu & PSP_CTRL_SELECT) { spiel_titel(); return; }
    if (t_tick > 0) t_tick--;
    lage_tick++;
    if (D.zustand == DZ_TOT && lage != L_INTRO && lage != L_GESPRAECH && ++D.tick > 400) D.zustand = DZ_FORT;
    K.geht = 0;   /* wird in koenigin_schritt bzw. held_schritt neu gesetzt */
    H.geht = 0;

    switch (lage) {
    case L_ENDE:
        return;
    case L_INTRO:
        intro_schritt(e);
        return;
    case L_GESPRAECH:
        gespraech_schritt(e);
        return;
    case L_KAMPF:
        koenigin_schritt(e);
        if (lage != L_KAMPF) return;
        if (H.plan_art != AKT_KEINE && H.zustand == HZ_KAMPF &&
            (K.zustand == KZ_ANGRIFF || K.zustand == KZ_VERWANDLUNG) && K.tick >= H.plan_tick)
            held_handelt(H.plan_art);
        held_schritt();
        break;
    case L_RITUAL:
        koenigin_schritt(e);
        held_schritt();
        ritual_schritt(e);
        break;
    case L_ABWESEND:
        koenigin_schritt(e);   /* sie kann gehen; es geschieht bewusst nichts */
        if (lage_tick > 60 * 10) {
            H.stufe = quest == 1 ? 1 : quest == 2 ? 2 : quest == 3 ? 3 : 4;
            zurueck_von_quest = quest;
            quest = 0;
            rueckkehr();
            t_tick = 0;   /* das Gespräch nach der Quest ersetzt die Rückkehrworte */
        }
        break;
    }
}

/* ------------------------------------------------------------------ Zeichnen */

static void herz(int x, int y, int voll)
{
    static const char *m[6] = {"0110110", "1111111", "1111111", "0111110", "0011100", "0001000"};
    unsigned int f = voll ? 0xFF3C28E6 : 0xFF463C3C;
    for (int yy = 0; yy < 6; yy++)
        for (int xx = 0; xx < 7; xx++)
            if (m[yy][xx] == '1') rechteck(x + xx, y + yy, 1, 1, f);
}

static int im_kampf(void)
{
    return lage == L_KAMPF && H.zustand != HZ_KOMMT && H.zustand != HZ_WEG && H.zustand != HZ_TOT;
}

static void hud(void)
{
    static const unsigned int farbe[3] = {0xFF2828D6, 0xFF1E8CF0, 0xFFFF6EBA};
    if (im_kampf()) {
        int x = 140, y = 10, w = 200, h = 8, p = K.phase;
        rechteck(x - 2, y - 2, w + 4, h + 4, 0xFF100608);
        rechteck(x, y, w, h, p < 2 ? farbe[p + 1] : 0xFF281A1E);
        int lp = K.lp[p] < 0 ? 0 : K.lp[p];
        rechteck(x, y, w * lp / LEISTE, h, farbe[p]);
        for (int i = 0; i < 3; i++) rechteck(x + w + 8 + i * 9, y + 1, 6, 6, i >= p ? farbe[i] : 0xFF403038);
    }
    if (lage != L_ABWESEND && lage != L_INTRO && H.zustand != HZ_WEG)
        for (int i = 0; i < H.stufe + 1; i++) herz(10 + i * 10, 254, i < H.herzen && H.zustand != HZ_TOT);
}

/* Text mit Zeilenumbruch in einer Box oben mittig */
/* Text mit Zeilenumbruch im Bereich x0 .. x0 + breite: zentriert oder (auswahl) linksbündig */
static int zeilen_bereich(const char *s, int sprecher, int y, int x0, int breite, int auswahl)
{
    const char *st[3];
    int ln[3];
    int n = umbrechen(s, breite / SCHRIFT_ZW, st, ln, 3);
    char puffer[200];
    for (int i = 0; i < n; i++) {
        int l = ln[i] < 199 ? ln[i] : 199;
        memcpy(puffer, st[i], l);
        puffer[l] = 0;
        int b = zeichen_anzahl(puffer) * SCHRIFT_ZW;
        int x = auswahl ? x0 : x0 + (breite - b) / 2;
        text_stil(puffer, x, y + i * 12, farbe_von(sprecher), sprecher == SP_VERDERBNIS);
    }
    return n;
}

static int zeilen_zeichnen(const char *s, int sprecher, int y, int auswahl)
{
    return auswahl ? zeilen_bereich(s, sprecher, y, 30, 432, 1) : zeilen_bereich(s, sprecher, y, 24, 432, 0);
}

/* Porträt der sprechenden Figur links in der Dialogbox (48 x 48) */
static void portrait(int sprecher, int x, int y)
{
    int anim, clut = 0;
    unsigned int f = WEISS;
    switch (sprecher) {
    case SP_KOENIGIN: anim = Q_PORTRAIT; break;
    case SP_VERDERBNIS: anim = Q_PORTRAIT; f = 0xFFFF60F0; break;   /* magenta eingefärbt */
    case SP_HELD: anim = H_PORTRAIT; clut = H.stufe; break;
    case SP_DIENER: anim = D_PORTRAIT; break;
    default: return;
    }
    rechteck(x - 2, y - 2, 52, 52, sprecher == SP_VERDERBNIS ? 0xFFFB20EE : 0xFF6E4E5A);
    zeichne_anim(anim, 0, x, y, 0, clut, f);
}

static void textbox(void)
{
    if (t_tick <= 0 || !t_zeile[0]) return;
    int h = (t_zeile[1] && t_zeile[1][0]) ? 30 : 17;
    rechteck(8, 24, 464, h, 0xC0100608);
    rechteck(8, 24 + h - 1, 464, 1, 0xFF6E4E5A);
    zeilen_zeichnen(t_zeile[0], t_sprecher[0], 27, 0);
    if (t_zeile[1] && t_zeile[1][0]) zeilen_zeichnen(t_zeile[1], t_sprecher[1], 40, 0);
}

static void gespraech_zeichnen(void)
{
    const Gespraech *g = &GESPRAECH[g_nr];
    rechteck(8, 24, 464, 68, 0xD8100608);
    rechteck(8, 91, 464, 1, 0xFF6E4E5A);
    /* links das Porträt, rechts daneben der Text */
    if (g_schritt < g->anzahl_zeilen) {
        const Zeile *z = &g->zeilen[g_schritt];
        portrait(z->sprecher, 16, 32);
        zeilen_bereich(z->text, z->sprecher, 34, 72, 384, 0);
        text("✕", 458, 78, 0xFF808080);
        return;
    }
    if (!g_antwort) {
        portrait(g->wahl[g_wahl].sprecher, 16, 32);
        int y = 30;
        for (int i = 0; i < g->anzahl_wahl; i++) {
            const Wahl *w = &g->wahl[i];
            if (!wahl_erlaubt(w)) continue;
            if (i == g_wahl) text("▶", 72, y, WEISS);
            int n = zeilen_bereich(w->satz, w->sprecher, y, 86, 378, 1);
            if (i != g_wahl) rechteck(84, y - 1, 384, n * 12 + 1, 0x70100608);   /* nicht gewählte abdunkeln */
            y += n * 12 + 4;
        }
        return;
    }
    portrait(SP_HELD, 16, 32);
    zeilen_bereich(g->wahl[g_wahl].antwort, SP_HELD, 34, 72, 384, 0);
    text("✕", 458, 78, 0xFF808080);
}

static void ende_zeichnen(void)
{
    const Ende *e = &ENDEN[ende_nr];
    rechteck(0, 0, BILD_B, BILD_H, 0xE0080406);
    char titel[80];
    titel[0] = 0;
    strcat(titel, "Ende: ");
    strncat(titel, e->titel, 70);
    text(titel, (BILD_B - zeichen_anzahl(titel) * SCHRIFT_ZW) / 2, 80, 0xFFFF6EBA);
    for (int i = 0; i < 4 && e->zeilen[i]; i++)
        text(e->zeilen[i], (BILD_B - zeichen_anzahl(e->zeilen[i]) * SCHRIFT_ZW) / 2, 110 + i * 14,
             e->zeilen[i][0] == (char)0xE2 ? FARBE_H : WEISS);
    text("Select: Hauptmenü", (BILD_B - 17 * SCHRIFT_ZW) / 2, 200, 0xFF808080);
}

static void effekte_zeichnen(void)
{
    if (K.zustand != KZ_ANGRIFF) return;
    int t = K.tick, b = (t / TPB);
    switch (K.angriff) {
    case A_STERN:
        for (int i = 0; i < K.ziele; i++) {
            if (t < 50) zeichne_anim(FX_KREIS, b % 4, K.ziel[i], BODEN, 0, 0, WEISS);
            if (t >= 38 && t < 50) zeichne_anim(FX_STERN, b % 4, K.ziel[i], BODEN - (50 - t) * 12, 0, 0, WEISS);
            if (t >= 50 && t < 70) zeichne_anim(FX_EINSCHLAG, (t - 50) / TPB, K.ziel[i], BODEN, 0, 0, WEISS);
        }
        break;
    case A_URTEIL:
        if (K.ziele && t < 45) zeichne_anim(FX_RUNE, b % 4, K.ziel[0], BODEN, 0, 0, WEISS);
        break;
    case A_WIND:
        if (K.geschoss_aktiv) zeichne_anim(FX_SICHEL, b % 2, (int)K.geschoss, BODEN, K.geschoss_dir > 0, 0, WEISS);
        break;
    case A_RANKEN:
        for (int i = 0; i < K.ziele; i++) {
            int start = 50 + i * 20;
            if (t < start) zeichne_anim(FX_RISS, b % 2, K.ziel[i], BODEN, 0, 0, WEISS);
            else if (t < start + 30) zeichne_anim(FX_WURZEL, (t - start) / TPB, K.ziel[i], BODEN, 0, 0, WEISS);
        }
        break;
    case A_RISS:
        if (t < 30) zeichne_anim(FX_KUGEL, b % 4, K.x + dir_zum_held() * 30, BODEN - 60, 0, 0, 0xFFFF80FF);
        if (K.geschoss_aktiv) zeichne_anim(FX_WELLE, b % 4, (int)K.geschoss, BODEN - 4, 0, 0, WEISS);
        break;
    case A_WELT: {
        int dunkel = t < 120 ? t * 160 / 120 : 160 - (t - 120) * 5;
        if (dunkel < 0) dunkel = 0;
        rechteck(0, 0, BILD_B, BILD_H, ((unsigned int)dunkel << 24) | 0x00100408);
        if (t < 120) zeichne_anim(FX_KUGEL, b % 4, K.x, BODEN - 110, 0, 0, WEISS);
        if (t >= 120 && t < 132) rechteck(0, 0, BILD_B, BILD_H, 0x80FFFFFF);   /* höchstens 50 % Helligkeit */
        break;
    }
    }
}

/* Ein 4 Pixel hoher Nebelstreifen von xa bis xb: gleichmäßige Grundfarbe und
 * darüber die Nebelkachel, die langsam nach links zieht */
static void nebel_streifen(int xa, int xb, int y, int t)
{
    if (xb <= xa) return;
    rechteck(xa, y, xb - xa, 4, 0x80A0127A);   /* lila (ABGR) */
    const Bild *b = &BILDER[ANIMS[FX_NEBEL].erstes];
    const Textur *tx = &TEX_GRUPPE[b->gruppe];
    int verschub = t / 2;
    int v = b->v + (y % b->h);
    int h = b->h - (y % b->h) < 4 ? b->h - (y % b->h) : 4;
    for (int x = xa; x < xb;) {
        int u = (x + verschub) % b->w;
        int w = b->w - u;
        if (w > xb - x) w = xb - x;
        zeichne(tx, b->seite, 0, b->u + u, v, w, h, x, y, 0, 0x90FFFFFF);
        x += w;
    }
}

static void nebel_zeichnen(void)
{
    if (K.zustand != KZ_VERWANDLUNG || K.verw != 2 || K.tick < V_WELLE) return;
    int t = K.tick;
    int r = (t - V_WELLE) * 10;          /* Nebel rollt von der Königin heran */
    int schild = hat_amulett() && H.zustand != HZ_TOT;
    int hx = (int)H.x, hy = BODEN - 28;
    int x0 = K.x - r, x1 = K.x + r;
    if (x0 < 0) x0 = 0;
    if (x1 > BILD_B) x1 = BILD_B;
    if (x1 <= x0) return;
    for (int y = 0; y < BILD_H; y += 4) {
        if (schild && y > hy - 40 && y < hy + 36) {
            int dy = y - hy, rx = 30;
            int halb = (int)(rx * __builtin_sqrtf(1.0f - (float)(dy * dy) / (38.0f * 38.0f)));
            if (halb < 0) halb = 0;
            nebel_streifen(x0, hx - halb < x1 ? hx - halb : x1, y, t);
            nebel_streifen(hx + halb > x0 ? hx + halb : x0, x1, y, t);
            rechteck(hx - halb - 2, y, 2, 4, 0xFF7ED9F6);   /* goldener Rand des Schilds */
            rechteck(hx + halb, y, 2, 4, 0xFF7ED9F6);
        } else {
            nebel_streifen(x0, x1, y, t);
        }
    }
}

/* Phasenwechsel im Hintergrund: Der Saal verdunkelt sich, um sie lädt sich Licht auf, und
 * hinter der Front der Welle erscheint der Saal der neuen Phase. */
static void verwandlung_hintergrund(void)
{
    int t = K.tick, neu = K.verw;
    if (t >= V_WELLE) {
        int r = (t - V_WELLE) * (K.verw == 1 ? 8 : 10);
        hintergrund_ausschnitt(neu, K.x - r, K.x + r);
    }
    int dunkel = t < V_REDE ? t * 120 / V_REDE : t < V_WELLE ? 120 : 120 - (t - V_WELLE) * 2;
    if (dunkel > 0) rechteck(0, 0, BILD_B, BILD_H, ((unsigned int)dunkel << 24) | 0x00100408);
}

/* Licht über dem ganzen Bild, in Streifen von 4 Pixeln; mit Amulett bleibt um den Helden
 * eine Blase mit goldenem Rand frei (wie beim Nebel). */
static void licht_flaeche(int x0, int x1, unsigned int farbe)
{
    if (x0 < 0) x0 = 0;
    if (x1 > BILD_B) x1 = BILD_B;
    if (x1 <= x0) return;
    int blase = hat_amulett() && H.zustand != HZ_TOT && H.zustand != HZ_WEG;
    static const int SPRUNG[8] = {0, 0, 6, 14, 18, 14, 6, 0};   /* Höhe je Bild (held.py) */
    int hy = BODEN - 28;
    if (H.zustand == HZ_SPRINGT) hy -= SPRUNG[(H.tick / TPB) & 7];   /* die Blase springt mit */
    int hx = (int)H.x;
    for (int y = 0; y < BILD_H; y += 4) {
        int dy = y + 2 - hy;
        if (blase && dy > -40 && dy < 40) {
            int halb = (int)(32 * __builtin_sqrtf(1.0f - (float)(dy * dy) / (40.0f * 40.0f)));
            int l = hx - halb, r = hx + halb;
            if (l > x0) rechteck(x0, y, (l < x1 ? l : x1) - x0, 4, farbe);
            if (r < x1) rechteck(r > x0 ? r : x0, y, x1 - (r > x0 ? r : x0), 4, farbe);
            rechteck(l - 2, y, 2, 4, 0xFF7ED9F6);   /* goldener Rand der Blase */
            rechteck(r, y, 2, 4, 0xFF7ED9F6);
        } else {
            rechteck(x0, y, x1 - x0, 4, farbe);
        }
    }
}

static int k_silhouette;   /* Königin als dunkle Gestalt im Licht zeichnen */
static void koenigin_zeichnen(void);

/* Beim Aufladen wächst eine pulsierende Lichtsäule von ihr aus über den ganzen Bildschirm;
 * beim Losbrechen der Welle blendet sie kurz grell auf. Sie selbst bleibt dunkel in der Mitte. */
static void verwandlung_licht(void)
{
    if (K.zustand != KZ_VERWANDLUNG) return;
    int t = K.tick;
    if (t < V_REDE || t >= V_WELLE + 24) return;
    unsigned int farbe = K.verw == 1 ? 0x00FFF0B0 : 0x00E070FF;   /* Türkisweiß bzw. Magenta (ABGR) */
    int a, b;
    if (t < V_WELLE) {
        int p = (t - V_REDE) * 256 / (V_WELLE - V_REDE);           /* 0 .. 256 */
        b = 24 + (BILD_B * 2 - 24) * p / 256 * p / 256;           /* wächst immer schneller */
        a = 50 + p * 130 / 256 + ((t / 4) % 2) * 30;               /* pulsierend heller */
    } else {
        b = BILD_B * 2;
        a = 230 - (t - V_WELLE) * 9;                               /* greller Blitz, dann aus */
    }
    if (a > 240) a = 240;
    /* weicher Rand: zwei schwächere Säume außen */
    licht_flaeche(K.x - b / 2 - 24, K.x + b / 2 + 24, ((unsigned int)(a / 4) << 24) | farbe);
    licht_flaeche(K.x - b / 2 - 10, K.x + b / 2 + 10, ((unsigned int)(a / 3) << 24) | farbe);
    licht_flaeche(K.x - b / 2, K.x + b / 2, ((unsigned int)(a * 2 / 3) << 24) | farbe);
    k_silhouette = 1;
    koenigin_zeichnen();
    k_silhouette = 0;
    if (t < V_WELLE) zeichne_anim(FX_KUGEL, (t / TPB) % 4, K.x, BODEN - 70, 0, 0, WEISS);
}

static void koenigin_zeichnen(void)
{
    int spiegel = koenigin_blickt_rechts();
    int anim, bild, wanken = 0;
    unsigned int f = WEISS;
    int p = K.phase;
    if (K.zustand == KZ_ANGRIFF) {
        anim = ANG[K.angriff].anim;
        bild = K.tick / TPB;
        if (K.angriff == A_WELT) bild = K.tick < 120 ? (K.tick / TPB < 5 ? K.tick / TPB : 5) : 6 + (K.tick - 120) / TPB;
    } else if (K.zustand == KZ_VERWANDLUNG) {
        int t = K.tick;
        anim = (K.verw == 1 && t < V_WELLE) ? Q_P1_IDLE : Q_P2_IDLE;
        bild = anim == Q_P1_IDLE ? (lage_tick / TPB / 2) % 6 : (lage_tick / TPB) % 10;
        if (t < V_REDE) {                                       /* getroffen: sie wankt */
            wanken = (t / 3) % 2 ? 2 : -2;
            if (t < 12 && (t / 2) % 2) f = 0xFF6060FF;          /* rot aufblitzen */
        }
        if (t >= V_RISS && t < V_WELLE && (t / 3) % 2)
            f = K.verw == 1 ? 0xFFFF80FF : P3_FARBE;            /* Helm reißt bzw. Wurzelholz bricht durch */
        if (K.verw == 2 && t >= V_WELLE) f = P3_FARBE;
    } else if (p >= 1) {
        anim = Q_P2_IDLE;
        bild = (lage_tick / TPB) % 10;
    } else if (K.geht) {
        anim = Q_P1_GEHEN;              /* in Phase 2 und 3 schwebt sie */
        bild = geh_bild(K.geh_weg);
    } else {
        anim = Q_P1_IDLE;
        bild = (lage_tick / TPB / 2) % 6;
    }
    if (umarm_anim()) { anim = Q_UMARMUNG; bild = umarm_bild(); }
    if (H.aufsteh_tick) { anim = Q_AUFSTEHEN; bild = 0; }
    if (p == 2) f = P3_FARBE;
    if (umarm_anim() || H.aufsteh_tick) zeichne_anim(Q_SENSE_BODEN, 0, K.x, BODEN, spiegel, 0, f);   /* abgelegt */
    if (k_silhouette) {   /* nur die Gestalt, dunkel gegen das Licht */
        zeichne_anim(anim, bild, K.x + wanken, BODEN, spiegel, 0, 0xFF301018);
        return;
    }
    zeichne_anim(anim, bild, K.x + wanken, BODEN, spiegel, 0, f);
    /* Umhang des Helden in der Umarmung mit der Farbtabelle seiner Ausrüstungsstufe */
    if (umarm_anim()) zeichne_anim(H_UMARMUNG_UMHANG, bild, K.x, BODEN, spiegel, H.stufe, f);
}

static void diener_zeichnen(void)
{
    if (D.zustand == DZ_FORT) return;
    int x = (int)D.x, anim = D_IDLE, bild = 0, spiegel = 0;
    unsigned int f = WEISS;
    switch (D.zustand) {
    case DZ_KOMMT: anim = D_GEHEN; bild = ((int)(D.x / GEH_PX) % 8 + 8) % 8; break;
    case DZ_KNIET: anim = D_KNIEN; bild = D.tick / (2 * TPB); break;
    case DZ_STEHT:
        if (D.tick < 4 * 2 * TPB) { anim = D_KNIEN; bild = 3 - D.tick / (2 * TPB); }   /* richtet sich auf */
        spiegel = D.tick > 16;                                                      /* wendet sich um */
        break;
    case DZ_TOT:
        anim = D_TOD; bild = D.tick / TPB; spiegel = 1;
        if (lage != L_INTRO && D.tick > 300) f = ((unsigned int)(255 - (D.tick - 300) * 255 / 100) << 24) | 0x00FFFFFF;
        break;
    }
    zeichne_anim(anim, bild, x, BODEN, spiegel, 0, f);
}

static void held_zeichnen(void)
{
    int spiegel = H.x > K.x;
    int clut = H.stufe;
    if (H.zustand == HZ_TOT) {
        int r = H.ritual, t = H.ritual_tick;
        int x = H.leiche_x, y = BODEN, fx = koerper_mitte(), fy = BODEN + 2;
        unsigned int f = WEISS;
        spiegel = H.leiche_spiegel;   /* die Lage des Körpers bleibt, auch wenn sie vorbeigeht */
        /* Das Schwert bleibt liegen, bis er verbrannt ist (bei der Umarmung: bis er zerfällt) */
        int schwert = H.tick / TPB >= TOD_SCHWERT_BILD && r != R_FERTIG && !(r == R_FEUER && t > 60)
                      && !(umarm_anim() && umarm_bild() == 7) && !(r == R_UMARMEN && !umarm_anim() && !H.umarm_geht && t > 140);
        if (umarm_anim()) {   /* Held und Feuer sind Teil der Umarmungs-Animation */
            if (schwert) zeichne_anim(H_SCHWERT_BODEN, 0, H.leiche_x, BODEN, spiegel, clut, f);
            return;
        }
        if (r == R_UMARMEN && !H.umarm_geht) {
            /* Phase 2/3: Sie hebt ihn in ARM_HEBEN Ticks an. Er liegt vor ihr, den Kopf an ihrer
             * Brust, und brennt in ihren Armen. */
            int d = K.blick > 0 ? 1 : -1;
            int heben = t < ARM_HEBEN ? t : ARM_HEBEN;
            int arm = K.x + d * (ARM_ABSTAND + TOD_MITTE);   /* Körpermitte in ihren Armen */
            int mitte = koerper_mitte() + (arm - koerper_mitte()) * heben / ARM_HEBEN;
            spiegel = d > 0;                                  /* Kopf zu ihr */
            x = mitte + d * TOD_MITTE;
            y = BODEN - ARM_HOEHE * heben / ARM_HEBEN;
            fx = mitte;
            fy = y + 2;
        }
        if (r == R_PORTAL) {
            int a = 255 - t * 4;
            if (a < 0) a = 0;
            f = ((unsigned int)a << 24) | 0x00FFFFFF;
            y = BODEN + t / 6;
        }
        /* Das Schwert bleibt am Boden, wo er gefallen ist (beim Portal sinkt es mit ihm) */
        if (schwert) zeichne_anim(H_SCHWERT_BODEN, 0, H.leiche_x, r == R_PORTAL ? y : BODEN, H.leiche_spiegel, clut, f);
        if (r != R_FERTIG && !(r == R_FEUER && t > 60) && !(r == R_UMARMEN && t > 140))
            zeichne_anim(H_TOD, H.tick / TPB, x, y, spiegel, clut, f);
        if (r == R_FEUER || (r == R_UMARMEN && !H.umarm_geht && t >= 90))
            zeichne_anim(FX_FEUER, (t / TPB) % 8, fx, fy, 0, 0, WEISS);
        if (r == R_PORTAL) zeichne_anim(FX_PORTAL, t / TPB, koerper_mitte(), BODEN, 0, 0, WEISS);
        return;
    }
    if (H.zustand == HZ_WEG) return;
    int a = H_IDLE, b = (lage_tick / TPB / 2) % 6;
    if (H.geht) { a = H_GEHEN; b = geh_bild(H.geh_weg); }
    switch (H.zustand) {
    case HZ_HIEBT: a = H_HIEB; b = H.tick / TPB; break;
    case HZ_ROLLT: a = H_ROLLE; b = H.tick / TPB; break;
    case HZ_SPRINGT: a = H_SPRUNG; b = H.tick / TPB; break;
    case HZ_GETROFFEN: a = H_TREFFER; b = H.tick / TPB; break;
    }
    unsigned int f = (H.unverwundbar > 0 && (H.unverwundbar / 4) % 2) ? 0x80FFFFFF : WEISS;
    zeichne_anim(a, b, (int)H.x, BODEN, spiegel, clut, f);
}

static void tafel(const char *const *zeilen, int n, int ueberschrift)
{
    rechteck(236, 20, 236, 232, 0xC0080406);
    rechteck(236, 251, 236, 1, 0xFF6E4E5A);
    menue_text(ueberschrift, 354 - menue_text_breite(ueberschrift) / 2, 26, WEISS);
    for (int i = 0; i < n; i++) text(zeilen[i], 246, 70 + i * 16, zeilen[i][0] == ' ' ? 0xFF9A8C94 : WEISS);
    text("✕ / ○ zurück", 246, 234, 0xFF808080);
}

static void titel_bild(void)
{
    if (m_schirm == S_TITEL) {
        titel_zeichnen();
        /* "Start drücken" blinkt langsam */
        if (lage_tick >= 30 && (lage_tick / 40) % 3 != 2)
            menue_text(MT_START, (BILD_B - menue_text_breite(MT_START)) / 2, 236, WEISS);
    } else {
        menue_zeichnen();
    }
    if (m_schirm == S_MENUE) {
        static const int TEXT[M_ANZAHL][2] = {
            {MT_SPIEL, MT_SPIEL_AKTIV}, {MT_OPTIONEN, MT_OPTIONEN_AKTIV}, {MT_CREDITS, MT_CREDITS_AKTIV}};
        for (int i = 0; i < M_ANZAHL; i++) {
            int mt = TEXT[i][i == m_wahl];
            menue_text(mt, 354 - menue_text_breite(mt) / 2, 84 + i * 40, WEISS);
        }
        text("✕ wählen   ○ zurück", 296, 250, 0xFF808080);
    } else if (m_schirm == S_OPTIONEN) {
        static const char *const z[] = {
            "Steuerung",
            "□ △ ○   Angriffe",
            "        (in jeder Phase andere)",
            "L + R   Weltgericht (Phase 3)",
            "← →     Gehen",
            "✕       Weiter, Antwort bestätigen",
            "↑ ↓     Antwort wählen",
            "Beim Toten: ✕ Verbrennen,",
            "        später weitere Rituale",
            "Select  zurück zum Hauptmenü",
        };
        tafel(z, 10, MT_OPTIONEN_AKTIV);
    } else if (m_schirm == S_CREDITS) {
        static const char *const z[] = {
            "Ein Spiel von Feierfox",
            "",
            "Menümusik: The Final Battle",
            "        von skrjablin (CC0)",
            "        opengameart.org",
            "Schrift im Spiel: DejaVu Sans Mono",
            "Programmierung mit Claude Code",
            "Werkzeuge: PSPSDK, PPSSPP,",
            "        Blender, Pillow",
        };
        tafel(z, 9, MT_CREDITS_AKTIV);
    }
    /* Einblenden aus Schwarz */
    if (lage_tick < 45) rechteck(0, 0, BILD_B, BILD_H, ((unsigned int)(255 - lage_tick * 255 / 45) << 24));
}

void spiel_zeichnen(void)
{
    if (lage == L_TITEL) {
        bild_beginnen(0xFF000000);
        titel_bild();
        bild_zeigen();
        return;
    }
    bild_beginnen(0xFF180A0E);
    hintergrund_zeichnen(K.phase);
    if (K.zustand == KZ_VERWANDLUNG) verwandlung_hintergrund();
    if (ring_aktiv) zeichne_anim(FX_RING, ring_tick / TPB, K.x, BODEN + 10, 0, 0, WEISS);
    koenigin_zeichnen();
    diener_zeichnen();
    held_zeichnen();
    effekte_zeichnen();
    verwandlung_licht();
    nebel_zeichnen();
    hud();
    if (ritual_moeglich()) {
        char hilfe[96];
        strcpy(hilfe, "✕ Verbrennen");
        if (erledigt[G_G2] && vertrauen >= 0) strcat(hilfe, "  ○ Umarmen");
        if (erledigt[G_G5]) strcat(hilfe, "  □ Opfern");
        int b = zeichen_anzahl(hilfe) * SCHRIFT_ZW;
        text(hilfe, koerper_mitte() - b / 2, BODEN - 70, WEISS);
    }
    if (lage == L_GESPRAECH) gespraech_zeichnen();
    else textbox();
    if (lage == L_ENDE) ende_zeichnen();
    bild_zeigen();
}

#ifdef DEMO
#include <stdio.h>
int demo_lage(void) { return lage; }
int demo_im_gespraech_wahl(void)
{
    return lage == L_GESPRAECH && g_schritt >= GESPRAECH[g_nr].anzahl_zeilen && !g_antwort;
}
int demo_gespraech_wahl(void) { return g_wahl; }
int demo_held_tot(void) { return lage == L_RITUAL; }
int demo_ritual_offen(void) { return ritual_moeglich(); }
int demo_abstand(void) { return abstand(); }
int demo_koenigin_x(void) { return K.x; }
int demo_leiche_x(void) { return H.ritual == R_FERTIG ? 1000 : koerper_mitte(); }
int demo_phase(void) { return K.phase; }
int demo_k_zustand(void) { return K.zustand; }
void demo_zustand(int t)
{
    printf("t=%d lage=%d phase=%d K.z=%d H.z=%d tode=%d stufe=%d vertrauen=%d einfluss=%d opfer=%d gespraech=%d ende=%d lp=%d/%d/%d\n",
           t, lage, K.phase, K.zustand, H.zustand, H.tode, H.stufe, vertrauen, einfluss, opfer,
           lage == L_GESPRAECH ? g_nr : -1, ende_nr, K.lp[0], K.lp[1], K.lp[2]);
}
#endif
