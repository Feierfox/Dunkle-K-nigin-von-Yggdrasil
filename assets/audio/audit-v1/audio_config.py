"""Optional local dependency/cache overrides; ordinary virtualenvs also work."""
from pathlib import Path
import os,sys
if os.environ.get('DARK_QUEEN_AUDIO_DEPS'):
 sys.path.insert(0,os.environ['DARK_QUEEN_AUDIO_DEPS'])
CACHE=Path(os.environ.get('DARK_QUEEN_AUDIO_CACHE',str(Path.home()/'.cache'/'dark-queen-audio')))
