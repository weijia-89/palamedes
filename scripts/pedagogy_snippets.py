#!/usr/bin/env python3
"""Single source of truth for assessment-prep pedagogy strings (anti-drift).

Consumers (must import, not duplicate):
  - toren/applications/codility-train/scripts/build_study_guide.py
  - toren/applications/openmined/scripts/build_openmined_reference.py

Coach/docs (pointer only): trainer assessment-prep-pedagogy.md, palamedes study-guide-site.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# --- Canonical claims (adversarial-reviewed 2026-06-06) ---

ROWLAND_SHORT = "159 effect sizes from 61 studies"
ROWLAND_CLAIM = f"Recall beats re-read on delayed tests (g ≈ 0.50; {ROWLAND_SHORT})"
RETRIEVAL_BULLET_HTML = (
    "<li><strong>Practice by producing, not consuming.</strong> Retrieval practice is the only "
    "technique with convergent meta-analytic support (g ≈ 0.50; Rowland 2014, "
    f"{ROWLAND_SHORT}; Dunlosky 2013 high-utility). Re-reading and highlighting are confirmed "
    "low-utility.</li>"
)
SPACING_BULLET_HTML = (
    "<li><strong>Split daily study into 2 sessions separated by 4+ hours.</strong> Spacing is "
    f"high-utility (Dunlosky 2013). For 7-day retention, interpolated optimal gap ≈ 3 days "
    "(Cepeda et al. 2008); within a 4-day sprint, maximize within-day spacing.</li>"
)
CEPEDA_GAP = "7-day RI optimal gap ≈ 3 days (interpolated)"
ABORT_RULE = (
    "**Abort rule:** Day 2 cold pattern recall **<30%** → extend foundations before lesson volume."
)
TOP_FIVE = (
    "**Top 5 (adversarial-reviewed):** retrieval practice, distributed spacing, "
    "transfer-appropriate processing (IDE+timer Day 1), subgoal worked examples in foundations "
    "`[T2]`, interleaving after blocked foundations `[moderate; coding transfer inferred]`."
)
DEMOTED = "**Demoted:** expressive writing pre-test (Camerer 2018 replication failure)."
CAVEAT = (
    "**Caveat:** Mocks beat palace when time is scarce; practice form must match test form (TAP). "
    "Detail: study guide pedagogy appendix."
)
HONEST_CAVEATS = (
    "Mocks beat palace when time is scarce; mnemonics are pointers not understanding; "
    "practice form must match test form (timed IDE); palace capacity ~2 items per locus; "
    "sleep beats one more re-read; cross-domain transfer from math/verbal studies is "
    "[inferred] for coding."
)

D5_CAVEATS = [
    "Mocks beat palace",
    "mnemonics are pointers",
    "practice form must match",
    "palace capacity",
    "sleep beats one more re-read",
]

FORBIDDEN_REGEX = [
    r"159 studies",
    r"Tier 1.*[Ii]nterleav",
    r"interleaving.*Tier 1",
    r"expressive writing.*mandatory daily",
    r"\.\./\.\./codility-train/",
]

REQUIRED_IN_EXAM_ARTIFACTS = [
    "Mocks beat palace",
    "practice form",
    "Abort",
    "159 effect sizes",
]

TECHNIQUE_ROWS: list[tuple[str, str, str, str]] = [
    (
        "Retrieval practice",
        ROWLAND_CLAIM,
        "[T1] Rowland 2014; Dunlosky 2013",
        "quick-check + rewrite go-deeper from memory; evening free-recall quiz",
    ),
    (
        "Distributed (spaced) practice",
        f"Two daily sessions 4+ h apart; {CEPEDA_GAP}",
        "[T1] Cepeda et al. 2008; Dunlosky 2013",
        "Morning study, evening retrieve - never mass all 17 patterns in one sitting",
    ),
    (
        "Transfer-appropriate processing",
        "Encoding conditions must match timed IDE retrieval",
        "[T1] Morris et al. 1977",
        "Named codility.com tasks in Codility IDE with timer from Day 1",
    ),
    (
        "Subgoal-labeled worked examples",
        "Labels improve persistence for at-risk novices (N=265; no avg exam gain)",
        "[T2] Margulieux et al. 2020",
        "Numbered subgoal boxes before timed coding",
    ),
    (
        "Worked-example fading",
        "Progressive blanking bridges study → independent solve",
        "[T2] Renkl et al. 2002 (<em>J Experimental Education</em>); Atkinson et al. 2003",
        "Full example → last steps blank → labels only → new problem",
    ),
    (
        "Self-explanation prompts",
        "Guided explanation integrates steps with prior knowledge",
        "[T1.5] Chi et al. 1989; Dunlosky 2013 moderate",
        "After each subgoal: why this line? what breaks if removed?",
    ),
    (
        "Interleaved practice",
        "Mixing patterns builds strategy-selection (d=0.83 math RCT)",
        "[T1.5] Rohrer et al. 2020; Dunlosky 2013 moderate",
        "From Day 3: random lesson draw before each timed task",
    ),
    (
        "Implementation intentions",
        "If-then plans automate behavior (d=0.65 meta-analysis, diverse domains)",
        "[T2] Gollwitzer &amp; Sheeran 2006",
        "3 if-then plans before each session (see D.4)",
    ),
    (
        "SDT motivation design",
        "Autonomy, competence, relatedness sustain effort",
        "[T2] Ryan &amp; Deci 2000",
        "Track pattern-naming score; debrief mocks without shame",
    ),
    (
        "Expertise reversal",
        "Drop scaffolding after gates pass",
        "[T1.5] Kalyuga et al. 2003",
        'Pattern-only cards once <a href="#pedagogy-d5">D.5</a> gates cleared',
    ),
    (
        "Expressive writing",
        "Pre-test worry externalization - original effect failed replication",
        "[Spec] Ramirez &amp; Beilock 2011; Camerer et al. 2018 null",
        "Optional only if you self-report high test anxiety",
    ),
]

CONSUMER_PATHS = [
    REPO / "toren/applications/codility-train/scripts/build_study_guide.py",
    REPO / "toren/applications/openmined/scripts/build_openmined_reference.py",
]

# Strings that must not be duplicated outside this file
DRIFT_MARKERS = [
    ROWLAND_SHORT,
    "159 effect sizes, 61 studies",
    "Top 5 (adversarial-reviewed)",
    "Mocks beat palace when time is scarce",
    "7-day RI optimal gap ≈ 3 days",
]


def logistics_pedagogy_markdown() -> str:
    """Part 0 dual-track pedagogy block for openmined LOGISTICS."""
    return f"""### Evidence-based study loop (dual-track)

