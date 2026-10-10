# Testfassung für die PSP-1000

Dasselbe Spiel wie `psp/EBOOT.PBP` (gleicher Quellcode), aber gebaut mit dem älteren PSPSDK aus `C:\pspsdk` (gcc 4.3.5), mit dem auch Ludus Lanista auf der PSP-1000 läuft. Unterschied im PARAM.SFO: kein `MEMSIZE`-Eintrag.

Hintergrund: Die pspdev-Fassung brach auf der PSP-1000 mit 80010002 ab.

Bauen: `make PSPSDK=C:/pspsdk/psp/sdk "CC=psp-gcc -std=gnu99" EBOOT.PBP` in `psp/` (mit `C:\pspsdk\bin` im PATH).

## Variante B (`variante-b/EBOOT.PBP`)

Wie oben, zusätzlich so nah wie möglich an Ludus Lanista: ohne `PSP_FW_VERSION = 500`, ohne Menüvideo (`ICON1.PMF`) und Menümusik (`SND0.AT3`), fester Heap von 12 MB statt `PSP_HEAP_SIZE_KB(-1024)`, Modulname `DarkQueen`.
