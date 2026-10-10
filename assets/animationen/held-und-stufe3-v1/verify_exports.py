from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent
for p in sorted(root.glob('*/animation.json')):
 d=json.loads(p.read_text(encoding='utf8'))
 s=Image.open(p.parent/'sheet.png'); g=Image.open(p.parent/'preview.gif')
 assert len(d['frames'])==8
 assert sum(f['durationTicks'] for f in d['frames'])==d['totalTicks']
 assert s.mode=='RGBA' and s.getchannel('A').getextrema()[0]==0
 assert all(f['frame']['x']+f['frame']['w']<=s.width and f['frame']['y']+f['frame']['h']<=s.height for f in d['frames'])
 assert g.n_frames>=8
 assert all((p.parent/f'{i:02d}.png').exists() for i in range(8))
 print(d['name'],s.size,g.n_frames,'OK')
