# PSP-Menü: The Dark Queen of Yggdrasil

Titelhintergrund auf Basis von assets/konzept/thronsaal-v1.webp. Bronze- und elfenbeinfarbene Fantasy-Serifenschrift im freien Vordergrund; der zentrale Wurzelthron bleibt sichtbar. Das Menüsymbol zeigt denselben Thron aus näherer Perspektive.

Mit dem eingebauten Imagegen-Tool erstellt; vollständige Prompts in PROMPTS.md. wallpaper-master.png und icon-master.png sind die hochaufgelösten Ergebnisse. previous-PIC1.PNG und previous-ICON0.PNG bewahren die bisherigen statischen Menübilder.

Die PSP-Exporte liegen unter psp/PIC1.PNG (480 × 272, RGB) und psp/ICON0.PNG (144 × 80, RGB). tools/psp/menu_bauen.py exportiert die Bilder; mit --repack ersetzt es die Menübilder und den TITLE-Eintrag der bestehenden EBOOT.PBP. Alle anderen PBP-Abschnitte einschließlich des kompilierten Spielcodes bleiben unverändert und werden beim Packen verglichen. Der Makefile-Titel ist für spätere Builds ebenfalls angepasst.

validation.json dokumentiert Bildmaße und den unveränderten Spielcode. Noch kein Test im XMB einer echten PSP. Die inzwischen ergänzte Königin-Vorschau mit ICON1-PMF-Animation und SND0-Menümusik ist unter ../koenigin-preview-v1 dokumentiert.
