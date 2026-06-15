# Palamedes architecture

Single repo, four user-facing surfaces, one epistemic methodology. Canonical skill body: [`skill/SKILL.md`](../skill/SKILL.md) (**v3.11.0**).

## Surfaces

| Surface | Path | Role |
| --- | --- | --- |
| Multi-agent prompts | [`prompts/`](../prompts/) | Human-driven dialectic: parallel agents → adversarial synthesis |
| Agent skill | [`skill/`](../skill/) | Loadable P1–P4 loop for Cursor / Claude / Windsurf |
| Browser UI | [`ui/`](../ui/) | Single-model front door; keys in browser `localStorage` only |
| Calibration scenarios | [`scenarios/`](../scenarios/) | Frozen regression runs (external agent vs skill) |
| HTML templates | [`templates/`](../templates/) | Offline deliverable skeletons (procedural guide, study site exports) |

**Deploy:** GitHub Pages serves [`ui/`](../ui/) at [weijia-89.github.io/palamedes](https://weijia-89.github.io/palamedes/). Root [`index.html`](../index.html) redirects to `ui/` for local repo-root opens. Local dev: [`scripts/serve-ui.sh`](../scripts/serve-ui.sh).

## Skill loop (P1 → P4)

```
P1 Frame     → stakes L0–L4, pre-register, falsifier
P2 Retrieve  → RETRIEVAL-ORDER log, read-depth, DEAI-IN; Pattern 8 (external artifacts) · Pattern 9 (literature corpus)
P3 Adversarial → steelman, bias scan, llm-failure-modes
P4 Synthesize  → tags, FR-1/FR-2/FR-3, DEAI-OUT, stop conditions
```

**First-read anchoring (§1.1):** Load-bearing `[T*-verified]` claims need support beyond `RETRIEVAL-ORDER[1]`; late contradicting reads must surface before emit.

**Methodological RAG/LLM-eval questions:** Load [`skill/references/rag-eval-literacy.md`](../skill/references/rag-eval-literacy.md) on §TRIGGER only. Eval corpus tiers and CI harness config are **not** Palamedes — see trainer routing below.

## deai integration (input + output)

Palamedes does not reimplement deai; it **gates** at two boundaries. Canonical: [`~/Projects/deai.skill/SKILL.md`](../../deai.skill/SKILL.md).

| Gate | Phase | Trigger | Tooling |
| --- | --- | --- | --- |
| **DEAI-IN** | P2 | Third-party review / roundup prose before citing | `reference/ai-signals.md` scan → KEEP / DISCARD (§5b) |
| **DEAI-IN** | P2 | User paste ≥200 words as hypothesis | `deai-scan.py`; tag `[user-asserted]`; never `[T*-verified]` |
| **DEAI-OUT** | Pre-render | L2+ `REPORT.md` before PDF/HTML | `deai-scan.py` + `deai-check.py` (§5h) |
| **DEAI-OUT** | Pre-send | L2+ chat-only synthesis (no report file) | `deai-check.py` on final message body |

Mid-iteration drafts may skip deai; **ship paths may not**. Self-attested “voice-clean” without scanner output is a stop fail.

Install overlay: `~/.cursor/skills/deai/` via `~/Projects/scripts/onboard/sync-dev-skills.sh` (`deai.skill:deai` in dev-skill-map).

## Trainer layer routing (not Palamedes)

When a session mixes research, automated eval metrics, or release gates, **trainer** assigns primary layer before dispatch:

| Layer | Owner | Doc |
| --- | --- | --- |
| L1 Decision synthesis | palamedes | this repo |
| L2 Trace QA (metrics) | project harness + form-check | repo eval README |
| L3 Structured truth | tests / review-rigor | repo CI |

Spec: [`~/Projects/trainer.skill/references/trainer-epistemic-layers.md`](../../trainer.skill/references/trainer-epistemic-layers.md).

## Dependency graph

```
prompts/research-synthesis.md ──┐
prompts/adversarial-review.md ──┼── shared methodology (evidence tiers, verifier split)
skill/SKILL.md ─────────────────┤
ui/prompts/research-system.md ──┘
        │
        ├── skill/references/*     (load on demand)
        ├── templates/*            (HTML skeletons)
        ├── deai.skill             (DEAI-IN / DEAI-OUT gates)
        └── trainer.skill          (layer routing; eval tiers E-T1/T2/T3)
```

**Sync note:** `palamedes` is on `sync-dev-skills.sh` **SKIP_DIRS**. Canonical SoT is this repo’s `skill/`; mirrors at `~/.cursor/skills/palamedes/` are manual or rule-pointed (`@palamedes` → canonical path).

## Merge gates

| Script | Checks |
| --- | --- |
| [`scripts/verify-study-guide-ui.sh`](../scripts/verify-study-guide-ui.sh) | Study-guide template + UI prompt stubs |
| [`scripts/verify-procedural-guide.sh`](../scripts/verify-procedural-guide.sh) | Procedural-guide template + prompt stubs |
| [`scripts/verify-pages-workflow.sh`](../scripts/verify-pages-workflow.sh) | Pages deploy paths + `ui/` layout |
| [`scripts/verify_palamedes_skill.sh`](../scripts/verify_palamedes_skill.sh) | Skill version parity, required refs, rule stub version |

## What is intentionally out of scope

- Multi-agent orchestration in the browser UI (use prompts + skill).
- Server-side API key storage.
- Eval harness configuration inside the Palamedes skill body (trainer → form-check → repo).
