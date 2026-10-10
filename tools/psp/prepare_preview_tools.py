"""Download portable public encoders; no system installation."""
from pathlib import Path
import urllib.request,json,zipfile,hashlib,concurrent.futures
CACHE=Path.home()/'.cache'/'dark-queen-preview-tools';CACHE.mkdir(parents=True,exist_ok=True)
def download(url,dest):
 if not dest.exists():urllib.request.urlretrieve(url,dest)
 return dest
def unpack(archive,where):
 where.mkdir(exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  assert all(not Path(n).is_absolute() and '..' not in Path(n.replace('\\','/')).parts for n in z.namelist())
  z.extractall(where)
def ffmpeg():
 url='https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
 archive=download(url,CACHE/'ffmpeg.zip')
 expected=urllib.request.urlopen(url+'.sha256',timeout=45).read().decode().strip().split()[0]
 actual=hashlib.sha256(archive.read_bytes()).hexdigest();assert actual==expected,'FFmpeg checksum mismatch'
 unpack(archive,CACHE/'ffmpeg')
 exe=next((CACHE/'ffmpeg').glob('*/bin/ffmpeg.exe'))
 print('FFmpeg ready',flush=True);return {'ffmpeg':str(exe),'ffprobe':str(exe.with_name('ffprobe.exe')),'ffmpegSHA256':actual}
def atrac():
 request=urllib.request.Request('https://api.github.com/repos/dcherednik/atracdenc/releases',headers={'User-Agent':'DarkQueenPreviewBuild'})
 releases=json.load(urllib.request.urlopen(request,timeout=45))
 assets=[a for r in releases for a in r['assets'] if 'win' in a['name'].lower() and a['name'].endswith('.zip')]
 assert assets,'No Windows ATRAC encoder release'
 asset=next((a for a in assets if '0.2.1' in a['name']),assets[0])
 archive=download(asset['browser_download_url'],CACHE/asset['name']);unpack(archive,CACHE/'atrac')
 exe=next((CACHE/'atrac').rglob('atracdenc.exe'))
 print('ATRAC encoder ready',flush=True);return {'atracdenc':str(exe),'atracURL':asset['browser_download_url'],'atracSHA256':hashlib.sha256(archive.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(lambda f:f(),[ffmpeg,atrac]))
paths={k:v for r in results for k,v in r.items()}
(CACHE/'paths.json').write_text(json.dumps(paths,indent=2),encoding='utf8')
print('Portable encoders downloaded and extracted.')
