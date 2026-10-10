"""Export title artwork and replace only the existing PBP menu resources.

Usage: python tools/psp/menu_bauen.py --repack --media
Requires Pillow. The compiled game and other PBP sections remain unchanged.
"""
from pathlib import Path
import argparse,struct,hashlib,json,os
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'assets/menu/thronsaal-title-v1'
PSP=ROOT/'psp'
TITLE='The Dark Queen of Yggdrasil'
def parse_pbp(blob):
 assert blob[:4]==b'\x00PBP','Invalid PBP magic'
 offsets=struct.unpack('<8I',blob[8:40])
 assert offsets[0]>=40 and all(a<=b for a,b in zip(offsets,offsets[1:]))
 assert offsets[-1]<=len(blob)
 return [blob[offsets[i]:(offsets[i+1] if i<7 else len(blob))] for i in range(8)]
def title_sfo(blob):
 data=bytearray(blob)
 magic,version,keys,values,count=struct.unpack('<4s4I',data[:20])
 assert magic==b'\x00PSF','Invalid SFO magic'
 for i in range(count):
  pos=20+i*16;key,fmt,length,capacity,offset=struct.unpack('<HHIII',data[pos:pos+16])
  name=bytes(data[keys+key:]).split(b'\x00',1)[0].decode('utf8')
  if name=='TITLE':
   encoded=TITLE.encode('utf8')+b'\x00'
   assert len(encoded)<=capacity,'SFO TITLE capacity too small'
   data[values+offset:values+offset+capacity]=encoded+b'\x00'*(capacity-len(encoded))
   struct.pack_into('<I',data,pos+4,len(encoded))
   return bytes(data)
 raise ValueError('No TITLE in SFO')
def main():
 args=argparse.ArgumentParser();args.add_argument('--repack',action='store_true');args.add_argument('--media',action='store_true',help='Also embed ICON1.PMF and SND0.AT3');opt=args.parse_args()
 if opt.media and not opt.repack:args.error('--media requires --repack')
 for master,name,size in [('wallpaper-master.png','PIC1.PNG',(480,272)),('icon-master.png','ICON0.PNG',(144,80))]:
  im=Image.open(ART/master).convert('RGB')
  ImageOps.fit(im,size,method=Image.Resampling.LANCZOS).save(PSP/name,optimize=True)
 report={'title':TITLE,'PIC1':[480,272],'ICON0':[144,80],'xmbHardwareTested':False}
 if opt.repack:
  path=PSP/'EBOOT.PBP';original=path.read_bytes();old=parse_pbp(original);parts=old.copy()
  parts[0]=title_sfo(old[0]);parts[1]=(PSP/'ICON0.PNG').read_bytes();parts[4]=(PSP/'PIC1.PNG').read_bytes()
  if opt.media:
   parts[2]=(PSP/'ICON1.PMF').read_bytes();parts[5]=(PSP/'SND0.AT3').read_bytes()
   assert parts[2][:4]==b'PSMF' and parts[5][:4]==b'RIFF'
   assert len(parts[2])+len(parts[5])<=500*1024
  offsets=[];pos=40
  for part in parts:offsets.append(pos);pos+=len(part)
  packed=original[:8]+struct.pack('<8I',*offsets)+b''.join(parts)
  checked=parse_pbp(packed)
  assert checked[1]==(PSP/'ICON0.PNG').read_bytes() and checked[4]==(PSP/'PIC1.PNG').read_bytes()
  assert TITLE.encode()+b'\x00' in checked[0]
  unchanged=[3,6,7] if opt.media else [2,3,5,6,7]
  assert all(checked[i]==old[i] for i in unchanged),'Non-menu resource changed'
  if opt.media:
   assert checked[2]==parts[2] and checked[5]==parts[5]
   report.update({'videoEmbedded':True,'musicEmbedded':True,'combinedMediaBytes':len(parts[2])+len(parts[5])})
  temp=path.with_suffix('.PBP.tmp');temp.write_bytes(packed);os.replace(temp,path)
  report.update({'pbpMenuUpdated':True,'gamePayloadUnchanged':True,'gamePayloadSHA256':hashlib.sha256(checked[6]).hexdigest()})
 (ART/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
