#!/usr/bin/env bash
# Merge gate: palamedes skill contract + doc parity (trainer review B-6).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SKILL=skill/SKILL.md
RULE="${HOME}/Projects/.cursor/rules/palamedes.mdc"
VERSION=3.13.0

test -f "$SKILL"
test -f skill/references/rag-eval-literacy.md
test -f skill/references/llm-failure-modes.md
test -f skill/references/legal-evidence-retrieval.md
test -f skill/references/threat-intel-evidence-retrieval.md
test -f skill/references/financial-evidence-retrieval.md
test -f docs/ARCHITECTURE.md
test -f CHANGELOG.md
test -f README.md
test -f context.md

grep -q "version: $VERSION" "$SKILL"
grep -q "version = \"$VERSION\"" pyproject.toml
grep -q 'description: research, investigate, audit, fact-check, lit-review, study guide, incorporate' "$SKILL"
python3 -c "
import pathlib, re
text = pathlib.Path('skill/SKILL.md').read_text(encoding='utf-8')
m = re.search(r'^description:\s*(.+)$', text, re.M)
assert m, 'missing description'
desc = m.group(1).strip()
assert len(desc) <= 80, f'description too long: {len(desc)} chars'
"

test -f skill/references/literature-corpus-fanout.md
test -f skill/references/authoritative-review-literacy.md
test -f skill/references/prompts/literature-paper-ingest.md
grep -q 'Pattern 9' "$SKILL"
grep -q '4.1 deai gates' "$SKILL"
grep -q 'FR-1' "$SKILL"
grep -q 'inferred:first-read-only' "$SKILL"
grep -q 'Constraint pinning' "$SKILL"
grep -q '0.2 Context compaction' "$SKILL"
grep -q '§RAG-judge' skill/references/llm-failure-modes.md
grep -q 'IF M = answer relevancy' skill/references/rag-eval-literacy.md
grep -q 'loading.*rag-eval-literacy' "$SKILL" || grep -q 'load.*rag-eval-literacy' "$SKILL"

if [[ -f "$RULE" ]]; then
  grep -q "v$VERSION" "$RULE"
  grep -qE '\*\*(Canon|Canonical):' "$RULE"
  grep -q 'Do not duplicate' "$RULE"
  if grep -q '## Loop, P1' "$RULE"; then
    exit 1
  fi
fi

grep -q 'DEAI-IN' docs/ARCHITECTURE.md
grep -q 'DEAI-OUT' docs/ARCHITECTURE.md
grep -q "v$VERSION" README.md
grep -q "v$VERSION" docs/ARCHITECTURE.md
grep -q 'Guardrails (budget, stop conditions, rigor floor) are engine state' context.md
grep -q 'finish_empty_nudge' skill/SKILL.md

# Cruft must stay removed
test ! -f study-guide-site.md
test ! -f verify-procedural-guide.sh
test ! -d js
test ! -d css

grep -q 'url=ui/' index.html
test -f ui/index.html
test -f scripts/pedagogy_snippets.py
python3 scripts/pedagogy_snippets.py verify-consumers

echo "verify_palamedes_skill: ok"
