#!/usr/bin/env python3
"""Check the shared skills and Codex marketplace wiring."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
marketplace = json.loads((root / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
entry = next(p for p in marketplace['plugins'] if p['name'] == 'dev-methodology')
plugin = (root / entry['source']['path']).resolve()
assert plugin == root / 'plugins/dev-methodology', 'invalid marketplace path'
manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
assert (plugin / manifest['hooks']).is_file(), 'missing Codex hooks'
hooks = json.loads((plugin / manifest['hooks']).read_text(encoding='utf-8'))
command = hooks['hooks']['SessionStart'][0]['hooks'][0]['command']
assert '${PLUGIN_ROOT}' in command and (plugin / 'hooks/session-start-note.md').is_file()
claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
assert manifest['version'] == claude['version'], 'versions differ'
skills = plugin / manifest['skills']
assert skills.is_dir()
for skill in skills.iterdir():
    if not skill.is_dir():
        continue
    content = (skill / 'SKILL.md').read_text(encoding='utf-8')
    parts = content.split('---', 2)
    assert len(parts) == 3 and not parts[0].strip(), f'{skill}: missing front matter'
    fields = parts[1].splitlines()
    assert f'name: {skill.name}' in fields, f'{skill}: missing or mismatched name'
    assert any(line.startswith('description: ') for line in fields), f'{skill}: missing description'
print('Codex marketplace, hooks and skills: OK')
