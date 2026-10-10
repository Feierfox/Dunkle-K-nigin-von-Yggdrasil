/* Gespräche mit Auswahl und Enden, Texte aus docs/DIALOGE.md. */
#pragma once

enum { SP_KOENIGIN, SP_HELD, SP_VERDERBNIS, SP_ERZAEHLER, SP_DIENER };

typedef struct {
    unsigned char sprecher;
    const char *text;
} Zeile;

typedef struct {
    unsigned char sprecher;     /* wer den Satz der Auswahl spricht (Königin oder Verderbnis) */
    const char *satz;
    const char *antwort;        /* Antwort des Helden, darf NULL sein */
    signed char vertrauen, einfluss, guide;
    unsigned char bedingung;    /* 0 = immer, 1 = nur wenn vertrauen >= 2 */
    unsigned char ende;         /* 0 = kein Ende, sonst Nummer des Endes */
} Wahl;

typedef struct {
    const char *name;
    const Zeile *zeilen;
    int anzahl_zeilen;
    const Wahl *wahl;
    int anzahl_wahl;            /* 0: nur Zeilen, keine Auswahl (Eröffnung) */
} Gespraech;

enum { G_G1, G_G2, G_G3, G_G4, G_G5, G_R2, G_G6, G_R3, G_G7, G_R4, G_G8, G_PATCH, G_INTRO, G_VERW1, G_VERW2, GESPRAECHE };

extern const Gespraech GESPRAECH[GESPRAECHE];

typedef struct {
    const char *titel;
    const char *zeilen[4];
} Ende;

/* Index = Nummer des Endes (1..6), 0 unbenutzt */
extern const Ende ENDEN[7];
