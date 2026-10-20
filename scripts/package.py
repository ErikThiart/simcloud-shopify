#!/usr/bin/env python3
"""Create a source/runtime ZIP from the reviewed allowlist, never a directory glob."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['python3', str(ROOT / 'scripts/public_check.py')], check=True, cwd=ROOT)
files = json.loads((ROOT / 'config/package-files.json').read_text())
version = json.loads((ROOT / 'package.json').read_text())['version']
target = ROOT / 'dist' / f'simcloud-shopify-{version}.zip'
target.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in files:
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise SystemExit('Invalid package allowlist entry: ' + name)
        info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100755 if name == '.githooks/pre-push' else 0o100644) << 16
        archive.writestr(info, path.read_bytes())
digest = hashlib.sha256(target.read_bytes()).hexdigest()
(target.parent / 'SHA256SUMS').write_text(f'{digest}  {target.name}\n')
subprocess.run(['python3', str(ROOT / 'scripts/public_check.py'), str(target)], check=True, cwd=ROOT)
print(f'Created {target.name}: {len(files)} allowlisted files; SHA-256 {digest}')
