from pathlib import Path
import urllib.request,urllib.parse,re,json,zipfile,sys,hashlib,concurrent.futures
from audio_config import CACHE
import py7zr
CACHE.mkdir(parents=True,exist_ok=True)
PACKS=[
 ('textures','https://opengameart.org/content/medieval-sound-effects-weapon-textures','Ben Jaszczak & Brian Nelson'),
 ('apparel','https://opengameart.org/content/fantasy-weapons-and-apparel-sfx-library','Vehicle / Jan Schupke'),
 ('rpg','https://opengameart.org/node/86018','rubberduck'),
 ('wood','https://opengameart.org/content/35-wooden-crackshitsdestructions','Independent.nu'),
 ('rumble','https://opengameart.org/content/rumble-fx','cinameng'),
]
def fetch(spec):
 name,url,author=spec;folder=CACHE/name;folder.mkdir(exist_ok=True)
 html=urllib.request.urlopen(url,timeout=45).read().decode('utf8')
 assert 'CC0' in html,'CC0 not found in source page'
 (folder/'source-page.html').write_text(html,encoding='utf8')
 links=re.findall(r'href=[\"\x27]([^\"\x27]+)[\"\x27]',html)
 files=list(dict.fromkeys(urllib.parse.urljoin(url,x.replace('&amp;','&')) for x in links if '/files/' in x and re.search(r'\.(zip|7z|wav)(?:\?|$)',x,re.I)))
 assert files,f'No audio archive found: {url}'
 # Part 1 contains sufficient weapon candidates for this first draft.
 chosen=files[:1] if name=='textures' else files
 out=[]
 for link in chosen:
  filename=urllib.parse.unquote(urllib.parse.urlparse(link).path.rsplit('/',1)[1]);archive=folder/filename
  if not archive.exists():urllib.request.urlretrieve(link,archive)
  dest=folder/'extracted';dest.mkdir(exist_ok=True)
  if archive.suffix.lower() in ('.zip','.7z'):
   if archive.suffix=='.zip':
    with zipfile.ZipFile(archive) as z:
     members=z.namelist()
     assert all(not Path(n).is_absolute() and '..' not in Path(n.replace('\\','/')).parts for n in members)
     z.extractall(dest)
   else:
    with py7zr.SevenZipFile(archive,'r') as z:
     members=z.getnames()
     assert all(not Path(n).is_absolute() and '..' not in Path(n.replace('\\','/')).parts for n in members)
     z.extractall(dest)
  else:
   import shutil;shutil.copy2(archive,dest/filename)
  out.append({'url':link,'filename':filename,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
 print(name,'downloaded',sum(x['bytes'] for x in out),flush=True)
 return {'name':name,'page':url,'author':author,'license':'CC0-1.0','checked':'2026-10-10','downloads':out}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(fetch,PACKS))
(Path(__file__).parent/'sources.json').write_text(json.dumps(results,indent=2),encoding='utf8')
