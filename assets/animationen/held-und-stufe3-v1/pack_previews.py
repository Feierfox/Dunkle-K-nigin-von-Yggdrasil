"""Extract generated keyframes and package transparent drafts; no repainting."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
CLIPS=[
 ('held_sprung','exec-01ef07d2-04d6-4244-92e0-997688f00b1c.png',[1]*8,[[220,680,1110,1560],[240,680,1140,1560]],[438,875]),
 ('held_rolle','exec-7f1a18be-7642-451c-ae73-35f75c45ba7b.png',[1]*8,[[250,700,1150,1570],[240,690,1120,1570]],[422,845]),
 ('held_amulett_schild','exec-60099b9b-d97d-4635-a28a-76c36bcd4d80.png',[2,2,2,2,5,5,2,2],[[240,680,1110,1550],[240,680,1110,1550]],[440,882]),
 ('p3_atk_ranken','exec-b3a81b7b-d8ac-4e3c-8967-5ca1962b2f4b.png',[3,4,4,3,4,4,3,3],[[210,650,1100,1550],[260,740,1160,1560]],[420,845]),
 ('p3_atk_erinnerungsriss','exec-bd26c750-5f9d-44a8-94cd-a72164d59f83.png',[2,2,2,2,3,3,2,2],[[265,725,1130,1570],[330,840,1220,1590]],[397,820]),
 ('p3_atk_weltgericht','exec-7efdcb12-08e9-4695-944d-3ae87dc9db3d.png',[4,6,6,8,4,8,6,6],[[240,670,1110,1550],[250,765,1160,1560]],[402,807]),
]
reports=[]
for name,src,ticks,anchors,baselines in CLIPS:
 folder=ROOT/name; folder.mkdir(parents=True,exist_ok=True)
 # The selected source sheet is included in each clip directory.
 # Original generation identifiers in CLIPS document provenance only.
 if not (folder/'source-sheet.png').is_file():
  raise FileNotFoundError(f'{name}: source-sheet.png is required')
 im=Image.open(folder/'source-sheet.png').convert('RGBA');w,h=im.size
 a=np.asarray(im)[:,:,3];frames=[];entries=[];bounds=[]
 for row in range(2):
  y0=row*h//2;y1=(row+1)*h//2;counts=(a[y0:y1]>20).sum(axis=0);cuts=[0]
  for i in range(1,4):
   lo=int((i-.30)*w/4);hi=int((i+.30)*w/4);v=counts[lo:hi]
   cand=np.where(v==v.min())[0]+lo;x=int(cand[np.argmin(abs(cand-i*w/4))]);cuts.append(x)
   if counts[x]>0: raise ValueError(f'{name}: visible art at row {row}, x {x}, count {counts[x]}')
  cuts.append(w);bounds.append(cuts)
  for col in range(4):
   idx=row*4+col;rect=(cuts[col],y0,cuts[col+1],y1);crop=im.crop(rect)
   frame=Image.new('RGBA',(960,720));offset=(480+cuts[col]-anchors[row][col],600+y0-baselines[row])
   bbox=crop.getbbox()
   if bbox:
    b=(bbox[0]+offset[0],bbox[1]+offset[1],bbox[2]+offset[0],bbox[3]+offset[1])
    if b[0]<0 or b[1]<0 or b[2]>960 or b[3]>720:raise ValueError(f'{name}: clipped frame {idx}: {b}')
   frame.paste(crop,offset);frame.save(folder/f'{idx:02d}.png');frames.append(frame)
   entries.append({'index':idx,'sourceRect':{'x':cuts[col],'y':y0,'w':crop.width,'h':crop.height},'frame':{'x':col*960,'y':row*720,'w':960,'h':720},'durationTicks':ticks[idx],'anchor':{'x':480,'y':600}})
 sheet=Image.new('RGBA',(3840,1440))
 for idx,f in enumerate(frames):sheet.paste(f,((idx%4)*960,(idx//4)*720))
 sheet.save(folder/'sheet.png')
 preview=[]
 for f in frames:
  bg=Image.new('RGBA',f.size,(18,18,34,255));bg.alpha_composite(f);preview.append(bg.convert('RGB'))
 preview.append(preview[-1].copy())
 preview[0].save(folder/'preview.gif',save_all=True,append_images=preview[1:],duration=[round(t*1000/12) for t in ticks]+[700],loop=0,disposal=2)
 data={'name':name,'status':'keyframe-animation-draft','productionReady':False,'fps':12,'loop':False,'keyframeCount':8,'totalTicks':sum(ticks),'sheet':'sheet.png','frames':entries}
 (folder/'animation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
 reports.append({'name':name,'sourceSize':[w,h],'alphaExtrema':im.getchannel('A').getextrema(),'uniqueRGBAColors':len(im.getcolors(w*h) or []),'cuts':bounds,'keyframes':8,'totalTicks':sum(ticks)})
 print(name,'OK',sum(ticks),'ticks')
(ROOT/'validation.json').write_text(json.dumps(reports,indent=2),encoding='utf8')
