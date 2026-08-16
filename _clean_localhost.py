#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_clean_localhost.py — 清理静态导出中的 localhost 残留"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_ONLINE = 'https://myjerry243.github.io/gale-force-air'
BASE_LOCAL = 'http://localhost/galeair'

def clean(html, path):
    # 1. 完整 localhost URL → 线上绝对 URL
    html = html.replace(BASE_LOCAL + '/', BASE_ONLINE + '/')
    # 2. 无尾斜杠形式
    html = html.replace(BASE_LOCAL, BASE_ONLINE)
    # 3. 残留 'http://localhost' 裸形式 (无路径) → 站点根
    html = re.sub(r'http://localhost(?:/galeair)?(?![\w])', BASE_ONLINE, html)
    # 4. 协议相对 //localhost/galeair/xxx → 线上绝对
    html = html.replace('//localhost/galeair/', BASE_ONLINE + '/')
    # 5. oembed 中 URL 编码的 localhost (%3A%2F%2Flocalhost%2Fgaleair)
    html = html.replace('%3A%2F%2Flocalhost%2Fgaleair%2F', '%3A%2F%2Fmyjerry243.github.io%2Fgale-force-air%2F')
    # 6. xmlrpc / wp-json / wp-comments-post 等后台端点 → 移除或指向线上根
    html = re.sub(r'https://myjerry243\.github\.io/gale-force-air/(xmlrpc\.php\?rsd|wp-json[^"\']*|wp-comments-post\.php[^"\']*|wp-admin[^"\']*)', BASE_ONLINE + '/', html)
    return html

files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
total = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    if 'localhost' not in content and 'xmlrpc' not in content and 'wp-json' not in content:
        continue
    new = clean(content, f)
    if new != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        total += 1

print(f"cleaned {total} files")
