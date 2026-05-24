#!/usr/bin/env bash
# sdk-review F3: keyword checklist so prompt trims cannot pass merge gate silently.
# sdk-review F1: canonical merge gate — orchestrator/playground verify cmd must invoke this script, not bare study-guide greps.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

grep -q study-guide ui/js/templates.js
grep -q study-guide ui/prompts/research-system.md
test -f ui/index.html

PROMPT=ui/prompts/research-system.md
grep -q 'Router page plan' "$PROMPT"
grep -q 'Pedagogy appendix' "$PROMPT"
grep -q 'Inline memory anchors' "$PROMPT"
grep -q 'Appendix B miss-pattern elicitation' "$PROMPT"
grep -q 'Elicitation only' "$PROMPT"
grep -q 'anki/' "$PROMPT"  # sdk-review F2: mandatory deck outline stub in Primary corpus
