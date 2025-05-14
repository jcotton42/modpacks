#!/usr/bin/python3

import re
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
    if not pack.is_dir(): continue
    work = scratch.joinpath(pack.name)
    work.mkdir()
    packToml = pack.joinpath('pack.toml').read_text()
    mc = re.search(r'^minecraft *= *"(.+)"$', packToml, re.MULTILINE).group(1)
    neo = re.search(r'^neoforge *= *"(.+)"$', packToml, re.MULTILINE).group(1)

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
