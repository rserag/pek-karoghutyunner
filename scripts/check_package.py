#!/usr/bin/env python3
"""Check the distributable skill layout using the Python standard library."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('armenia-tax-login', 'armenia-tax-income',
          'armenia-tax-declaration', 'armenia-tax-annual-returns',
          'armenia-tax-turnover-election', 'armenia-tax-balances')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    require(manifest.get('name') == 'armenia-tax-skills', 'Plugin name mismatch')
    require(bool(re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', ''))),
            'Plugin version must use major.minor.patch')
    require(bool(manifest.get('description')), 'Missing plugin description')
    require('MIT License' in (ROOT / 'LICENSE').read_text(encoding='utf-8'), 'Missing MIT license')
    require({p.name for p in (ROOT / 'skills').iterdir()} == set(SKILLS), 'Unexpected skill set')

    for name in SKILLS:
        folder = ROOT / 'skills' / name
        text = (folder / 'SKILL.md').read_text(encoding='utf-8')
        require(text.startswith('---\n') and '\n---\n' in text[4:], f'{name}: missing frontmatter')
        frontmatter = text.split('---', 2)[1]
        fields = dict(line.split(': ', 1) for line in frontmatter.strip().splitlines())
        require(set(fields) == {'name', 'description'}, f'{name}: unexpected frontmatter fields')
        require(fields['name'] == name, f'{name}: name mismatch')
        require(0 < len(fields['description']) <= 1024, f'{name}: invalid description length')
        require('<' not in frontmatter and '>' not in frontmatter, f'{name}: unexpected markup')
        metadata = (folder / 'agents' / 'openai.yaml').read_text(encoding='utf-8')
        interface = {}
        for line in metadata.splitlines():
            match = re.fullmatch(r'  (display_name|short_description|default_prompt): (.+)', line)
            if match:
                interface[match[1]] = json.loads(match[2])
        require(set(interface) == {'display_name', 'short_description', 'default_prompt'},
                f'{name}: incomplete interface metadata')
        require(25 <= len(interface['short_description']) <= 64, f'{name}: short description length')
        require('$' + name in interface['default_prompt'], f'{name}: prompt must invoke the skill')

    def blank(value):
        if isinstance(value, dict):
            return all(blank(item) for item in value.values())
        return value == '' or value == []

    profile = json.loads((ROOT / 'examples' / 'profile.example.json').read_text(encoding='utf-8'))
    require(blank(profile), 'Public profile example must contain only empty values')
    example = json.loads((ROOT / 'examples' / 'income.synthetic.json').read_text(encoding='utf-8'))
    require('SYNTHETIC' in example['basis'], 'Income example must be explicitly synthetic')
    for receipt in example['payments']:
        require(receipt['transaction_ref'].startswith('SYNTHETIC-'), 'Use synthetic transaction IDs')
        if 'rate_source' in receipt:
            require(urlparse(receipt['rate_source']).hostname == 'example.org',
                    'Synthetic fixture must not claim real verified exchange rates')

    annual = json.loads((ROOT / 'examples' / 'annual.synthetic.json').read_text(encoding='utf-8'))
    require('SYNTHETIC' in annual['basis'], 'Annual example must be explicitly synthetic')
    require(annual['taxpayer_tin'].startswith('SYNTHETIC-'), 'Use a synthetic annual taxpayer')
    for quarter in annual['quarters']:
        require(quarter['record_id'].startswith('SYNTHETIC-'), 'Use synthetic quarter IDs')
        for filing in quarter.get('filings', []):
            require(filing['filing_ref'].startswith('SYNTHETIC-'), 'Use synthetic filing IDs')

    for fixture in (example, annual):
        def check_example_urls(value):
            if isinstance(value, dict):
                for child in value.values():
                    check_example_urls(child)
            elif isinstance(value, list):
                for child in value:
                    check_example_urls(child)
            elif isinstance(value, str) and value.startswith(('http://', 'https://')):
                require(urlparse(value).hostname == 'example.org',
                        'Synthetic fixture URLs must use example.org')
        check_example_urls(fixture)

    count = 0
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', '__pycache__', '.venv'} for part in relative.parts):
            continue
        require(not path.is_symlink(), f'Unexpected symlink: {relative}')
        if not path.is_file():
            continue
        require(path.suffix in {'.md', '.py', '.json', '.yaml', '.yml'}
                or relative.as_posix() in {'LICENSE', '.gitignore'},
                f'Unexpected distributable file: {relative}')
        if path.suffix == '.json':
            require(relative.as_posix() in {'plugin.json', 'examples/profile.example.json',
                                          'examples/income.synthetic.json',
                                          'examples/annual.synthetic.json'},
                    f'Unexpected JSON: {relative}; keep personal inputs outside the repo')
            json.loads(path.read_text(encoding='utf-8'))
        if path.suffix == '.md':
            text = path.read_text(encoding='utf-8')
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
                if urlparse(target).scheme or target.startswith('#'):
                    continue
                target = unquote(target.split('#', 1)[0].strip('<>'))
                require((path.parent / target).is_file(), f'{relative}: broken local link {target}')
        count += 1
    print(f'Package valid: {len(SKILLS)} skills, {count} source files. '
          'Review privacy and live workflow evidence separately.')


if __name__ == '__main__':
    try:
        check()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'Package error: {error}', file=sys.stderr)
        sys.exit(1)
