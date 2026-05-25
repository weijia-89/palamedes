#!/usr/bin/env bash
# sdk-review F3: merge gate for GitHub Pages deploy workflow (path triggers + artifact path).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WF=.github/workflows/deploy-ui.yml
test -f "$WF"

grep -q 'ui/\*\*' "$WF"
grep -q 'index.html' "$WF"
grep -q '.nojekyll' "$WF"
grep -q 'deploy-ui.yml' "$WF"

grep -q 'path: ui' "$WF"
grep -q 'include-hidden-files: true' "$WF"

test -f ui/index.html
test -f index.html
test -f .nojekyll

grep -q 'study-guide' ui/js/templates.js
