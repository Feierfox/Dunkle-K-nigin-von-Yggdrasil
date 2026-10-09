/* Spiellogik der Testszene. Eine Spielrunde = ein Logikschritt bei 60 Bildern pro Sekunde. */
#pragma once

typedef struct {
    unsigned int gedrueckt;  /* gehaltene Tasten */
    unsigned int neu;        /* in diesem Schritt neu gedrückte Tasten */
    int stick_x;             /* Analog-Stick -128..127 */
} Eingabe;

void spiel_start(void);
void spiel_schritt(const Eingabe *e);
void spiel_zeichnen(void);
