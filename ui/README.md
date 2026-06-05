# Palamedes browser UI (`ui/`)

Single-model front end for Palamedes-style research: stakes ladder, output templates, token heuristic, short answer + downloadable report, refinement chips. API keys stay in the browser only.

**Live:** [https://weijia-89.github.io/palamedes/](https://weijia-89.github.io/palamedes/) (deployed from this folder on push to `main`).

This is **not** a replacement for the full multi-agent [`prompts/`](../prompts/) workflow or the agent [`skill/`](../skill/); it is the fastest way to run one bounded pass with the same template vocabulary.

## Run locally

```bash
cd ~/Projects/palamedes
./scripts/serve-ui.sh
```

Open http://127.0.0.1:8765/

Or from the repo root:

```bash
cd ui && python3 -m http.server 8765 --bind 127.0.0.1
```

## Features

- Research **field** (question type) and **stakes** — **L0–L4** (L0 = exploratory; skill may suggest bypass at L0)
- **Templates** aligned with [`skill/SKILL.md`](../skill/SKILL.md) output modes: full report, landscape one-pager, executive brief, [study guide site](../skill/references/study-guide-site.md), [procedural guide site](../skill/references/procedural-guide-site.md)
- Defaults: L2 advisory, empirical, full report; token/cost heuristic on selector change
- **API key** in `localStorage` only; OpenAI-compatible endpoint from the browser
- **Short answer**, **full report** (markdown download), **refinement** follow-ups in `sessionStorage`

## Security

- No server stores keys. Use a dedicated key with low limits.
- Do not commit API keys. `localStorage` is readable by any script on this origin.

## Templates

| Template | Skill reference | Typical use |
|---|---|---|
| Full report | default markdown | Decision memo, claim ledger |
| Landscape one-pager | [`landscape-summary-report.md`](../skill/references/landscape-summary-report.md) | Skim sheet, executive summary |
| Executive brief | — | Recommendation-focused memo |
| Study guide site | [`study-guide-site.md`](../skill/references/study-guide-site.md) | Exam prep, certification cram, weekday cadence |
| Procedural guide site | [`procedural-guide-site.md`](../skill/references/procedural-guide-site.md) | Fix/install walkthrough HTML (offline, remove+reinstall) |

### Example: study guide site

1. Set **Template** → *Study guide site*, **Stakes** → L2 (advisory), **Question type** → synthetic or conceptual.
2. Ask something like: *"Build a 10-weekday ISC2 CC cram program with daily pages, practice mocks, and a pedagogy appendix covering memory palace and spaced repetition."*
3. Download the markdown outline from **Full report**; use it as the corpus spec for a downstream HTML render (see skill reference — not built in this UI).

### Example: procedural guide site

1. Set **Template** → *Procedural guide site*, **Stakes** → L2 (advisory), **Question type** → empirical or investigative.
2. Ask something like: *"Build a shim-first walkthrough for 2015 Forester A/C clutch gap fix with workflow shopping and bench layout."*
3. Download the markdown outline; copy `templates/procedural-guide/template.html` and fill section IDs for the final offline HTML artifact.

## Verify

Merge gates (run from repo root):

```bash
bash scripts/verify-study-guide-ui.sh
bash scripts/verify-procedural-guide.sh
```

Study-guide gate checks template wiring plus load-bearing `research-system.md` section keywords (router, pedagogy, elicitation guards). Procedural gate checks mandatory HTML section IDs and UI prompt stubs. Do not substitute bare `grep study-guide` — that passes if contract bullets are trimmed.

## Canon

Full rigor: [`skill/SKILL.md`](../skill/SKILL.md) · multi-agent synthesis: [`prompts/research-synthesis.md`](../prompts/research-synthesis.md)
