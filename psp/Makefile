# Dunkle Königin von Yggdrasil - PSP-1000
# Bauen:   make            (pspdev-Toolchain im PATH, psp-config muss gefunden werden)
# Daten:   python ../tools/psp/assets_bauen.py  erzeugt data/ und src/assets_gen.h

TARGET = DunkleKoenigin
OBJS = src/main.o src/grafik.o src/spiel.o src/dialoge.o

INCDIR = src
CFLAGS = -O2 -G0 -Wall -Wextra -Wno-unused-parameter
CXXFLAGS = $(CFLAGS)
ASFLAGS = $(CFLAGS)

LIBS = -lpspgu -lpspctrl -lpspdisplay -lm

EXTRA_TARGETS = EBOOT.PBP
PSP_EBOOT_TITLE = The Dark Queen of Yggdrasil
PSP_EBOOT_ICON = ICON0.PNG
PSP_EBOOT_ICON1 = ICON1.PMF
PSP_EBOOT_PIC1 = PIC1.PNG
PSP_EBOOT_SND0 = SND0.AT3

PSPSDK = $(shell psp-config --pspsdk-path)
include $(PSPSDK)/lib/build.mak
