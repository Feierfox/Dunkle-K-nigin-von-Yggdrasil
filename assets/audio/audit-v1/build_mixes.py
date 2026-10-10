"""Reproducible CC0 sound-design drafts and objective export checks."""
from pathlib import Path
import sys,json,math,shutil,hashlib
from audio_config import CACHE
import numpy as np,soundfile as sf
from scipy import signal
from analyze_sources import metrics
ROOT=Path(__file__).parent;SR=48000
audit=json.loads((ROOT/'source_audit.json').read_text())['files']
sources=json.loads((ROOT/'sources.json').read_text())
used={};recipes=[]
for d in ['originals','masters','psp','reports']:(ROOT/d).mkdir(exist_ok=True)
def load(pack,name):
 r=next(x for x in audit if x['pack']==pack and x['filename']==name)
 if r['suspectedClipping'] or r['suspectedAbruptEnd'] or r['peakDbFS']>.1:raise ValueError(f'Flagged source: {name}')
 path=ROOT/'originals'/pack/name
 if not path.is_file():path=CACHE/r['path']
 x,sr=sf.read(path,always_2d=True);x=x.mean(axis=1);x-=x.mean()
 x=signal.resample_poly(x,SR//math.gcd(SR,sr),sr//math.gcd(SR,sr))
 x/=max(np.max(np.abs(x)),1e-10)
 key=pack+'/'+name
 if key not in used:
  dest=ROOT/'originals'/pack/name;dest.parent.mkdir(exist_ok=True)
  if path.resolve()!=dest.resolve():shutil.copy2(path,dest)
  p=next(z for z in sources if z['name']==pack)
  used[key]={'file':str(dest.relative_to(ROOT)).replace('\\','/'),'author':p['author'],'page':p['page'],'license':p['license'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'originalMetrics':r}
 return x
def taper(x,attack=.005,release=.08):
 x=x.copy();a=min(len(x)//2,int(SR*attack));b=min(len(x)//2,int(SR*release))
 if a:x[:a]*=np.linspace(0,1,a)**2
 if b:x[-b:]*=np.linspace(1,0,b)**2
 return x
def pitch(x,factor):return signal.resample_poly(x,1000,round(1000*factor))
def filt(x,lo=70,hi=7500):return signal.sosfilt(signal.butter(2,[lo,hi],btype='bandpass',fs=SR,output='sos'),x)
def isolated_swing(x):
 # Preserve the full first gesture up to a long quiet gap, plus its tail.
 step=int(SR*.02);env=np.array([np.sqrt(np.mean(x[i:i+step]**2)) for i in range(0,len(x),step)])
 active=np.flatnonzero(env>env.max()*.12)
 groups=np.split(active,np.where(np.diff(active)>15)[0]+1)
 g=next(g for g in groups if len(g)>=3)
 start=max(0,int((g[0]*.02-.08)*SR));end=min(len(x),int((g[-1]*.02+.5)*SR))
 recipes.append({'extraction':'first Katana Swing gesture','sourceStartSeconds':start/SR,'sourceEndSeconds':end/SR,'note':'energy-based segmentation, auditory validation pending'})
 return taper(x[start:end],.005,.06)
def layer(duration,parts):
 y=np.zeros(int(duration*SR))
 for x,t,g in parts:
  start=round(t*SR);end=min(len(y),start+len(x))
  y[start:end]+=x[:end-start]*g
 return y
def hall(x,seconds=.65,wet=.10):
 rng=np.random.default_rng(431);n=int(seconds*SR);t=np.arange(n)/SR
 # Deterministic diffuse tail plus early stone-room reflections.
 out=[]
 for c in range(2):
  ir=filt(rng.normal(size=n),180,6500)*np.exp(-t*9/seconds)
  ir*=.015/max(np.sqrt(np.sum(ir*ir)),1e-9)
  for delay,gain in [(0.031+c*.004,.35),(.067-c*.003,.22),(.101+c*.007,.13)]:ir[int(delay*SR)]+=gain
  ir*=wet
  wetx=signal.fftconvolve(x,ir)
  dry=np.pad(x,(0,len(wetx)-len(x)))
  out.append(dry+wetx)
 return np.stack(out,axis=1)
def export(name,x,parts,peak=-6,space=.65):
 x=filt(taper(x,.003,.10));x=hall(x,space,.12) if space else np.stack([x,x],axis=1)
 x-=x.mean(axis=0);x=taper_stereo(x)
 x*=10**(peak/20)/max(np.max(np.abs(x)),1e-10)
 sf.write(ROOT/'masters'/f'{name}.wav',x,SR,subtype='PCM_24')
 mono=x.mean(axis=1);mono=signal.resample_poly(mono,147,320)
 sf.write(ROOT/'psp'/f'{name}.wav',mono,22050,subtype='PCM_16')
 m=metrics(x,SR);m['name']=name;m['psp']=metrics(mono,22050)
 m['stereoMonoRmsDifferenceDb']=round(20*np.log10(max(np.sqrt(np.mean(mono*mono)),1e-12)/max(np.sqrt(np.mean(x*x)),1e-12)),2)
 recipes.append({'name':name,'parts':parts,'peakTargetDbFS':peak,'hallSeconds':space,'metrics':m})
 return x
def taper_stereo(x):
 x=x.copy();n=min(int(.12*SR),len(x)//2);x[-n:]*=np.linspace(1,0,n)[:,None]**2
 return x
whoosh=isolated_swing(load('textures','Katana Swing.wav'))
blade=load('rpg','blade_03.ogg');metal=load('rpg','metal_01.ogg');stone=load('rpg','item_stone_01.ogg')
magic=load('rpg','spell_02.ogg');wood1=load('wood','crack03.mp3.flac');wood2=load('wood','impactwood03.mp3.flac')
leather=load('apparel','sheath-squeeze-01.wav');rumble=load('rumble','rumble.wav')
bed=taper(rumble[6*SR:12*SR],.20,.40)
for i in range(1,4):
 name=f'boots-leather-step-{i:02d}.wav';x=load('apparel',name)
 export(f'held_step_{i:02d}',x,[name],peak=-13,space=.35)
export('held_schwerthieb',layer(2.0,[(whoosh,0,.5),(blade,.10,.3),(metal,.18,.12)]),['Katana Swing.wav','blade_03.ogg','metal_01.ogg'],peak=-8,space=.6)
export('koenigin_richtschlag',layer(3.5,[(pitch(whoosh,.75),0,.55),(pitch(stone,.7),.43,.5),(pitch(metal,.8),.43,.35),(pitch(wood1,.8),.46,.23)]),['Katana Swing.wav','item_stone_01.ogg','metal_01.ogg','crack03.mp3.flac'],peak=-6,space=.9)
rootparts=['rumble.wav','crack03.mp3.flac','impactwood03.mp3.flac','sheath-squeeze-01.wav']
for name,factor in [('ranke_a',.85),('ranke_b',.65)]:
 export(name,layer(4.5,[(taper(bed[:3*SR],.1,.3),0,.13),(pitch(wood1,factor),8/12,.55),(pitch(wood2,factor),.72,.23),(pitch(leather,factor),21/12,.3)]),rootparts,peak=-8,space=.65)
charge=layer(2.0,[(bed[:2*SR],0,.32),(pitch(magic,.7),.65,.17),(whoosh[::-1],1.2,.12)])
charge*=np.linspace(.08,1,len(charge))**1.8
release=layer(6.0,[(bed[:5*SR],0,.35),(pitch(wood1,.65),0,.36),(pitch(wood2,.7),.04,.42),(pitch(stone,.5),0,.7),(pitch(metal,.6),.02,.5),(pitch(magic,.65),.06,.3),(pitch(wood1,.85),.3,.16)])
export('weltgericht_aufladen',charge,['rumble.wav','spell_02.ogg','Katana Swing.wav'],peak=-9,space=0)
export('weltgericht_entladung',release,rootparts+['item_stone_01.ogg','metal_01.ogg','spell_02.ogg'],peak=-3,space=1.25)
full=layer(8.5,[(charge,0,1),(release,2,1)])
export('weltgericht_demo_voller_ausklang',full,['charge 0–2 s','release from 2 s; demonstration tail, not death-silence game mix'],peak=-3,space=1.25)
# Deliberately separate version for the documented immediate death silence.
short=layer(2.22,[(charge,0,1),(release[:int(.22*SR)],2,1)])
export('weltgericht_todesstille',short,['charge 0–2 s','release 0.22 s with shaped fade; deliberate design, not repaired missing tail'],peak=-3,space=0)
(ROOT/'selected_sources.json').write_text(json.dumps(list(used.values()),indent=2),encoding='utf8')
(ROOT/'mix_recipes.json').write_text(json.dumps(recipes,indent=2),encoding='utf8')
for r in recipes:
 if 'metrics' in r:
  m=r['metrics'];assert not m['suspectedClipping'] and not m['suspectedAbruptEnd'];assert abs(m['stereoMonoRmsDifferenceDb'])<3
  print(r['name'],m['seconds'],'s',m['peakDbFS'],'dBFS','tail',m['tail50msRmsDbFS'],'mono',m['stereoMonoRmsDifferenceDb'],'dB')
