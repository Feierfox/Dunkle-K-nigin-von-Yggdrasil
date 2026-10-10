"""16-second title preview and PSP menu media. Needs public encoders."""
from pathlib import Path
import argparse,sys,os,json,urllib.request,re,urllib.parse,hashlib,subprocess,math
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/menu/koenigin-preview-v1';OUT.mkdir(parents=True,exist_ok=True)
def run(cmd):
 p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-4000:])
 return p.stdout
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--toolkit',type=Path,required=True);args=ap.parse_args()
 paths=json.loads((Path.home()/'.cache/dark-queen-preview-tools/paths.json').read_text())
 ff=paths['ffmpeg'];os.environ['PATH']=str(Path(ff).parent)+os.pathsep+str(Path(paths['atracdenc']).parent)+os.pathsep+os.environ['PATH']
 page='https://opengameart.org/content/the-final-battle'
 html=urllib.request.urlopen(page,timeout=45).read().decode('utf8')
 assert 'CC0' in html
 links=re.findall(r'href=[\"\x27]([^\"\x27]+)[\"\x27]',html)
 url=next(urllib.parse.urljoin(page,l) for l in links if '/files/' in l and l.endswith('the_final_battle.ogg'))
 original=OUT/'the_final_battle-original.ogg'
 if not original.exists():urllib.request.urlretrieve(url,original)
 # Keep the composer's opening section; consciously fade clip boundaries.
 audio=OUT/'theme-16s.wav'
 run([ff,'-y','-v','error','-i',original,'-t','16','-af','afade=t=in:st=0:d=0.35,afade=t=out:st=14.6:d=1.4,volume=0.65','-ar','44100','-ac','2','-c:a','pcm_s16le',audio])
 art=OUT/'koenigin-helm-lila-v1.png'
 video=OUT/'preview-16s.mp4'
 graph="[0:v]scale=1440:-2,crop=1440:816:0:0,zoompan=z='1+0.03*(1-cos(2*PI*on/480))/2':x='iw/2-iw/zoom/2':y=0:d=1:s=720x408:fps=30[base];[2:v]format=rgba,geq=r='130':g='30':b='200':a='22*(0.55+0.45*sin(2*PI*T/4))*exp(-pow((X-373)/85,2)-pow((Y-149)/30,2))*(0.7+0.3*sin(X/20+T))'[fog];[base][fog]overlay=shortest=1,format=yuv420p[out]"
 run([ff,'-y','-v','error','-loop','1','-framerate','30','-i',art,'-i',audio,'-f','lavfi','-i','color=c=black:s=720x408:r=30','-filter_complex',graph,'-map','[out]','-map','1:a','-t','16','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','160k','-movflags','+faststart',video])
 print('16-second video rendered',flush=True)
 toolkit=args.toolkit/'pspmedia.py'
 print(run([sys.executable,toolkit,'snd0',audio,'-o',ROOT/'psp/SND0.AT3','--encoder','atracdenc','--codec','at3']),flush=True)
 print(run([sys.executable,toolkit,'convert',video,'-o',ROOT/'psp/ICON1.PMF','--budget-kb','280']),flush=True)
 total=(ROOT/'psp/ICON1.PMF').stat().st_size+(ROOT/'psp/SND0.AT3').stat().st_size
 assert total<=500*1024,'Combined XMB media budget exceeded'
 toolmeta=json.loads((args.toolkit/'SOURCE.json').read_text()) if (args.toolkit/'SOURCE.json').exists() else {'commit':run(['git','-C',args.toolkit,'rev-parse','HEAD']).strip()}
 provenance={'music':'The Final Battle','author':'skrjablin','license':'CC0-1.0','source':page,'download':url,'originalSHA256':hashlib.sha256(original.read_bytes()).hexdigest(),'excerptStartSeconds':0,'excerptSeconds':16,'edits':'0.35s fade-in; 1.4s fade-out; 65% gain','preview':'720x408, H.264/AAC, 16s','xmbVideo':'144x80 PSMF/H.264','xmbMusic':'ATRAC3, 44.1 kHz stereo','combinedXmbBytes':total,'toolkitSource':'https://github.com/TotalKommando/psp-media-toolkit','toolkitCommit':toolmeta['commit'],'pspHardwareTested':False}
 (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf8')
 print('Combined ICON1 + SND0:',total,'bytes',flush=True)
if __name__=='__main__':main()
