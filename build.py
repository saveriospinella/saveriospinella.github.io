"""Validate and stage the static site, with no external dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree
import shutil

ROOT = Path(__file__).resolve().parent
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.links, self.ids, self.tags = [], [], set(), []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        if tag == 'img': assert attrs.get('alt'), 'Missing alternative text'
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag, f'Unbalanced closing tag: {tag}'
        self.stack.pop()

for name in ('index.html', 'research.html'):
    source = (ROOT / name).read_text()
    page = Page()
    page.feed(source)
    assert not page.stack, 'Unclosed elements'
    assert sum(tag == 'h1' for tag, attrs in page.tags) == 1
    assert sum(tag == 'main' for tag, attrs in page.tags) == 1
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        if parsed.path:
            assert (ROOT / unquote(parsed.path)).is_file(), f'Missing file: {link}'
        elif parsed.fragment:
            assert parsed.fragment in page.ids, f'Missing anchor: {link}'
    assert 'h64Iin0AAAAJ' in source
    if name == 'research.html':
        assert sum(tag == 'details' for tag, attrs in page.tags) == 4
        assert sum(tag == 'article' for tag, attrs in page.tags) == 7
        assert {'published', 'working', 'in-progress', 'predoctoral'} <= page.ids
        assert source.count('More on onetary Economics') == 1
        assert source.count('The Inequality Multiplier') == 1
        assert 'Conditionally Accepted' not in source
    print(f'{name}: HTML structure, local links, and requested content passed')
ElementTree.parse(ROOT / 'sitemap.xml')
dist = ROOT / 'dist'
dist.mkdir(exist_ok=True)
for name in ('index.html', 'research.html', 'sitemap.xml', 'google21341a37d7343975.html', 'google7e97dcd7bb2ff629.html'):
    shutil.copy2(ROOT / name, dist / name)
for name in ('styles', 'resources', 'scripts'):
    shutil.copytree(ROOT / name, dist / name, dirs_exist_ok=True)
print('Static build ready in dist/')
