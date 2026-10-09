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
PSP_HEAP_SIZE_KB(-1024);

static volatile int laeuft = 1;

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
        pspDebugScreenPrintf("Daten nicht gefunden (Fehler %d).\n", fehler);
        pspDebugScreenPrintf("Der Ordner data/ muss neben der EBOOT.PBP liegen.\n");
        pspDebugScreenPrintf("Basis: %s\n", basis);
        sceKernelSleepThread();
        return 0;
    }

    sceCtrlSetSamplingCycle(0);
    sceCtrlSetSamplingMode(PSP_CTRL_MODE_ANALOG);

    spiel_start();
    unsigned int vorher = 0;
    while (laeuft) {
        SceCtrlData pad;
        sceCtrlReadBufferPositive(&pad, 1);
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
