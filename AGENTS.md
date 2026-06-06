# Agents

## Cursor Cloud specific instructions

This repo is primarily **Markdown** (LLM prompts, `skill/`, references) plus a **static browser UI** under `ui/` deployed to [GitHub Pages](https://weijia-89.github.io/palamedes/).

### Repository layout

- `prompts/` — Multi-agent dialectic research synthesis prompts (paste into LLM UIs).
- `scenarios/` — Frozen calibration runs (external agent vs skill); see `scenarios/README.md`.
- `skill/` — Agent-loadable skill file (`SKILL.md` v3.8.1) plus supporting reference docs in `skill/references/`.
- `docs/ARCHITECTURE.md` — Surfaces, P1–P4 loop, deai input/output gates, trainer layer routing, dependency graph.
- `templates/` — Offline HTML skeletons (`procedural-guide/`, study-site exports).
- `assets/` — Image assets referenced by `README.md`.
- `ui/` — Static research app (HTML + JS, no build step); canonical UI home.
- `index.html` — Redirect to `ui/` (repo-root convenience; Pages artifact is `ui/` only).
- `scripts/serve-ui.sh` — Local dev server (`http://127.0.0.1:8765/`).
- `scripts/verify-study-guide-ui.sh` — Merge gate for study-guide template + prompt contract stubs.
- `scripts/verify-procedural-guide.sh` — Merge gate for procedural-guide template + prompt contract stubs.
- `scripts/verify-pages-workflow.sh` — Merge gate for Pages deploy workflow paths and `ui/` artifact layout.
- `scripts/verify_palamedes_skill.sh` — Merge gate for skill version parity, deai §4.1, required refs, rule stub.
- `.github/workflows/deploy-ui.yml` — Pushes `ui/` to GitHub Pages on `main` when UI paths change.

### deai (external skill)

Palamedes **gates** at input and output; implementation lives in [`~/Projects/deai.skill/`](../deai.skill/):

- **DEAI-IN (P2):** ai-signals on third-party review prose (skill §5b); optional scan on user paste ≥200w.
- **DEAI-OUT (L2+):** `deai-scan.py` + `deai-check.py` on `REPORT.md` before render (§5h); `deai-check` on chat-only final message.

See `skill/SKILL.md` §4.1 and `docs/ARCHITECTURE.md`.

### Trainer routing (eval / release)

Eval corpus tiers and CI harness config are **not** in Palamedes. When a task mixes research + automated metrics + release gates, load [`~/Projects/trainer.skill/references/trainer-epistemic-layers.md`](../trainer.skill/references/trainer-epistemic-layers.md) and assign primary layer before dispatch.

### Linting (Markdown)

```sh
markdownlint '**/*.md' --ignore node_modules
```

Most warnings will be MD013 (line-length >80) which is expected for long-form prose. Focus on structural issues (MD041, MD022, etc.) rather than line-length.

### UI development workflow

1. Edit files under `ui/` (and prompts/skill when templates change).
2. Run merge gates before opening a PR that touches UI, skill, or Pages config:

```sh
./scripts/verify-study-guide-ui.sh
./scripts/verify-procedural-guide.sh
./scripts/verify-pages-workflow.sh
./scripts/verify_palamedes_skill.sh
```

3. Optional local smoke: `./scripts/serve-ui.sh`
4. Commit and push; `main` deploys via Actions when path filters match.

There is no `package.json` or application test suite for the static UI. The dialectic prompts and skill are consumed by copy-paste or agent load; the UI calls your OpenAI-compatible endpoint with keys in browser `localStorage` only.

### System dependencies (not in-repo)

- **Python 3** — required for `./scripts/serve-ui.sh` and deai scanners when running DEAI-OUT gates.
- **markdownlint-cli** — global npm package (`npm install -g markdownlint-cli`); not vendored in this repo.

### UI smoke without an API key

You can verify the static app without calling an LLM: start `./scripts/serve-ui.sh`, open the UI, change research field / stakes / template, type a question, and confirm the **token/cost estimate** under Setup updates (`aria-live` `#estimate`). Full “Run research” needs a user-supplied OpenAI-compatible base URL, model, and key in the browser.
