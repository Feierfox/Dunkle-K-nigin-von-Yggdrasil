# Testfassung für die PSP-1000

Dasselbe Spiel wie `psp/EBOOT.PBP` (gleicher Quellcode), aber gebaut mit dem älteren PSPSDK aus `C:\pspsdk` (gcc 4.3.5), mit dem auch Ludus Lanista auf der PSP-1000 läuft. Unterschied im PARAM.SFO: kein `MEMSIZE`-Eintrag.

Hintergrund: Die pspdev-Fassung brach auf der PSP-1000 mit 80010002 ab.

Bauen: `make PSPSDK=C:/pspsdk/psp/sdk "CC=psp-gcc -std=gnu99" EBOOT.PBP` in `psp/` (mit `C:\pspsdk\bin` im PATH).
