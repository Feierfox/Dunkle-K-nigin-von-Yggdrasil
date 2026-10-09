#include <pspkernel.h>
#include <pspdisplay.h>
#include <pspgu.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

#include "grafik.h"
#include "assets_gen.h"

#define PUFFER_B 512

static unsigned int __attribute__((aligned(16))) befehle[262144];

Textur TEX_GRUPPE[G_ANZAHL];
static Textur tex_saal, tex_schrift;
static int schrift_cp[256];
static int schrift_anzahl;

typedef struct {
    unsigned short u, v;
    unsigned int farbe;
    short x, y, z;
} VertexT;

typedef struct {
    unsigned int farbe;
    short x, y, z;
} VertexF;

static const Textur *aktive_textur;
static int aktive_seite = -1, aktive_clut = -1;

static unsigned short le16(const unsigned char *p) { return p[0] | (p[1] << 8); }

int textur_laden(Textur *t, const char *pfad)
{
    FILE *f = fopen(pfad, "rb");
    if (!f) return -1;
    unsigned char kopf[8];
    if (fread(kopf, 1, 8, f) != 8 || memcmp(kopf, "DKAT", 4) != 0) { fclose(f); return -2; }
    t->seiten = le16(kopf + 4);
    t->cluts = le16(kopf + 6);
    if (t->seiten > 8) { fclose(f); return -3; }
    t->clut = memalign(16, t->cluts * 256 * 4);
    fread(t->clut, 4, t->cluts * 256, f);
    for (int s = 0; s < t->seiten; s++) {
        unsigned char wh[4];
        fread(wh, 1, 4, f);
        t->breite[s] = le16(wh);
        t->hoehe[s] = le16(wh + 2);
        int n = t->breite[s] * t->hoehe[s];
        t->pixel[s] = memalign(16, n);
        fread(t->pixel[s], 1, n, f);
    }
    fclose(f);
    sceKernelDcacheWritebackAll();
    return 0;
}

/* UTF-8 dekodieren */
static int naechstes_zeichen(const char **s)
{
    const unsigned char *p = (const unsigned char *)*s;
    int c = p[0];
    if (c < 0x80) { *s += 1; return c; }
    if ((c & 0xE0) == 0xC0) { *s += 2; return ((c & 0x1F) << 6) | (p[1] & 0x3F); }
    if ((c & 0xF0) == 0xE0) { *s += 3; return ((c & 0x0F) << 12) | ((p[1] & 0x3F) << 6) | (p[2] & 0x3F); }
    *s += 1;
    return '?';
}

int grafik_start(const char *basis)
{
    char pfad[256];
    for (int g = 0; g < G_ANZAHL; g++) {
        snprintf(pfad, sizeof pfad, "%s%s", basis, GRUPPEN_DATEI[g]);
        if (textur_laden(&TEX_GRUPPE[g], pfad) != 0) return -1;
    }
    snprintf(pfad, sizeof pfad, "%sdata/saal.bin", basis);
    if (textur_laden(&tex_saal, pfad) != 0) return -2;
    snprintf(pfad, sizeof pfad, "%sdata/schrift.bin", basis);
    if (textur_laden(&tex_schrift, pfad) != 0) return -3;

    const char *z = SCHRIFT_ZEICHEN;
    schrift_anzahl = 0;
    while (*z && schrift_anzahl < 256) schrift_cp[schrift_anzahl++] = naechstes_zeichen(&z);

    sceGuInit();
    sceGuStart(GU_DIRECT, befehle);
    sceGuDrawBuffer(GU_PSM_8888, (void *)0, PUFFER_B);
    sceGuDispBuffer(BILD_B, BILD_H, (void *)0x88000, PUFFER_B);
    sceGuDepthBuffer((void *)0x110000, PUFFER_B);
    sceGuOffset(2048 - (BILD_B / 2), 2048 - (BILD_H / 2));
    sceGuViewport(2048, 2048, BILD_B, BILD_H);
    sceGuDepthRange(65535, 0);
    sceGuScissor(0, 0, BILD_B, BILD_H);
    sceGuEnable(GU_SCISSOR_TEST);
    sceGuDisable(GU_DEPTH_TEST);
    sceGuEnable(GU_BLEND);
    sceGuBlendFunc(GU_ADD, GU_SRC_ALPHA, GU_ONE_MINUS_SRC_ALPHA, 0, 0);
    sceGuTexFunc(GU_TFX_MODULATE, GU_TCC_RGBA);
    sceGuTexFilter(GU_NEAREST, GU_NEAREST);
    sceGuTexWrap(GU_CLAMP, GU_CLAMP);
    sceGuShadeModel(GU_FLAT);
    sceGuFinish();
    sceGuSync(0, 0);
    sceDisplayWaitVblankStart();
    sceGuDisplay(GU_TRUE);
    return 0;
}

