#!/usr/bin/env python3
"""Push static site to GitHub using token from /tmp/ghtok"""
import subprocess, base64, os

os.chdir(r'C:\Users\Administrator\galeair-static')
tok = open(r'C:\Users\Administrator\AppData\Local\Temp\ghtok', encoding='utf-8').read().strip()
auth = 'Basic ' + base64.b64encode(('x-access-token:' + tok).encode()).decode()

# ensure remote
subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
r = subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/myjerry243/gale-force-air.git'], capture_output=True)
print('remote add:', r.returncode)

p = subprocess.run(
    ['git', '-c', 'http.extraheader=Authorization: ' + auth, 'push', '-u', 'origin', 'main'],
    capture_output=True, text=True)
print(p.stdout[-800:])
print(p.stderr[-800:])
print('PUSH_EXIT=', p.returncode)
