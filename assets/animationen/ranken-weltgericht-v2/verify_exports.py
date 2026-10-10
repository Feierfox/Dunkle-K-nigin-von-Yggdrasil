from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent
for p in sorted(root.glob('*/animation.json')):
 d=json.loads(p.read_text(encoding='utf8'))
 s=Image.open(p.parent/'sheet.png');g=Image.open(p.parent/'preview.gif')
 assert len(d['frames'])==8
 assert sum(f['durationTicks'] for f in d['frames'])==d['totalTicks']
 assert s.mode=='RGBA' and s.getchannel('A').getextrema()[0]==0
 assert all(f['frame']['x']+f['frame']['w']<=s.width and f['frame']['y']+f['frame']['h']<=s.height for f in d['frames'])
 assert g.n_frames>=8
 if d['name'].startswith('fx_ranke_'):
  assert Image.open(p.parent/'07.png').getchannel('A').getextrema()==(0,0)
  assert d['frames'][0]['durationTicks']==8
  assert sum(f['durationTicks'] for f in d['frames'][:5])==21
  assert d['frames'][0]['anchor']==d['frames'][6]['anchor']
 if d['name']=='p3_atk_weltgericht_v2':
  assert sum(f['durationTicks'] for f in d['frames'][:5])==24
 if d['name']=='fx_weltgericht_saal':
  assert sum(f['durationTicks'] for f in d['frames'][:3])==24
 print(d['name'],'OK',d['totalTicks'],'ticks')
spec=json.loads((root/'attack_spec.json').read_text(encoding='utf8'))
assert spec['worldJudgement']['instantKill'] and spec['worldJudgement']['unavoidable']
assert not spec['worldJudgement']['amuletProtects']
assert spec['worldJudgement']['lethalTick']==24
