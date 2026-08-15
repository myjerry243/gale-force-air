#!/usr/bin/env python3
"""Enable GitHub Pages for the repo + poll deployment status"""
import json, time, urllib.request

tok = open(r'C:\Users\Administrator\AppData\Local\Temp\ghtok', encoding='utf-8').read().strip()

def api(method, path, body=None):
    req = urllib.request.Request('https://api.github.com' + path, method=method)
    req.add_header('Authorization', 'token ' + tok)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'hermes-deploy')
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

# enable pages
st, res = api('POST', '/repos/myjerry243/gale-force-air/pages', {
    'source': {'branch': 'main', 'path': '/'}
})
print('enable pages:', st, res.get('html_url') if isinstance(res, dict) else res)

# poll build status
for i in range(30):
    time.sleep(6)
    st, res = api('GET', '/repos/myjerry243/gale-force-air/pages')
    if isinstance(res, dict):
        status = res.get('status')
        url = res.get('html_url')
        print(f'poll {i}: status={status} url={url}')
        if status in ('built', 'active'):
            print('PAGES_ACTIVE:', url)
            break
    else:
        print('poll', i, st, res)
