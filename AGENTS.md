# Agents

## Cursor Cloud specific instructions

This is a **documentation-only repository** — it contains no runnable application code, no services, no build system, and no automated test suite. The entire repository is Markdown files (LLM prompts, a coding-agent skill, and reference materials).

### Repository layout

- `prompts/` — Multi-agent dialectic research synthesis prompts (paste into LLM UIs).
- `skill/` — Agent-loadable skill file (`SKILL.md`) plus supporting reference docs in `skill/references/`.
- `assets/` — Image assets referenced by `README.md`.

### Linting

The only meaningful automated check is markdown linting:

```sh
markdownlint '**/*.md' --ignore node_modules
```

Most warnings will be MD013 (line-length >80) which is expected for long-form prose. Focus on structural issues (MD041, MD022, etc.) rather than line-length.

### No build / run / test

There is no `package.json`, `Makefile`, `Dockerfile`, or any dependency manifest. There are no services to start, no tests to run, and no application to build. The "product" is consumed by copy-pasting prompts into LLM chat interfaces or loading `skill/SKILL.md` as an agent skill.

### Development workflow

1. Edit Markdown files.
2. Run `markdownlint` to check for structural issues.
3. Commit and push.
