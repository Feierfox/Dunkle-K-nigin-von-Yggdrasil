from pathlib import Path
import json,html,sys
import audio_config
import soundfile as sf
from analyze_sources import metrics
ROOT=Path(__file__).parent
recipes=json.loads((ROOT/'mix_recipes.json').read_text())
selected=json.loads((ROOT/'selected_sources.json').read_text())
audit=json.loads((ROOT/'source_audit.json').read_text())
labels={'held_step_01':'Held: Schritt 1','held_step_02':'Held: Schritt 2','held_step_03':'Held: Schritt 3','held_schwerthieb':'Held: Schwerthieb','koenigin_richtschlag':'Königin: Richtschlag','ranke_a':'Dornenranke: Durchbruch und Rückzug','ranke_b':'Hakenranke: Durchbruch und Rückzug','weltgericht_aufladen':'Weltgericht: Aufladung (2 Sekunden)','weltgericht_entladung':'Weltgericht: Entladung und Nachwirkung','weltgericht_demo_voller_ausklang':'Weltgericht: Gesamtvergleich mit vollem Ausklang','weltgericht_todesstille':'Weltgericht: bewusste kurze Todesstille'}
page='''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SFX-Hörvergleich</title><style>body{font:16px system-ui;background:#151222;color:#e3dff0;margin:28px;line-height:1.5}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px}article{background:#211b31;border:1px solid #675479;padding:18px;border-radius:10px}audio{width:100%}a{color:#92d9e5}small{display:block;color:#bbb4cd;margin:8px 0}.status{padding:14px;background:#392c35;border:1px solid #987485}details{margin:20px 0}h2{font-size:20px}</style><h1>SFX: Originale und Mischungen</h1><p class="status">Technische Prüfung durchgeführt. Die Hörfreigabe steht aus: Ich kann Audio hier messen und bearbeiten, aber nicht selbst hören. Diese Fassungen sind Sounddesign-Entwürfe, keine bestätigte AA-Endqualität.</p><p>Mit moderater Lautstärke beginnen. Jede Master-Mischung lässt sich mit der PSP-Fassung in Mono vergleichen. Bitte auf fehlende Ausklänge, Rauschen, störende Schärfe, übermäßigen Hall und verständliche Treffer achten. Es spielt immer nur ein Clip.</p><main>'''
results=[]
for r in recipes:
 if 'name' not in r:continue
 name=r['name'];path=ROOT/'masters'/f'{name}.wav';x,sr=sf.read(path,always_2d=True);m=metrics(x,sr)
 psp=ROOT/'psp'/f'{name}.wav';mono,mr=sf.read(psp,always_2d=True);pm=metrics(mono,mr)
 assert not m['suspectedClipping'] and not m['suspectedAbruptEnd']
 assert not pm['suspectedClipping'] and not pm['suspectedAbruptEnd']
 assert abs(x[-1]).max()<.0001 and abs(mono[-1]).max()<.0001
 results.append({'name':name,'master':m,'psp':pm,'auditoryApproval':'pending'})
 page+=f'<article><h2>{html.escape(labels[name])}</h2><small>{m["seconds"]:.2f} s · Peak {m["peakDbFS"]:.1f} dBFS · technisch geprüft</small><p>Master · 48 kHz, 24 Bit, Stereo</p><audio controls preload="none" src="masters/{name}.wav"></audio><p>PSP-Vergleich · 22,05 kHz, 16 Bit, Mono</p><audio controls preload="none" src="psp/{name}.wav"></audio></article>'
page+='</main><h2>Unveränderte Ausgangsaufnahmen</h2><p>Keine Behauptung, dass diese Originale verlustfreie Erstaufnahmen sind: einige Quellen liegen als OGG beziehungsweise mit .mp3.flac-Dateinamen vor. Höhere Exportauflösung stellt verlorene Informationen nicht wieder her.</p>'
for s in selected:
 page+=f'<details><summary>{html.escape(s["file"])} · CC0</summary><audio controls preload="none" src="{html.escape(s["file"])}"></audio><p>{html.escape(s["author"])} · <a href="{html.escape(s["page"])}">Originalquelle</a></p></details>'
page+='''<p><a href="README.md">Prüfung und Grenzen</a> · <a href="selected_sources.json">Quellen und Originalprüfwerte</a></p><script>document.querySelectorAll('audio').forEach(a=>{a.volume=.5;a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()}));});</script></html>'''
(ROOT/'index.html').write_text(page,encoding='utf8')
(ROOT/'reports'/'export_checks.json').write_text(json.dumps(results,indent=2),encoding='utf8')
reject=[r for r in audit['files'] if r['suspectedClipping'] or r['suspectedAbruptEnd']]
(ROOT/'reports'/'flagged_sources.json').write_text(json.dumps(reject,indent=2),encoding='utf8')
lines=['# Technische Auswertung','',f'{len(audit["files"])} Dateien decodiert; {len(audit["decodeErrors"])} Decodierfehler.',f'{sum(r["suspectedClipping"] for r in audit["files"])} Clipping-Verdachtsfälle, {sum(r["suspectedAbruptEnd"] for r in audit["files"])} auffälliges Dateiende. Diese Dateien wurden nicht für die Mischungen gewählt.','', '| Mischung | Sekunden | Peak dBFS | End-RMS 50 ms dBFS | Endabriss-Flag |','| --- | ---: | ---: | ---: | --- |']
for r in results:
 m=r['master'];lines.append(f'| {r["name"]} | {m["seconds"]:.2f} | {m["peakDbFS"]:.2f} | {m["tail50msRmsDbFS"]:.2f} | {m["suspectedAbruptEnd"]} |')
lines+=['','Die Messungen sind Indikatoren, kein Ersatz für Hören. Ein leises Dateiende kann auch künstlich ausgeblendet sein; fehlende ursprüngliche Nachklänge lassen sich dadurch nicht feststellen oder wiederherstellen. Rauschen, Timbre, Ausdruck, musikalische Wirkung und Setting-Passung sind nicht auditiv freigegeben.','', 'Clipping-Verdacht: mindestens drei aufeinanderfolgende Samples nahe Vollaussteuerung. Endabriss-Verdacht: letzte 50 ms RMS über -40 dBFS und letzte 5 ms Peak über -35 dBFS. Vollaussteuerung kann auch aus Normalisierung/Codec-Überschwingen stammen; deshalb sind dies Verdachtsfälle. Keine LUFS- oder True-Peak-Zertifizierung.']
(ROOT/'reports'/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Verified',len(results),'master/mono pairs; original sources',len(selected))
