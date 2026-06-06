#!/usr/bin/env bash
# Merge gate: palamedes skill contract + doc parity (trainer review B-6).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SKILL=skill/SKILL.md
RULE="${HOME}/Projects/.cursor/rules/palamedes.mdc"

test -f "$SKILL"
test -f skill/references/rag-eval-literacy.md
test -f skill/references/llm-failure-modes.md
test -f docs/ARCHITECTURE.md
test -f CHANGELOG.md
test -f README.md

grep -q 'version: 3.8.1' "$SKILL"
grep -q '4.1 deai gates' "$SKILL"
grep -q 'FR-1' "$SKILL"
grep -q 'inferred:first-read-only' "$SKILL"
grep -q '§RAG-judge' skill/references/llm-failure-modes.md
grep -q 'IF M = answer relevancy' skill/references/rag-eval-literacy.md
grep -q 'loading.*rag-eval-literacy' "$SKILL" || grep -q 'load.*rag-eval-literacy' "$SKILL"

if [[ -f "$RULE" ]]; then
  grep -q 'v3.8.1' "$RULE"
  grep -q 'DEAI-IN' "$RULE"
  grep -q 'Iron laws' "$RULE"
fi

grep -q 'DEAI-IN' docs/ARCHITECTURE.md
grep -q 'DEAI-OUT' docs/ARCHITECTURE.md
grep -q 'v3.8.1' README.md

# Cruft must stay removed
test ! -f study-guide-site.md
test ! -f verify-procedural-guide.sh
test ! -d js
test ! -d css

grep -q 'url=ui/' index.html
test -f ui/index.html

echo "verify_palamedes_skill: ok"
