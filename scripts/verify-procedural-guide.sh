#!/usr/bin/env bash
# Merge gate: procedural-guide-site template + skill contract stubs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f skill/references/procedural-guide-site.md
test -f templates/procedural-guide/template.html
test -f templates/procedural-guide/README.md

TEMPLATE=templates/procedural-guide/template.html
for id in start-here shopping bench-setup walkthrough verify safety prevent overview; do
  grep -q "id=\"${id}\"" "$TEMPLATE"
done
grep -q 'id="wf-primary"' "$TEMPLATE"
grep -q 'id="restore-' "$TEMPLATE"

grep -q procedural-guide-site skill/SKILL.md
grep -q 'procedural-guide-site' ui/js/templates.js

PROMPT=ui/prompts/research-system.md
grep -q 'procedural-guide-site' "$PROMPT"
grep -q 'Start here' "$PROMPT"
grep -q 'Bench setup' "$PROMPT"
grep -q 'Shopping workflows' "$PROMPT"
grep -q 'Walkthrough Parts A–K' "$PROMPT"

grep -q '../../skill/references/procedural-guide-site.md' templates/procedural-guide/README.md
grep -q procedural-guide-site skill/references/output-rendering.md
grep -q templates/ AGENTS.md
