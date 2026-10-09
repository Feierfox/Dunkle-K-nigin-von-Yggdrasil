# PSP-1000: Testszene

Erste spielbare Testszene in C mit dem PSPSDK (pspdev), 60 Bilder pro Sekunde.

## Starten

- **PPSSPP (PC):** `EBOOT.PBP` öffnen. Der Ordner `data/` muss daneben liegen.
- **PSP-1000 mit Custom Firmware:** den Ordner so auf den Memory Stick kopieren:
  ```
  ms0:/PSP/GAME/DunkleKoenigin/EBOOT.PBP
  ms0:/PSP/GAME/DunkleKoenigin/data/*.bin
  ```

## Steuerung

| Taste | Wirkung |
| --- | --- |
| ← → / Analog-Stick | Königin gehen |
| □ | Richtschlag |
| △ | Sensenzug |
| ○ | Kreisschnitt |
| ✕ | Totenritual: Verbrennen (beim Körper des Helden) |
| Select | Neustart |
| Home | Beenden |

## Inhalt der Testszene

- Thronsaal, Königin mit Ruhepose und drei Angriffen (Trefferzonen nach `docs/ANGRIFFE.md`), drei Lebensleisten.
- Held mit Lern-KI: weicht einem Angriff erst aus, nachdem er davon getroffen wurde; zuerst zu früh, ab dem dritten Mal richtig (Rolle bzw. Sprung).
- Tod, Stille, die Königin geht zum Körper, ✕ verbrennt ihn mit eisblauem Feuer, der Held kehrt zurück, sobald sie wieder rechts im Saal steht.
- Rückkehrworte der Königin und erste Kommentare des Helden.
- Nach dem 5. und 11. Tod eine Quest: Abwesenheit (es geschieht nichts), danach neue Umhangfarbe (Palettentausch) und ein Herz mehr.
- Rote Leiste leer: Verwandlung mit Ringwelle; der Held lernt, darüberzuspringen. Phase 2 selbst folgt später.

**Noch nicht enthalten:** Gehen-Animationen (Figuren gleiten), Phase 2 und 3, Umarmen und Opfern, Gespräche mit Auswahl, Musik und Ton.

## Bauen

```
python tools/psp/assets_bauen.py      # data/*.bin und src/assets_gen.h aus den Sprites
export PSPDEV=/pfad/zu/pspdev PATH=$PSPDEV/bin:$PATH
cd psp && make
```

Die Toolchain gibt es fertig unter https://github.com/pspdev/pspdev/releases.

## Datenformat

`data/*.bin`: Texturseiten mit 8 Bit pro Pixel (höchstens 512 × 512) und Farbtabellen (CLUT); Aufbau siehe `tools/psp/assets_bauen.py`. Die Helden-Datei enthält fünf Farbtabellen für die Ausrüstungsstufen.
