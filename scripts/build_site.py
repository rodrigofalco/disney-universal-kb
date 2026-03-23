from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {'.git', '.obsidian', 'scripts', 'Assets'}
IGNORE_FILES = {'.DS_Store', 'Thumbs.db', 'site-files.json'}
ALLOWED_SUFFIXES = {'.md', '.html', '.json'}
ALLOWED_NAMES = {'README.md', '.nojekyll', '.gitignore'}

files = []
for path in sorted(ROOT.rglob('*')):
    if path.is_dir():
        continue
    rel = path.relative_to(ROOT).as_posix()
    parts = set(path.relative_to(ROOT).parts)
    if parts & IGNORE_DIRS:
        continue
    if path.name in IGNORE_FILES:
        continue
    if rel.startswith('.git/'):
        continue
    if path.name not in ALLOWED_NAMES and path.suffix.lower() not in ALLOWED_SUFFIXES:
        continue
    files.append(rel)

(ROOT / 'site-files.json').write_text(json.dumps(files, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Wrote {len(files)} entries to {ROOT / "site-files.json"}')
