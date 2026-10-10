"""Extract generated keyframes and package transparent drafts; no repainting."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
CLIPS=[
 ('fx_ranke_a','exec-437e269a-6d0c-419d-b9b4-f2776aa99965.png',[8,2,3,4,4,3,2,2],[[220,670,1110,1560],[220,670,1110,1560]],[435,865]),
 ('fx_ranke_b','exec-cb352fe2-507e-4505-b4b6-280a89804c24.png',[8,2,3,4,4,3,2,2],[[220,670,1110,1550],[220,670,1110,1550]],[430,835]),
 ('p3_atk_weltgericht_v2','exec-654322d4-b493-423c-9bbf-29e48486a3f9.png',[3,5,5,5,6,8,8,8],[[200,640,1080,1500],[200,655,1100,1530]],[398,803]),
 ('fx_weltgericht_saal','exec-ec3c1f03-f575-4580-9a89-1dc6e641735d.png',[6,8,10,4,8,4,4,4],[[220,665,1110,1555],[220,665,1110,1555]],[400,785]),
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
   frame.paste(crop,offset)
   if name.startswith('fx_ranke_') and idx==7:
    # The generated blank slot contains only invisible alpha=1 residue.
    # Export the intentional empty hold frame with exactly zero alpha.
    if frame.getchannel('A').getextrema()[1]>1:
     raise ValueError(f'{name}: final frame still contains visible artwork')
    frame=Image.new('RGBA',(960,720))
   frame.save(folder/f'{idx:02d}.png');frames.append(frame)
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
