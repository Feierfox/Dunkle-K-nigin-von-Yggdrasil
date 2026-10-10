# Dunkle Königin von Yggdrasil - PSP-1000
# Bauen:   make PSPSDK=C:/pspsdk/psp/sdk "CC=psp-gcc -std=gnu99" EBOOT.PBP   (C:/pspsdk/bin im PATH)
#          Mit diesem PSPSDK läuft das Spiel auf der PSP-1000; der pspdev-Build brach mit 80010002 ab.
# Daten:   python ../tools/psp/assets_bauen.py  erzeugt data/ und src/assets_gen.h

TARGET = DunkleKoenigin
OBJS = src/main.o src/grafik.o src/spiel.o src/dialoge.o

INCDIR = src
CFLAGS = -O2 -G0 -Wall -Wextra -Wno-unused-parameter
CXXFLAGS = $(CFLAGS)
ASFLAGS = $(CFLAGS)

LIBS = -lpspgu -lpspctrl -lpspdisplay -lm

# Verschiebbares Programm (PRX): Mit fester Adresse (0x08804000) bricht der Start auf
# der PSP-1000 mit Custom Firmware ab (Fehler 800200D9, Speicher belegt).
BUILD_PRX = 1

EXTRA_TARGETS = EBOOT.PBP
PSP_EBOOT_TITLE = The Dark Queen of Yggdrasil
PSP_EBOOT_ICON = ICON0.PNG
PSP_EBOOT_ICON1 = ICON1.PMF
PSP_EBOOT_PIC1 = PIC1.PNG
PSP_EBOOT_SND0 = SND0.AT3

PSPSDK = $(shell psp-config --pspsdk-path)
include $(PSPSDK)/lib/build.mak
