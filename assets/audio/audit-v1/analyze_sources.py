from pathlib import Path
import sys,json,math
from audio_config import CACHE
import numpy as np,soundfile as sf
ROOT=Path(__file__).parent
def db(x):return float(20*np.log10(max(float(x),1e-12)))
def metrics(x,sr):
 if x.ndim==1:x=x[:,None]
 p=np.max(np.abs(x),axis=1);n=max(1,int(.05*sr));last=max(1,int(.005*sr))
 above=np.flatnonzero(p>10**(-50/20))
 tail=db(np.sqrt(np.mean(x[-n:]**2)));endpoint=db(np.max(np.abs(x[-last:])))
 clip=p>=.9999;changes=np.flatnonzero(np.diff(np.r_[False,clip,False]));runs=changes[1::2]-changes[::2]
 return {'seconds':round(len(x)/sr,4),'sampleRate':sr,'channels':x.shape[1],'peakDbFS':round(db(p.max()),2),'rmsDbFS':round(db(np.sqrt(np.mean(x*x))),2),'dc':round(float(abs(x.mean())),7),'tail50msRmsDbFS':round(tail,2),'endpoint5msPeakDbFS':round(endpoint,2),'nearFullScaleSamples':int(clip.sum()),'maxFullScaleRun':int(runs.max()) if len(runs) else 0,'leadingBelowMinus50ms':round(1000*above[0]/sr,2) if len(above) else None,'trailingBelowMinus50ms':round(1000*(len(x)-1-above[-1])/sr,2) if len(above) else None,'suspectedAbruptEnd':bool(tail>-40 and endpoint>-35),'suspectedClipping':bool(len(runs) and runs.max()>=3)}
def main():
 out=[];errors=[]
 for f in sorted(CACHE.glob('*/extracted/**/*')):
  if f.is_file() and f.suffix.lower() in ('.wav','.ogg','.flac','.mp3') and 'preview' not in f.name.lower():
   try:
    x,sr=sf.read(f,always_2d=True,dtype='float32')
    if len(x):out.append({'pack':f.relative_to(CACHE).parts[0],'path':f.relative_to(CACHE).as_posix(),'filename':f.name,**metrics(x,sr)})
   except Exception as e:errors.append({'path':f.relative_to(CACHE).as_posix(),'error':str(e)})
 if not out:raise FileNotFoundError('No extracted audio in cache; run download_sources.py first')
 (ROOT/'source_audit.json').write_text(json.dumps({'files':out,'decodeErrors':errors},indent=2),encoding='utf8')
 print('Files',len(out),'abrupt-end flags',sum(r['suspectedAbruptEnd'] for r in out),'clipping flags',sum(r['suspectedClipping'] for r in out),'decode errors',len(errors))
if __name__=='__main__':main()
