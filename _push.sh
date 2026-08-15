#!/bin/bash
# Push static site to GitHub
cd /c/Users/Administrator/galeair-static || exit 1
TOKEN=$(python -c "print(open('/tmp/ghtok').read().strip())")
git remote remove origin 2>/dev/null
git remote add origin https://github.com/myjerry243/gale-force-air.git
AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$TOKEN" | base64 -w 0)"
git -c http.extraheader="$AUTH" push -u origin main 2>&1 | tail -6
echo "PUSH_EXIT=$?"
