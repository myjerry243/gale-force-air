#!/usr/bin/env python3
"""Re-export, commit and push the static site to GitHub Pages."""
import subprocess, base64, os, sys

os.chdir(r'C:\Users\Administrator\galeair-static')

# 1. re-export
r = subprocess.run([sys.executable, 'export.py'], capture_output=True, text=True)
print(r.stdout[-500:])
if r.returncode != 0:
    print('EXPORT FAILED', r.stderr[-500:])
    sys.exit(1)

# 2. git commit
subprocess.run(['git', 'add', '-A'], capture_output=True)
r = subprocess.run(['git', '-c', 'user.name=myjerry243', '-c', 'user.email=myjerry243@users.noreply.github.com',
                    'commit', '-m', 'Fix wp-includes assets + full static export'], capture_output=True, text=True)
print(r.stdout[-300:], r.stderr[-200:])

# 3. push
tok = open(r'C:\Users\Administrator\AppData\Local\Temp\ghtok', encoding='utf-8').read().strip()
auth = 'Basic ' + base64.b64encode(('x-access-token:' + tok).encode()).decode()
p = subprocess.run(['git', '-c', 'http.extraheader=Authorization: ' + auth, 'push', '-u', 'origin', 'main'],
                   capture_output=True, text=True)
print(p.stdout[-400:], p.stderr[-400:])
print('PUSH_EXIT=', p.returncode)