void grafik_ende(void) { sceGuTerm(); }

void bild_beginnen(unsigned int hintergrund)
{
    sceGuStart(GU_DIRECT, befehle);
    aktive_textur = 0;   /* Textur nach jedem neuen Befehlspuffer neu setzen */
    sceGuClearColor(hintergrund);
    sceGuClear(GU_COLOR_BUFFER_BIT);
}

void bild_zeigen(void)
{
    sceGuFinish();
    sceGuSync(0, 0);
    sceDisplayWaitVblankStart();
    sceGuSwapBuffers();
}


static void textur_setzen(const Textur *t, int seite, int clut)
{
    if (t == aktive_textur && seite == aktive_seite && clut == aktive_clut) return;
    sceGuClutMode(GU_PSM_8888, 0, 0xFF, 0);
    sceGuClutLoad(256 / 8, t->clut + clut * 256);
    sceGuTexMode(GU_PSM_T8, 0, 0, 0);
    sceGuTexImage(0, t->breite[seite], t->hoehe[seite], t->breite[seite], t->pixel[seite]);
    sceGuTexFlush();
    aktive_textur = t;
    aktive_seite = seite;
    aktive_clut = clut;
}

void zeichne(const Textur *t, int seite, int clut, int u, int v, int w, int h,
             int x, int y, int spiegeln, unsigned int farbe)
{
    sceGuEnable(GU_TEXTURE_2D);
    textur_setzen(t, seite, clut);
    /* Breite Sprites in 64-Pixel-Streifen zerlegen: schneller im Texturcache der PSP */
    for (int s = 0; s < w; s += 64) {
        int sw = (w - s < 64) ? w - s : 64;
        VertexT *vt = sceGuGetMemory(2 * sizeof(VertexT));
        int x0 = spiegeln ? x + w - s - sw : x + s;
        vt[0].u = spiegeln ? u + s + sw : u + s;
        vt[0].v = v;
        vt[0].farbe = farbe;
        vt[0].x = x0;
        vt[0].y = y;
        vt[0].z = 0;
        vt[1].u = spiegeln ? u + s : u + s + sw;
        vt[1].v = v + h;
        vt[1].farbe = farbe;
        vt[1].x = x0 + sw;
        vt[1].y = y + h;
        vt[1].z = 0;
        sceGuDrawArray(GU_SPRITES, GU_TEXTURE_16BIT | GU_COLOR_8888 | GU_VERTEX_16BIT | GU_TRANSFORM_2D,
                       2, 0, vt);
    }
}

void zeichne_anim(int anim, int bild, int ax, int ay, int spiegeln, int clut, unsigned int farbe)
{
    const Anim *a = &ANIMS[anim];
    if (bild < 0) bild = 0;
    if (bild >= a->anzahl) bild = a->anzahl - 1;
    const Bild *b = &BILDER[a->erstes + bild];
    const Textur *t = &TEX_GRUPPE[b->gruppe];
    if (clut >= t->cluts) clut = 0;
    int x = spiegeln ? ax - b->ox - b->w : ax + b->ox;
    zeichne(t, b->seite, clut, b->u, b->v, b->w, b->h, x, ay + b->oy, spiegeln, farbe);
}

void rechteck(int x, int y, int w, int h, unsigned int farbe)
{
    sceGuDisable(GU_TEXTURE_2D);
    VertexF *vt = sceGuGetMemory(2 * sizeof(VertexF));
    vt[0].farbe = farbe; vt[0].x = x; vt[0].y = y; vt[0].z = 0;
    vt[1].farbe = farbe; vt[1].x = x + w; vt[1].y = y + h; vt[1].z = 0;
    sceGuDrawArray(GU_SPRITES, GU_COLOR_8888 | GU_VERTEX_16BIT | GU_TRANSFORM_2D, 2, 0, vt);
}

void hintergrund_zeichnen(void)
{
    zeichne(&tex_saal, 0, 0, 0, 0, BILD_B, BILD_H, 0, 0, 0, 0xFFFFFFFF);
}

int text(const char *s, int x, int y, unsigned int farbe)
{
    int x0 = x;
    while (*s) {
        int cp = naechstes_zeichen(&s);
        int i = 0;
        while (i < schrift_anzahl && schrift_cp[i] != cp) i++;
        if (i == schrift_anzahl) i = '?' - 32;
        if (cp != ' ') {
            int u = (i % SCHRIFT_JE_ZEILE) * SCHRIFT_ZW;
            int v = (i / SCHRIFT_JE_ZEILE) * SCHRIFT_ZH;
            zeichne(&tex_schrift, 0, 0, u, v, SCHRIFT_ZW, SCHRIFT_ZH, x, y, 0, farbe);
        }
        x += SCHRIFT_ZW;
    }
    return x - x0;
}
