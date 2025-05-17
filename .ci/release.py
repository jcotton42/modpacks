#!/usr/bin/python3

import shutil
import sys
import tempfile
import tomllib

from pathlib import Path
from string import Template

ci = Path(__file__).parent

mmc_pack_template = Template(ci.joinpath('mmc-pack.json').read_text())

packs = Path(sys.argv[1])
dist = Path(sys.argv[2])
scratch = Path(tempfile.mkdtemp(dir=sys.argv[3]))

dist.mkdir()

for pack in packs.iterdir():
    if not pack.is_dir(): continue
    work = scratch.joinpath(pack.name)
    work.mkdir()
    with pack.joinpath('pack.toml').open('rb') as f:
        packToml = tomllib.load(f)
        mc = packToml['versions']['minecraft']
        neo = packToml['versions']['neoforge']

    mmc_pack = mmc_pack_template.substitute(mc=mc, neo=neo)
    work.joinpath('mmc-pack.json').write_text(mmc_pack)
    work.joinpath('instance.cfg').touch(mode=0o644)
    patches = work.joinpath('patches')
    patches.mkdir()
    shutil.copy(
        ci.joinpath('com.unascribed.unsup.json'),
        patches
    )
    minecraft = work.joinpath('minecraft')
    minecraft.mkdir()
    shutil.copy(
        pack.joinpath('unsup.ini'),
        minecraft
    )

    shutil.make_archive(dist.joinpath(pack.name), 'zip', work)
