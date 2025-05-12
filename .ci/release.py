import shutil
import sys

from pathlib import Path
from string import Template

ci = Path(__file__).parent

dist = ci.joinpath('dist')
dist.mkdir()

scratch = ci.joinpath('scratch')
scratch.mkdir()

mmc_pack_template = Template(ci.joinpath('mmc-pack.json').read_text())

packs = Path(sys.argv[1])

for pack in packs.iterdir():
    work = scratch.joinpath(pack.name)
    
