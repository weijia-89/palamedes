#!/usr/bin/env bash
# Mechanical gates for study-guide-site.md deliverables (doc §Workflow step 8).
# Usage:
#   verify_study_guide_site.sh codility-train <dir>
#   verify_study_guide_site.sh openmined <dir>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

MODE="${1:-}"
ROOT="${2:-}"

usage() {
  echo "usage: $0 codility-train|openmined <project-dir>" >&2
  exit 2
}

[[ -n "$MODE" && -n "$ROOT" ]] || usage
[[ -d "$ROOT" ]] || { echo "not a directory: $ROOT" >&2; exit 1; }

python3 "$SCRIPT_DIR/pedagogy_snippets.py" sync-inc
python3 "$SCRIPT_DIR/pedagogy_snippets.py" verify-consumers
# shellcheck source=pedagogy_contract.inc.sh
source "$SCRIPT_DIR/pedagogy_contract.inc.sh"

check_forbidden() {
  local file="$1"
  local pat
  for pat in "${PEDAGOGY_FORBIDDEN[@]}"; do
    if grep -qE "$pat" "$file" 2>/dev/null; then
      echo "FORBIDDEN '$pat' in $file" >&2
      exit 1
    fi
  done
}

check_required() {
  local file="$1"
  local needle
  for needle in "${PEDAGOGY_D5_REQUIRED[@]}"; do
    if ! grep -qF "$needle" "$file"; then
      echo "MISSING required pedagogy substring '$needle' in $file" >&2
      exit 1
    fi
  done
}

verify_codility_train() {
  local html="$ROOT/codility_train_study_guide.html"
  [[ -f "$html" ]] || { echo "missing $html" >&2; exit 1; }

  check_forbidden "$html"

  grep -q 'id="overview"' "$html" || { echo "missing #overview" >&2; exit 1; }
  grep -q 'id="exam-contract"' "$html" || { echo "missing #exam-contract" >&2; exit 1; }
  grep -q 'id="pedagogy"' "$html" || { echo "missing #pedagogy" >&2; exit 1; }
  grep -q 'id="how-to-study"' "$html" || { echo "missing #how-to-study" >&2; exit 1; }

  # Overview must not host Big-O table (belongs in exam-contract)
  python3 - "$html" <<'PY'
import re, sys
html = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'id="overview"[^>]*>(.*?)<section', html, re.S)
if not m:
    sys.exit("cannot parse overview section")
body = m.group(1)
if "patterns-table" in body or ("Big-O" in body and "n limit" in body):
    sys.exit("overview contains exam-contract content (table/Big-O)")
PY

  grep -q '159 effect sizes' "$html" || { echo "Rowland wording missing in pedagogy table" >&2; exit 1; }
  grep -q 'Abort rule' "$html" || { echo "missing abort rule" >&2; exit 1; }
  grep -q 'Transfer-appropriate processing' "$html" || { echo "missing TAP in trainer/pedagogy" >&2; exit 1; }
  if grep -q 'assessment-prep-pedagogy.md' "$html" && ! grep -q '#pedagogy' "$html"; then
    echo "bare assessment-prep-pedagogy.md reference without #pedagogy link" >&2
    exit 1
  fi

  if grep -q $'\u2014' "$html" 2>/dev/null || grep -q '—' "$html"; then
    echo "em-dash found in $html" >&2
    exit 1
  fi

  echo "verify_study_guide_site: codility-train ok ($html)"
}

verify_openmined() {
  local md="$ROOT/openmined_full_reference.md"
  local html="$ROOT/openmined_full_reference.html"
  local index="$ROOT/openmined_codility_index.html"
  [[ -f "$md" ]] || { echo "missing $md" >&2; exit 1; }
  [[ -f "$html" ]] || { echo "missing $html" >&2; exit 1; }
  [[ -f "$index" ]] || { echo "missing $index" >&2; exit 1; }

  for f in "$md" "$html" "$index"; do
    check_forbidden "$f"
  done

  grep -q 'codility_train_study_guide' "$md" || { echo "study guide link missing in monolith md" >&2; exit 1; }
  grep -qF '../codility-train/codility_train_study_guide.html' "$md" || {
    echo "expected ../codility-train/ link in Part 0 md" >&2
    exit 1
  }
  if grep -qF '../../codility-train/' "$md"; then
    echo "broken ../../codility-train/ still in monolith md" >&2
    exit 1
  fi

  check_required "$md"
  grep -q 'Dual-track' "$md" || { echo "dual-track section missing" >&2; exit 1; }

  echo "verify_study_guide_site: openmined ok"
}

case "$MODE" in
  codility-train) verify_codility_train ;;
  openmined) verify_openmined ;;
  *) usage ;;
esac
