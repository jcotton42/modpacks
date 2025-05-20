#!/usr/bin/python3

import sys

from pathlib import Path

site_root = Path(sys.argv[1])
launcher_packs_root = Path(sys.argv[2])
index_md = Path(sys.argv[3])

text = 'Available modpacks'

for pack in sorted(launcher_packs_root.iterdir(), key=lambda p: p.stem):
    text += f'\n- [{pack.stem}]({pack.relative_to(site_root)})'

index_md_text = index_md.read_text()
site_root.joinpath('index.md').write_text(index_md_text.replace('##PACK_LIST##', text))
