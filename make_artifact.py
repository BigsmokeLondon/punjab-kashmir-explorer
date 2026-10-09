"""Stage the hosted (claude.ai artifact) copy of the site from dist/.

Usage: python make_artifact.py <output folder>

The artifact host wraps its main page in its own <!doctype>/<head>/<body>, so the
explorer page is written without those wrappers; every other file is copied as is.
Files are staged flat (short paths stay under the Windows path limit), and files.json
maps each published path to its staged file for the publish step.
Only files the pages use are staged; the design report and the original banner stay local.
"""
import json
import re
import shutil
import sys
from pathlib import Path, PurePosixPath

DIST = Path(__file__).parent / 'dist'
FILES = ['styles.css', 'heritage.css', 'book.css', 'data.js', 'core.js', 'app.js',
         'book.html', 'book.js', 'book-core.js', 'passages.js',
         'assets/collection-mark.svg', 'assets/ajk-directory.png', 'assets/rajput-clans.png',
         'assets/history/heritage-panorama-smaller-mosque.png',
         'assets/history/lahore-vazir-khan-1895.jpg', 'assets/history/kashmir-shawl-weavers.jpg',
         'assets/sources/Panjab_Castes_uploaded.txt']


def page_body(html):
    # Drop the document wrappers and the head-only tags the host supplies or ignores.
    html = re.sub(r'<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*', '', html, flags=re.I)
    return re.sub(r'\s*<meta (?:charset|name="(?:viewport|robots|theme-color|description)")[^>]*>|\s*<link rel="icon"[^>]*>', '', html).lstrip()


def main(out):
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    names = [PurePosixPath(f).name for f in FILES]
    assert len(set(names)) == len(names), 'staged names must be unique'
    for published, name in zip(FILES, names):
        shutil.copyfile(DIST / published, out / name)
    page = page_body((DIST / 'index.html').read_text(encoding='utf-8'))
    assert page.startswith('<title>'), 'the title must come first so the host can find it'
    (out / 'index.html').write_text(page, encoding='utf-8', newline='\n')
    # Every relative link and script source in the two pages must be published.
    available = set(FILES) | {'index.html'}
    for html in ('index.html', 'book.html'):
        for ref in re.findall(r'(?:src|href)="(?![a-z]+:)([^"#]+)', (out / html).read_text(encoding='utf-8')):
            assert ref in available, (html, ref)
    (out / 'files.json').write_text(json.dumps(dict(zip(FILES, names)), indent=2) + '\n', encoding='utf-8')
    print(f'Staged the page and {len(FILES)} files in {out}')


if __name__ == '__main__':
    main(sys.argv[1])
