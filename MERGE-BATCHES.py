#!/usr/bin/env python3
"""Usage: python MERGE-BATCHES.py PATH_TO_dev_OR_dev1 OUTPUT_DOCUMENT_ROOT"""
from pathlib import Path
import sys,shutil
source=Path(sys.argv[1]).resolve();target=Path(sys.argv[2]).resolve()
assert source.name in ['dev','dev1'], 'Choose one version folder, not the ZIP root'
assert source!=target and source not in target.parents, 'Output must be outside the package'
files=[]
for batch in sorted(source.iterdir()):
 if not batch.is_dir() or len(batch.name)!=3 or not batch.name.isdigit():raise SystemExit('Unexpected batch '+str(batch))
 items=list(batch.iterdir())
 assert len(items)<=100 and all(p.is_file() for p in items), 'Invalid batch'
 files.extend(items)
assert len(files)<=1000 and len({p.name.casefold() for p in files})==len(files), 'Count or name conflict'
target.mkdir(parents=True,exist_ok=True)
for p in files:
 dst=target/p.name
 if dst.exists() and dst.read_bytes()!=p.read_bytes():raise SystemExit('Refusing to overwrite different file: '+str(dst))
 shutil.copy2(p,dst)
print(str(target)+': '+str(len(files))+' files merged. Run VERIFY-FILES.py there.')
