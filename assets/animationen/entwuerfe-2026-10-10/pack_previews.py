"""Package Imagegen keyframes without repainting or resampling source artwork.
This is a concept preview export, not the PSP production sprite pipeline.
"""
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\Users\Flavi\.codex\generated_images\01a121e4-17ed-7150-affc-b68cb69192d3')
CLIPS = [
    ('p1_atk_richtschlag', 'exec-06b82ef4-4ba8-4b08-8a8b-56b477096b15.png', 5,
     [[210,650,1010,1390,1800],[215,625,1030,1410,1820]], [390,754], [1]*10),
    ('held_atk_hieb', 'exec-562d3ee4-603a-4210-841b-9e67723e6e63.png', 4,
     [[200,700,1120,1550],[210,680,1130,1600]], [421,826], [1]*8),
    ('p1_ritual_umarmung_feuer', 'exec-cf14a234-2ff7-405a-970e-7b80f7510b73.png', 4,
     [[300,720,1140,1570],[240,680,1120,1580]], [438,832], [3,3,3,4,8,8,6,8]),
]

report=[]
for name, filename, cols, anchors, baselines, ticks in CLIPS:
    folder=ROOT/name
    folder.mkdir(parents=True,exist_ok=True)
    shutil.copy2(SOURCE/filename, folder/'source-sheet.png')
    im=Image.open(folder/'source-sheet.png').convert('RGBA')
    w,h=im.size
    alpha=np.asarray(im)[:,:,3]
    frames=[]; metadata=[]; cuts_report=[]
    for row in range(2):
        y0=row*h//2; y1=(row+1)*h//2
        counts=(alpha[y0:y1]>20).sum(axis=0)
        cuts=[0]
        for i in range(1,cols):
            lo=int((i-.25)*w/cols); hi=int((i+.30)*w/cols)
            segment=counts[lo:hi]
            candidates=np.where(segment==segment.min())[0]+lo
            # Empty space nearest nominal boundary, preserving uneven AI layout.
            x=int(candidates[np.argmin(abs(candidates-i*w/cols))])
            cuts.append(x)
            if int(counts[x])>0:
                raise ValueError(f'{name}: frame boundary intersects artwork at {x}, row {row}')
        cuts.append(w)
        cuts_report.append(cuts)
        for col in range(cols):
            idx=row*cols+col
            region=(cuts[col],y0,cuts[col+1],y1)
            crop=im.crop(region)
            # Translation only. Keep the source RGBA pixels and alpha unchanged.
            canvas=Image.new('RGBA',(720,600))
            offset=(360+cuts[col]-anchors[row][col],520+y0-baselines[row])
            bbox=crop.getbbox()
            if bbox:
                translated=(bbox[0]+offset[0],bbox[1]+offset[1],bbox[2]+offset[0],bbox[3]+offset[1])
                if not (translated[0]>=0 and translated[1]>=0 and translated[2]<=720 and translated[3]<=600):
                    raise ValueError(f'{name} frame {idx} clipped: {translated}')
            canvas.paste(crop,offset)
            canvas.save(folder/f'{idx:02d}.png')
            frames.append(canvas)
            metadata.append({'index':idx,'sourceRect':{'x':region[0],'y':region[1],'w':crop.width,'h':crop.height},'sourceAnchor':{'x':anchors[row][col],'y':baselines[row]},'durationTicks':ticks[idx],'durationMs':round(ticks[idx]*1000/12)})
    packed=Image.new('RGBA',(720*cols,600*2))
    for i,frame in enumerate(frames):
        packed.paste(frame,((i%cols)*720,(i//cols)*600))
        metadata[i]['frame']={'x':(i%cols)*720,'y':(i//cols)*600,'w':720,'h':600}
    packed.save(folder/'sheet.png')
    # GIF is only a dark-background playback preview. RGBA PNGs retain true alpha.
    previews=[]
    for frame in frames:
        bg=Image.new('RGBA',frame.size,(18,18,34,255))
        bg.alpha_composite(frame)
        previews.append(bg.convert('RGB'))
    durations=[round(1000*t/12) for t in ticks]+[700]
    previews.append(previews[-1].copy())
    previews[0].save(folder/'preview.gif',save_all=True,append_images=previews[1:],duration=durations,loop=0,disposal=2)
    data={'name':name,'status':'concept-animation-draft','fps':12,'loop':False,'previewLoops':True,'image':'sheet.png','canvas':{'w':720,'h':600},'anchor':{'x':360,'y':520},'frames':metadata,'productionReady':False}
    (folder/'animation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    report.append({'name':name,'frames':len(frames),'sourceSize':[w,h],'cuts':cuts_report,'alphaExtrema':im.getchannel('A').getextrema(),'colors':len(im.getcolors(w*h) or []),'totalTicks':sum(ticks)})
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))

