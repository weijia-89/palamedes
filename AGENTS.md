# Agents

## Cursor Cloud specific instructions

This repo is primarily **Markdown** (LLM prompts, `skill/`, references) plus a **static browser UI** under `ui/` deployed to [GitHub Pages](https://weijia-89.github.io/palamedes/).

### Repository layout

- `prompts/` — Multi-agent dialectic research synthesis prompts (paste into LLM UIs).
- `skill/` — Agent-loadable skill file (`SKILL.md`) plus supporting reference docs in `skill/references/`.
- `assets/` — Image assets referenced by `README.md`.
- `ui/` — Static research app (HTML + JS, no build step); canonical UI home.
- `scripts/serve-ui.sh` — Local dev server (`http://127.0.0.1:8765/`).
- `scripts/verify-study-guide-ui.sh` — Merge gate for study-guide template + prompt contract stubs.
- `scripts/verify-pages-workflow.sh` — Merge gate for Pages deploy workflow paths and `ui/` artifact layout.
- `.github/workflows/deploy-ui.yml` — Pushes `ui/` to GitHub Pages on `main` when UI paths change.

### Linting (Markdown)

```sh
markdownlint '**/*.md' --ignore node_modules
```

Most warnings will be MD013 (line-length >80) which is expected for long-form prose. Focus on structural issues (MD041, MD022, etc.) rather than line-length.

### UI development workflow

1. Edit files under `ui/` (and prompts/skill when templates change).
2. Run merge gates before opening a PR that touches UI or Pages config:

```sh
./scripts/verify-study-guide-ui.sh
./scripts/verify-pages-workflow.sh
```

3. Optional local smoke: `./scripts/serve-ui.sh`
4. Commit and push; `main` deploys via Actions when path filters match.

There is no `package.json` or application test suite for the static UI. The dialectic prompts and skill are consumed by copy-paste or agent load; the UI calls your OpenAI-compatible endpoint with keys in browser `localStorage` only.
