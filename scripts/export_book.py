"""Generate a continuous Markdown edition from the ordered chapter files."""
from pathlib import Path
import argparse
import json
import posixpath
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def export():
    book = json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))
    result = ['# ' + book['title']]
    for chapter in book['chapters']:
        files = [(chapter['path'], 1)] + [(s['path'], 2) for s in chapter['sections']]
        for path, shift in files:
            text = (ROOT / path).read_text(encoding='utf-8')
            listing = {f"- [{s['title']}]({Path(s['path']).name})" for s in chapter['sections']}
            lines = [line for line in text.splitlines()
                     if not line.startswith(('[本章目录]', '[全书目录]'))
                     and line not in listing]
            text = '\n'.join(lines)
            text = re.sub(r'^(#{1,4}) ', lambda m: '#' * (len(m[1]) + shift) + ' ', text, flags=re.M)

            def relocate(match):
                target = match[2]
                if urlsplit(target).scheme or target.startswith('#'):
                    return match[0]
                normalized = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
                if normalized.startswith('chapter_references/index.md#'):
                    normalized = '#' + normalized.split('#', 1)[1]
                return f'{match[1]}({normalized})'

            text = re.sub(r'(!?\[[^\n]*?\])\(([^)]+)\)', relocate, text)
            result.append(text.strip())
    refs = (ROOT / book['references']).read_text(encoding='utf-8')
    refs = '\n'.join(line for line in refs.splitlines() if not line.startswith('[全书目录]'))
    refs = re.sub(r'^# ', '## ', refs, flags=re.M)
    result.append(refs.strip())
    return '\n\n'.join(result).rstrip() + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check that book.md is current.')
    args = parser.parse_args()
    generated = export()
    destination = ROOT / 'book.md'
    if args.check:
        if not destination.exists() or destination.read_text(encoding='utf-8') != generated:
            raise SystemExit('book.md is outdated. Run python scripts/export_book.py')
        print('book.md is current.')
    else:
        destination.write_text(generated, encoding='utf-8')
        print('Generated book.md')
