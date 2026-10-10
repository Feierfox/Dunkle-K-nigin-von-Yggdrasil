from pathlib import Path
import sys,json,subprocess,importlib.util,io,contextlib,re,struct
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/menu/koenigin-preview-v1'
spec=importlib.util.spec_from_file_location('pspmedia',ROOT/'tools/psp/vendor/psp-media-toolkit/pspmedia.py')
media=importlib.util.module_from_spec(spec);spec.loader.exec_module(media)
paths=json.loads((Path.home()/'.cache/dark-queen-preview-tools/paths.json').read_text())
buf=io.StringIO()
with contextlib.redirect_stdout(buf):info=media.analyze_pmf(str(ROOT/'psp/ICON1.PMF'))
report=buf.getvalue();assert 'sizes OK (cover 480/480 AUs)' in report
gap=float(re.search(r'maxGap=([\d.]+)s',report)[1]);assert gap<.7
assert info['aus']==480
total=(ROOT/'psp/ICON1.PMF').stat().st_size+(ROOT/'psp/SND0.AT3').stat().st_size;assert total<=500*1024
decode=subprocess.run([paths['ffmpeg'],'-v','error','-i',str(ROOT/'psp/SND0.AT3'),'-f','null','-'],capture_output=True)
assert decode.returncode==0,decode.stderr.decode(errors='replace')
pbp=(ROOT/'psp/EBOOT.PBP').read_bytes();o=struct.unpack('<8I',pbp[8:40])
parts=[pbp[o[i]:(o[i+1] if i<7 else len(pbp))] for i in range(8)]
assert parts[1]==(ROOT/'psp/ICON0.PNG').read_bytes()
assert parts[2]==(ROOT/'psp/ICON1.PMF').read_bytes()
assert parts[4]==(ROOT/'psp/PIC1.PNG').read_bytes()
assert parts[5]==(ROOT/'psp/SND0.AT3').read_bytes()
tool=json.loads((ROOT/'tools/psp/vendor/psp-media-toolkit/SOURCE.json').read_text())
prov=json.loads((OUT/'provenance.json').read_text());prov['toolkitCommit']=tool['commit']
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n',encoding='utf8')
(OUT/'verification.txt').write_text(report+'\nATRAC decode: OK\nPBP embedded resources: byte-identical\nCombined media bytes: '+str(total)+'\nReal PSP hardware test: not performed\n',encoding='utf8')
print('480 PMF frames; max PTS gap',gap,'s; ATRAC decode OK; embedded resources OK;',total,'bytes combined')
