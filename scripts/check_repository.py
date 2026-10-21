"""Check the book structure, local links, figures, references and table files."""
from pathlib import Path
import csv
import html
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check():
    book = json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))
    assert book['chapters'], 'No chapters configured'
    sections = [s for c in book['chapters'] for s in c['sections']]
    paths = [c['path'] for c in book['chapters']] + [s['path'] for s in sections]
    assert len(paths) == len(set(paths)), 'Duplicate chapter or section path'
    for c in book['chapters']:
        assert c['sections'], f'No sections in {c["path"]}'
        assert (ROOT / c['path']).read_text(encoding='utf-8').splitlines()[0] == '# ' + c['title']
        for s in c['sections']:
            text = (ROOT / s['path']).read_text(encoding='utf-8')
            assert text.splitlines()[0] == '# ' + s['title'], s['path']
            assert [line[3:] for line in text.splitlines() if line.startswith('## ')] == s['subheadings'], s['path']
    reftext = (ROOT / book['references']).read_text(encoding='utf-8')
    ids = re.findall(r'<a id="(ref-\d+)"></a>', reftext)
    assert ids == [f'ref-{i}' for i in range(1, 182)], 'Reference numbering'
    links = 0
    linked_images = set()
    for p in ROOT.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        assert text.count('```') % 2 == 0, f'Unclosed code fence in {p}'
        for m in re.finditer(r'!?\[[^\n]*?\]\(([^)]+)\)', text):
            target = m[1]
            url = urlsplit(target)
            if url.scheme or target.startswith('//'):
                continue
            destination = (p.parent / unquote(url.path)).resolve() if url.path else p
            assert destination.is_relative_to(ROOT), f'Link leaves repository: {p}: {target}'
            assert destination.is_file(), f'Broken link: {p}: {target}'
            if m[0].startswith('!'):
                linked_images.add(destination)
            if url.fragment.startswith('ref-'):
                assert f'id="{url.fragment}"' in destination.read_text(encoding='utf-8'), target
            links += 1
    images = sorted(p for p in (ROOT / 'img').iterdir() if p.suffix in {'.png', '.svg'})
    assert set(images) == linked_images, 'Unused or untracked figure'
    for p in images:
        if p.suffix == '.png':
            assert p.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), p
        else:
            root = ET.parse(p).getroot()
            assert root.tag == '{http://www.w3.org/2000/svg}svg', p
            assert root.find('{http://www.w3.org/2000/svg}title') is not None, p
    tables = sorted((ROOT / 'data').glob('table-*.csv'))
    assert len(tables) == 17, 'Expected 17 table files'
    markdown_tables = []
    for c in book['chapters']:
        for path in [c['path']] + [s['path'] for s in c['sections']]:
            text = (ROOT / path).read_text(encoding='utf-8')
            for block in re.findall(r'(?m)(?:^\|.*\|\n)+', text):
                rows = []
                for line in block.strip().splitlines():
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    if all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                        continue
                    cells = [re.sub(r'\[\[(\d+)\]\]\([^)]*\)', r'[\1]', cell) for cell in cells]
                    rows.append([html.unescape(cell.replace('<br>', '\n')) for cell in cells])
                markdown_tables.append(rows)
    assert len(markdown_tables) == 17, 'Expected 17 tables in chapter Markdown'
    for p, markdown_rows in zip(tables, markdown_tables):
        with p.open(encoding='utf-8', newline='') as f:
            rows = list(csv.reader(f))
        assert len(rows) > 1 and len(set(map(len, rows))) == 1, p
        assert rows == markdown_rows, f'CSV differs from chapter table: {p}'
        # HTML entities and Markdown escapes are format differences only.
        label = p.stem.split('-')[-1]
        assert label.isdigit(), p
    for p in ROOT.rglob('*.py'):
        compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    print(f'Passed: {len(book["chapters"])} chapters, {len(sections)} sections, '
          f'{len(images)} figures, {len(tables)} tables, {len(ids)} references, {links} local links.')


if __name__ == '__main__':
    check()