| Step | Surface | Time (cram days) |
| --- | --- | --- |
| 1 — Read + retrieve | Study guide `#how-to-study`, `#foundations`, today's chapter | ~45 min |
| 2 — Prime | Lesson PDF + walkthrough videos (index C-day) | ~30 min |
| 3 — Practice (TAP) | Codility IDE, timer on, 100% per task | ~3 h 30 min |
| 4 — Log | Error log: correctness vs performance | ~45 min |
| 5 — Optional SR | Anki complexity patterns | ~60 min |

{TOP_FIVE}

{DEMOTED}

{ABORT_RULE}

{CAVEAT}
"""


def technique_table_rows_html() -> str:
    rows = []
    for technique, claim, tag, action in TECHNIQUE_ROWS:
        rows.append(
            f"        <tr><td>{technique}</td><td>{claim}</td><td>{tag}</td><td>{action}</td></tr>"
        )
    return "\n".join(rows)


def honest_caveats_html() -> str:
    return f'    <p><strong>Honest caveats:</strong> {HONEST_CAVEATS}</p>'


def write_contract_inc(path: Path | None = None) -> None:
    """Regenerate pedagogy_contract.inc.sh from this module."""
    out = path or Path(__file__).resolve().parent / "pedagogy_contract.inc.sh"
    lines = [
        "# AUTO-GENERATED from pedagogy_snippets.py — do not edit by hand",
        "PEDAGOGY_FORBIDDEN=(",
    ]
    for pat in FORBIDDEN_REGEX:
        lines.append(f"  '{pat}'")
    lines.append(")")
    lines.append("PEDAGOGY_D5_REQUIRED=(")
    for req in ["Mocks beat palace", "practice form", "Abort"]:
        lines.append(f"  '{req}'")
    lines.append(")")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def check_forbidden(text: str, label: str) -> list[str]:
    errors = []
    for pat in FORBIDDEN_REGEX:
        if re.search(pat, text):
            errors.append(f"FORBIDDEN /{pat}/ in {label}")
    return errors


def check_required(text: str, label: str) -> list[str]:
    errors = []
    for needle in REQUIRED_IN_EXAM_ARTIFACTS:
        if needle not in text:
            errors.append(f"MISSING {needle!r} in {label}")
    return errors


def verify_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    label = str(path)
    return check_forbidden(text, label) + check_required(text, label)


def verify_consumers() -> list[str]:
    """Fail if build scripts duplicate canonical strings instead of importing.

    Missing consumer paths are deferred (not errors) until toren application
    build scripts exist on disk.
    """
    errors: list[str] = []
    present: list[Path] = []
    for path in CONSUMER_PATHS:
        if path.is_file():
            present.append(path)
    if not present:
        print(
            "pedagogy_snippets: no consumer build scripts on disk — verify-consumers deferred",
            file=sys.stderr,
        )
        return errors
    for marker in DRIFT_MARKERS:
        for path in present:
            body = path.read_text(encoding="utf-8")
            if "pedagogy_snippets" not in body:
                errors.append(f"{path.name} must import pedagogy_snippets")
            if body.count(marker) > 0:
                errors.append(f"drift: {marker!r} duplicated in {path.name} (use import)")
    return errors


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: pedagogy_snippets.py sync-inc | verify-consumers | verify-file <path>"
        )
    cmd = sys.argv[1]
    if cmd == "sync-inc":
        write_contract_inc()
        print("wrote pedagogy_contract.inc.sh")
    elif cmd == "verify-consumers":
        errs = verify_consumers()
        if errs:
            for e in errs:
                print(e, file=sys.stderr)
            raise SystemExit(1)
        print("pedagogy_snippets: consumers ok")
    elif cmd == "verify-file":
        if len(sys.argv) < 3:
            raise SystemExit("verify-file requires path")
        errs = verify_file(Path(sys.argv[2]))
        if errs:
            for e in errs:
                print(e, file=sys.stderr)
            raise SystemExit(1)
        print(f"pedagogy_snippets: {sys.argv[2]} ok")
    else:
        raise SystemExit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
