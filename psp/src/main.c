/* Dunkle Königin von Yggdrasil - Testszene für die PSP-1000.
 * Hauptschleife mit 60 Bildern pro Sekunde (an die Bildwiederholung gekoppelt). */
#include <pspkernel.h>
#include <pspctrl.h>
#include <pspdisplay.h>
#include <pspdebug.h>
#include <string.h>

#include "grafik.h"
#include "spiel.h"

PSP_MODULE_INFO("DunkleKoenigin", 0, 0, 1);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_USER | THREAD_ATTR_VFPU);
PSP_HEAP_SIZE_KB(12 * 1024);   /* fest wie bei Ludus Lanista; mit -1024 startete die PSP-1000 nicht (80010002) */

static volatile int laeuft = 1;

#ifdef DEMO
/* Nur zum Testen im Emulator: Skript steuert die Königin, Bildschirmfotos als Rohdaten. */
#include <stdio.h>
#include <pspgu.h>
extern int demo_lage(void);
extern int demo_im_gespraech_wahl(void);
extern int demo_gespraech_wahl(void);
extern int demo_held_tot(void);
extern int demo_ritual_offen(void);
extern int demo_abstand(void);
extern int demo_koenigin_x(void);
extern int demo_leiche_x(void);
extern int demo_phase(void);
extern int demo_k_zustand(void);
extern void demo_zustand(int t);
/* Lage: 0 Kampf, 1 Ritual, 2 abwesend, 3 Gespräch, 4 Ende */
static unsigned int demo_eingabe(int t)
{
    static int rituale;
    if (demo_lage() == 3) {
        if (t % 20) return 0;
        /* immer die zweite Antwort: der vertrauensvolle Weg */
        if (demo_im_gespraech_wahl() && demo_gespraech_wahl() != 1) return PSP_CTRL_DOWN;
        return PSP_CTRL_CROSS;
    }
    if (demo_lage() == 2) return (t / 120) % 2 ? PSP_CTRL_LEFT : PSP_CTRL_RIGHT;
    if (demo_held_tot()) {
        int d = demo_leiche_x() - demo_koenigin_x();
        if (d > 200) return PSP_CTRL_RIGHT;          /* Ritual vorbei: zurück nach rechts */
        if (d < -25) return PSP_CTRL_LEFT;
        if (d > 25) return PSP_CTRL_RIGHT;
        if (t % 10 || !demo_ritual_offen()) return 0;
        /* abwechselnd Umarmen und Verbrennen, ab und zu Opfern; wirkt eine Taste
         * noch nicht (nicht freigeschaltet), folgt beim nächsten Versuch ✕ */
        static int letzter_t = -100;
        int nochmal = (t - letzter_t) <= 10;
        letzter_t = t;
        if (nochmal) return PSP_CTRL_CROSS;
        rituale++;
        if (rituale % 7 == 3) return PSP_CTRL_SQUARE;
        return (rituale % 2) ? PSP_CTRL_CIRCLE : PSP_CTRL_CROSS;
    }
    if (demo_abstand() > 70) return PSP_CTRL_LEFT;
    if (demo_phase() == 2) return PSP_CTRL_LTRIGGER | PSP_CTRL_RTRIGGER;   /* Weltgericht, sobald bereit */
    if ((t % 75) == 0) {
        static const unsigned int a[3] = {PSP_CTRL_SQUARE, PSP_CTRL_TRIANGLE, PSP_CTRL_CIRCLE};
        return a[(t / 75) % 3];
    }
    return 0;
}
static void demo_foto(const char *basis, int t)
{
    void *top; int breite, format;
    sceDisplayGetFrameBuf(&top, &breite, &format, PSP_DISPLAY_SETBUF_NEXTFRAME);
    char pfad[300];
    snprintf(pfad, sizeof pfad, "%sfoto_%05d.raw", basis, t);
    FILE *f = fopen(pfad, "wb");
    if (!f) return;
    unsigned int *p = (unsigned int *)((unsigned int)top | 0x40000000);  /* ungecacht lesen */
    for (int y = 0; y < 272; y++) fwrite(p + y * breite, 4, 480, f);
    fclose(f);
}
#endif

static int beenden(int a, int b, void *c)
{
    (void)a; (void)b; (void)c;
    laeuft = 0;
    sceKernelExitGame();
    return 0;
}

static int rueckruf_faden(SceSize args, void *argp)
{
    (void)args; (void)argp;
    int id = sceKernelCreateCallback("Beenden", beenden, NULL);
    sceKernelRegisterExitCallback(id);
    sceKernelSleepThreadCB();
    return 0;
}

static void rueckrufe_einrichten(void)
{
    int id = sceKernelCreateThread("Rueckrufe", rueckruf_faden, 0x11, 0xFA0, 0, 0);
    if (id >= 0) sceKernelStartThread(id, 0, 0);
}

int main(int argc, char *argv[])
{
    rueckrufe_einrichten();

    /* Verzeichnis der EBOOT.PBP als Basis für data/ */
    char basis[256] = "";
    if (argc > 0 && argv[0]) {
        strncpy(basis, argv[0], sizeof basis - 1);
        char *schraeg = strrchr(basis, '/');
        if (schraeg) schraeg[1] = 0; else basis[0] = 0;
    }

    int fehler = grafik_start(basis);
    if (fehler != 0) {
        pspDebugScreenInit();
        pspDebugScreenPrintf("Daten nicht gefunden oder beschaedigt (Fehler %d).\n", fehler);
        pspDebugScreenPrintf("Der Ordner data/ muss neben der EBOOT.PBP liegen.\n");
        pspDebugScreenPrintf("Basis: %s\n", basis);
        sceKernelSleepThread();
        return 0;
    }

    sceCtrlSetSamplingCycle(0);
    sceCtrlSetSamplingMode(PSP_CTRL_MODE_ANALOG);

    spiel_start();
    unsigned int vorher = 0;
#ifdef DEMO
    int demo_t = 0;
#endif
    while (laeuft) {
        SceCtrlData pad;
        sceCtrlReadBufferPositive(&pad, 1);
#ifdef DEMO
        pad.Buttons = demo_eingabe(demo_t);
        pad.Lx = 128;
        if (demo_t % 90 == 0) demo_zustand(demo_t);
        /* zusätzliche Fotos während der Verwandlung 2 (Nebel) und in Phase 3 */
        if (demo_t % 90 == 0 || (demo_phase() >= 1 && demo_k_zustand() == 2 && demo_t % 15 == 0) ||
            (demo_phase() == 2 && demo_t % 30 == 0))
            demo_foto(basis, demo_t);
        if (++demo_t > DEMO) break;
#endif
        Eingabe e;
        e.gedrueckt = pad.Buttons;
        e.neu = pad.Buttons & ~vorher;
        e.stick_x = (int)pad.Lx - 128;
        vorher = pad.Buttons;

        spiel_schritt(&e);
        spiel_zeichnen();   /* wartet auf die Bildwiederholung: 60 Schritte pro Sekunde */
    }
    grafik_ende();
    sceKernelExitGame();
    return 0;
}
