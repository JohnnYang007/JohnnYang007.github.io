#!/usr/bin/env python3
"""Update website text in-place, without loading or rerunning the simulation."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY_PATTERN = r'(<script type="application/json" id="sg-copy">).*?(</script>)'
DATA_PATTERN = r'<script type="application/json" id="sg-trajectory">(.*?)</script>'


def update(page: Path, copy_path: Path):
    copy = json.loads(copy_path.read_text(encoding='utf-8'))
    required = ['title', 'page_description', 'model_caption',
                'equation_mathml', 'equation_accessible_text']
    if any(not isinstance(copy.get(key), str) for key in required):
        raise ValueError('Each copy.json field must be present and contain a string.')
    document = page.read_text(encoding='utf-8')
    match = re.search(r'data-srcdoc="([^"]*)"', document)
    inner = html.unescape(match.group(1)) if match else document
    data = re.search(DATA_PATTERN, inner, re.S)
    if not data:
        raise ValueError('No simulation payload found. Use a built PAM page.')
    before = hashlib.sha256(data.group(1).encode()).hexdigest()
    encoded = json.dumps(copy, ensure_ascii=False, allow_nan=False).replace('<', '\\u003c')
    inner, count = re.subn(COPY_PATTERN, lambda m: m.group(1)+encoded+m.group(2), inner, flags=re.S)
    if count != 1:
        raise ValueError('Expected one editable copy block; no page was changed.')
    title = html.escape(copy['title'])
    inner = re.sub(r'<title>.*?</title>', lambda m: '<title>'+title+'</title>', inner, count=1, flags=re.S)
    after = hashlib.sha256(re.search(DATA_PATTERN, inner, re.S).group(1).encode()).hexdigest()
    if before != after:
        raise ValueError('Simulation payload changed unexpectedly; no page was written.')
    if match:
        document = document[:match.start(1)]+html.escape(inner, quote=True)+document[match.end(1):]
        document = re.sub(r'<title>.*?</title>', lambda m: '<title>'+title+'</title>', document, count=1, flags=re.S)
        document = re.sub(r'<meta name="description" content="[^"]*">',
                          lambda m: '<meta name="description" content="'+html.escape(copy['page_description'], quote=True)+'">',
                          document, count=1)
    else:
        document = inner
    temporary = page.with_suffix(page.suffix+'.tmp')
    temporary.write_text(document, encoding='utf-8')
    temporary.replace(page)
    print(f'Updated text: {page.resolve()}')
    print(f'Simulation payload unchanged: {after}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', type=Path, default=HERE.parent/'simulations'/'pam.html')
    parser.add_argument('--copy', type=Path, default=HERE/'copy.json')
    args = parser.parse_args()
    update(args.page, args.copy)
