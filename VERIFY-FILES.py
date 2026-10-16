#!/usr/bin/env python3
"""Run from the merged document root: python VERIFY-FILES.py"""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
manifest=json.loads((root/'FILE-INVENTORY.json').read_text())
fail=[]
for item in manifest['files']:
 p=root/item['file']
 if not p.is_file():fail.append(item['file']+': missing');continue
 if item['sha256'] and hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:fail.append(item['file']+': hash mismatch')
expected={x['file'] for x in manifest['files']}
extra=[p.name for p in root.iterdir() if p.is_file() and p.name not in expected]
print(json.dumps({'files':len(expected),'failures':fail,'extra_files':extra},indent=2))
raise SystemExit(bool(fail))
