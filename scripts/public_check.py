#!/usr/bin/env python3
"""Bounded source/history/package privacy checks. Never print matched sensitive values."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'dist', '.shopify', '__pycache__', 'test-results', 'playwright-report'}
PATTERNS = [
    rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'shpat_[a-fA-F0-9]{20,}',
    rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    rb'/' + rb'Users/[^\s\"\x27]+', rb'/home/[a-z][a-z0-9_-]+/(?:public_html|app|vendor)',
    rb'(?:ftp|ftps)://[^\s\"\x27]+',
    rb'https://(?:www\.)?simcloud\.co\.za/(?!api(?:/|[\"\x27\s])|img/)[A-Za-z0-9_/?=&.-]+',
]
BAD_NAME = re.compile(r'(?:^|/)(?:\.env(?:\..*)?|config\.php|.*\.local\.(?:php|toml)|.*\.(?:sqlite(?:-.*)?|db|pem|key|p12|pfx|log|bak|sql)|private|storage|runtime)(?:/|$)', re.I)
errors = []
image_hashes = {}
image_hashes.update(json.loads((ROOT / 'config/public-images.json').read_text()))

def inspect(name, data, context):
    if Path(name).suffix.lower() == '.php' or name.split('/')[0] in {'app', 'bin', 'public', 'server', 'runtime'}:
        errors.append(f'{context}: hosted server code is forbidden: {name}')
    if BAD_NAME.search(name):
        errors.append(f'{context}: forbidden private/runtime path {name}')
    if Path(name).suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
        if image_hashes.get(name) != hashlib.sha256(data).hexdigest():
            errors.append(f'{context}: image requires provenance/privacy review: {name}')
        return
    if b'\x00' in data:
        errors.append(f'{context}: unexpected binary file {name}')
        return
    if any(re.search(pattern, data) for pattern in PATTERNS):
        errors.append(f'{context}: sensitive pattern in {name}')
    if name == 'shopify.app.toml' and (b'client_id = "REPLACE_WITH_YOUR_PUBLIC_APP_CLIENT_ID"' not in data or b'application_url = "https://app.example.com"' not in data):
        errors.append(f'{context}: public app template contains an account binding')
    # Forbid literal PHP account tokens/secrets; examples use empty strings, tests generate random secrets.
    secret = rb"[\"'](?:client_secret|access_token|refresh_token|simcloud_token|encryption_key)[\"']\s*(?:=>|:)\s*[\"']([^\"']{16,})[\"']"
    for match in re.finditer(secret, data):
        if name == 'public/demo.php' and match.group(1) == b'demo-only-no-credential':
            continue
        errors.append(f'{context}: literal credential assignment in {name}')

count = 0
tracked = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT, capture_output=True)
paths = [ROOT / name.decode() for name in tracked.stdout.split(b'\x00') if name] if tracked.returncode == 0 else ROOT.rglob('*')
for path in paths:
    if not path.is_file() or any(part in SKIP for part in path.relative_to(ROOT).parts):
        continue
    name = path.relative_to(ROOT).as_posix()
    if path.is_symlink(): errors.append('Symlinks are not permitted: ' + name)
    inspect(name, path.read_bytes(), 'tree'); count += 1

history = subprocess.run(['git', 'rev-list', '--objects', '--all'], cwd=ROOT, text=True, capture_output=True)
blob_count = 0
if history.returncode == 0:
    for line in history.stdout.splitlines():
        oid, _, name = line.partition(' ')
        if not name: continue
        kind = subprocess.check_output(['git', 'cat-file', '-t', oid], cwd=ROOT).strip()
        if kind != b'blob': continue
        inspect(name, subprocess.check_output(['git', 'cat-file', 'blob', oid], cwd=ROOT), 'history'); blob_count += 1

for value in sys.argv[1:]:
    with zipfile.ZipFile(value) as archive:
        allow = set(json.loads((ROOT / 'config/package-files.json').read_text()))
        if set(archive.namelist()) != allow: errors.append('Package contents differ from allowlist')
        for name in archive.namelist():
            if name.startswith('/') or '..' in Path(name).parts: errors.append('Unsafe ZIP path')
            inspect(name, archive.read(name), 'package')
if errors:
    print('\n'.join(sorted(set(errors))), file=sys.stderr)
    raise SystemExit(1)
print(f'Public-source checks passed: {count} files, {blob_count} reachable history blobs, {len(sys.argv)-1} packages. No sensitive values printed.')
