#!/usr/bin/env python3
"""Convert all image refs to absolute URLs (bulletproof for any browser/cache)."""
import os, re, glob

ROOT = r'C:\Users\Administrator\galeair-static'
BASE = 'https://myjerry243.github.io/gale-force-air/'

pat = re.compile(r'(<img[^>]*?src=")([^"]+)(\")', re.S)
count = 0
for html_file in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    orig = content
    def repl(m):
        global count
        src = m.group(2)
        if src.startswith(('http://', 'https://', 'data:', '#')):
            return m.group(0)
        # resolve relative against the html file's dir, then make absolute
        d = os.path.dirname(html_file)
        resolved = os.path.normpath(os.path.join(d, src)).replace('\\', '/')
        rel = os.path.relpath(ROOT, os.path.dirname(resolved))
        # simpler: rebuild URL path relative to ROOT
        abs_path = os.path.normpath(os.path.join(d, src))
        rel_to_root = os.path.relpath(abs_path, ROOT).replace('\\', '/')
        full = BASE + rel_to_root
        count += 1
        return m.group(1) + full + m.group(3)
    content = pat.sub(repl, content)
    if content != orig:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
print('img refs absolutized:', count)
