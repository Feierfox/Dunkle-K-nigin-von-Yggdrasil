/* Grafik für die PSP-1000: sceGu, 8-Bit-Texturen mit Farbtabelle, Sprites, Text. */
#pragma once

#define BILD_B 480
#define BILD_H 272

typedef struct {
    int seiten, cluts;
    unsigned int *clut;          /* cluts x 256 Einträge */
    unsigned char *pixel[8];     /* je Seite */
    int breite[8], hoehe[8];
} Textur;

int grafik_start(const char *basis);
void grafik_ende(void);

int textur_laden(Textur *t, const char *pfad);

void bild_beginnen(unsigned int hintergrund);
void bild_zeigen(void);

/* Ausschnitt einer Texturseite zeichnen. farbe: ABGR, 0xFFFFFFFF = unverändert. */
void zeichne(const Textur *t, int seite, int clut, int u, int v, int w, int h,
             int x, int y, int spiegeln, unsigned int farbe);
/* Bild einer Animation am Ankerpunkt (Fußpunkt) ax/ay zeichnen. */
void zeichne_anim(int anim, int bild, int ax, int ay, int spiegeln, int clut, unsigned int farbe);
/* Gefülltes Rechteck, farbe ABGR mit Alpha. */
void rechteck(int x, int y, int w, int h, unsigned int farbe);
/* Thronsaal als Hintergrund: 0 = Phase 1, 1 = Phase 2, 2 = Phase 3. */
void hintergrund_zeichnen(int phase);
/* Titelbild (data/titel.bin) als Hintergrund des Hauptmenüs. */
void titel_zeichnen(void);
/* Hauptmenü (data/menue.bin): Hintergrund mit der Königin und vorgefertigte Menütexte (MT_...). */
void menue_zeichnen(void);
void menue_text(int mt, int x, int y, unsigned int farbe);
int menue_text_breite(int mt);
/* UTF-8-Text; gibt die gezeichnete Breite zurück. stil 1 = Schrift der Verderbnis. */
int text(const char *s, int x, int y, unsigned int farbe);
int text_stil(const char *s, int x, int y, unsigned int farbe, int stil);
/* Anzahl Zeichen (nicht Bytes) eines UTF-8-Textes. */
int zeichen_anzahl(const char *s);
/* Zeilenumbruch an Leerzeichen: schreibt bis zu max_zeilen Anfangspositionen und Längen (Bytes). */
int umbrechen(const char *s, int max_zeichen, const char **start, int *laenge, int max_zeilen);

extern Textur TEX_GRUPPE[];
