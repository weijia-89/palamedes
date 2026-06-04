# Scenario: Manus vs palamedes (Datadog, 2026-06-04)

**Type:** comparative · **Stakes:** L2 · **Domain:** public IR/SEC company brief (interview crib, not hire/no-hire)

## Question under test

When a commercial autonomous research agent (Manus) and Cursor running `@palamedes` receive the **same** evidence rules, do they produce the same **defensibility**, or only the same **headline numbers**?

## Arms

| Arm | File | Notes |
| --- | --- | --- |
| Cursor + palamedes (blind) | [`artifacts/cursor_palamedes_2026-06-04_market.md`](./artifacts/cursor_palamedes_2026-06-04_market.md) | 10-K, IR PR, Q3 call, Q4 supplemental; quote table |
| Manus + same Palamedes prompt | [`artifacts/manus_same_prompt_2026-06-04.md`](./artifacts/manus_same_prompt_2026-06-04.md) | Palamedes-shaped sections; mixed tier on risks |
| Manus free-form (pilot) | [`artifacts/manus_freeform_2026-06-04_market.md`](./artifacts/manus_freeform_2026-06-04_market.md) | MatrixBCG/Tunguz stack; bad NRR attribution |
| Palamedes review of free-form | [`artifacts/palamedes_review_manus_freeform_2026-06-04.md`](./artifacts/palamedes_review_manus_freeform_2026-06-04.md) | Adversarial pass on pilot Manus only |

## Prompt to reproduce

[`prompt.md`](./prompt.md) — paste into Cursor with `@palamedes` `@review-rigor`. Save new runs beside artifacts with a dated filename.

## Pass criteria (skill regression)

- Load-bearing metrics trace to **T1** with `read:body` or explicit `searched-and-missing`.
- Risk prose for L2 does not lean on vendor blogs for claims presented as filing-grounded.
- Claim ledger tags match reference table (no generic “Primary” without tier).
- Kill list matches body (no “ignored MatrixBCG” while citing openobserve in risks).

## Outcome (frozen)

**Verdict (C):** do not wire Manus into application research pipelines. Palamedes-only path is sufficient; external agent optional at best for async draft if a mandatory palamedes gate remains.

Full write-up: [`report.md`](./report.md) (DEAI-edited case study).

## Provenance

Pilot run under `~/Projects/docs/archive/manus_token_dump/` (archived 2026-06-04). This scenario is the canonical copy for the palamedes repo.
