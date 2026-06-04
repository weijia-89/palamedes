# Case study: Palamedes vs Manus on a public company brief

**Scenario ID:** `manus-vs-palamedes-datadog-2026-06-04`  
**Stakes:** L2 (interview prep; no hire/no-hire)  
**Subject:** Datadog, Inc. (DDOG), Senior QA Engineer crib  
**Artifacts:** [`artifacts/`](./artifacts/) · **Prompt:** [`prompt.md`](./prompt.md)

---

## Summary

We ran the same Palamedes v3 packet twice: once in Cursor with the palamedes skill, once in Manus (Meta-marketed autonomous research agent). A third arm used Manus without that packet (free-form pilot).

Headline financial facts converged across arms when the strict prompt was used. They diverged on what you could defend in a skeptical follow-up: source tier, kill-list honesty, and whether “accurate” marketing copy matched the citations in the body.

**Recommendation for practitioners:** treat external agents as optional first drafts only if a palamedes pass remains mandatory. For L2 public research we tested, palamedes-only in Cursor was the better default.

---

## What we were testing

Manus advertises deep, accurate research, cross-referencing, and optional fact-check labels (TRUE / FALSE / UNVERIFIABLE). Palamedes advertises something different: tier tags, read-depth, claim ledgers, falsifiers, and explicit refusal when primary search fails.

The scenario asks which product delivers **epistemic accuracy** (right claim, right source, honest uncertainty), not which finishes a readable PDF faster.

---

## Arms and results

### 1. Manus free-form (pilot)

Manus produced a polished brief quickly but there was a load-bearing error: **~120% NRR** attributed to a Tomasz Tunguz post that does not state that figure. Competitor narrative leaned on MatrixBCG and similar third-tier pages.

**Failure mode:** citation laundering. Fluent prose + numbered references without quote-level verification.

### 2. Same Palamedes prompt, two runners

| Dimension | Cursor + palamedes | Manus + same prompt |
| --- | --- | --- |
| FY2025 $3.43B, 603 / ~4,310 ARR tiers | T1 IR + quotes | Matched [6] |
| Multi-product % (Q3/Q4) | Call + supplemental, quoted | Q4 supplemental [7] |
| DBNR / NRR ~120% | Q3 call + Q4 supplemental | Supplemental [7] |
| Competitors | FY2025 10-K competition section | Mix of 10-K + vendor PR + **openobserve blog** for hyperscalers |
| Observability-tax risk | 10-K usage/churn language | **oneuptime blog** [8] |
| SBC $750.6M | 10-K | **alphaquery** [10] |
| Ledger discipline | `[T1-verified]` + falsifiers | Generic “Primary” |

Manus **adopted the Palamedes outline** when given the packet. It did not adopt the **tier discipline**. The body still cited blogs for risks while the kill list claimed third-party metric blogs were ignored.

### 3. Cursor palamedes (reference arm)

The Cursor run pulled SEC 10-K, IR press release, Q3 earnings call transcript, and Q4 supplemental. It included a reference table mapping claim → URL → verbatim quote. That is the artifact you would open if an interviewer asked “where did you get 120% retention?”

---

## What this scenario teaches the skill

1. **Format compliance ≠ verification.** External agents can mimic P1 frame, ledger, and kill list without enforcing them against the reference table.

2. **Shared prompt does not imply shared rigor.** Parity on numbers with non-parity on proof is the dangerous middle state: confidence without audit trail.

3. **SEARCHED-AND-MISSING is a feature.** The free-form pilot’s NRR mistake is exactly what tiered search and kill lists are meant to prevent. The strict-prompt arms found DBNR in supplemental/call sources; the lesson is *where* you looked, not whether the metric exists.

4. **Marketing accuracy claims need a operator gate.** Manus FAQ text says to review the final result. This scenario is the concrete review task palamedes automates.

---

## Regression checks for future skill edits

When changing `skill/SKILL.md` or `references/source-grading.md`, re-read this scenario and confirm:

- [ ] A run on [`prompt.md`](./prompt.md) still refuses blog-backed load-bearing metrics unless tagged T3 and not used for numbers.
- [ ] Claim ledger tags cannot be swapped for vague “Primary.”
- [ ] Kill-list entries must match what the report body actually cites.

---

## Operator verdict

| Option | Label | This pilot |
| --- | --- | --- |
| A | Always use Manus before palamedes | Rejected |
| B | Manus for heavy 7.8 only | Rejected (review tax ≈ palamedes-only latency) |
| C | Never wire Manus; palamedes + Cursor only | **Accepted** |

Manus remains archived under `~/Projects/docs/archive/manus_token_dump/` as a token dump, not a pipeline stage.

---

## References (scenario meta)

| Ref | Note |
| --- | --- |
| Artifacts | Frozen outputs in [`artifacts/`](./artifacts/); not re-fetched for this report |
| Manus marketing | [manus.im/compare/manus-vs-claude-code](https://manus.im/compare/manus-vs-claude-code) FAQ “How accurate is Manus?”; [manus.im/playbook/fact-checker](https://manus.im/playbook/fact-checker) |
| Palamedes skill | [`skill/SKILL.md`](../../skill/SKILL.md) stakes L2, citation protocol |

*Report prose edited with DEAI (technical report register; meaning preserved from pilot notes).*
