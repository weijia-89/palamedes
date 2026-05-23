# Palamedes browser UI (`ui/`)

Local single-model front end for Palamedes-style research: stakes ladder, output templates, token heuristic, short answer + downloadable report, refinement chips. API keys stay in the browser only.

This is **not** a replacement for the full multi-agent [`prompts/`](../prompts/) workflow or the agent [`skill/`](../skill/); it is the fastest way to run one bounded pass with the same template vocabulary.

## Run

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
- **Templates** aligned with [`skill/SKILL.md`](../skill/SKILL.md) output modes: full report, landscape one-pager, executive brief, study guide site
- Defaults: L2 advisory, empirical, full report; token/cost heuristic on selector change
- **API key** in `localStorage` only; OpenAI-compatible endpoint from the browser
- **Short answer**, **full report** (markdown download), **refinement** follow-ups in `sessionStorage`

## Security

- No server stores keys. Use a dedicated key with low limits.
- Do not commit API keys. `localStorage` is readable by any script on this origin.

## Canon

Full rigor: [`skill/SKILL.md`](../skill/SKILL.md) · multi-agent synthesis: [`prompts/research-synthesis.md`](../prompts/research-synthesis.md)
