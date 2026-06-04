# Palamedes parity run — copy into Cursor (same scope as Manus pilot)

Paste everything below the line into a **new** Cursor chat. Load **@palamedes** and **@review-rigor**. Do not read `manus_draft/` until the palamedes report is written (blind run).

---

```
palamedes v3 engaged · type=comparative · stakes=L2 · budget=read+web-fetch

## Task

Produce a **public-source** company brief for **Datadog, Inc.** (datadoghq.com) for a **Senior QA Engineer** interview candidate.

**Out of scope:** JFS/ILS scores, hire/no-hire, resume/CL, private data, JobSpy, flesh.

## Required sections (match Manus pilot scope)

1. Product and who pays (usage model, buyer personas)
2. Top 5 competitors (one line each + differentiation)
3. Moat thesis with evidence (primary or credible secondary only for numbers)
4. Business model risks (observability tax, hyperscalers, OpenTelemetry, margins)

## Evidence rules (strict)

- **Primary first** for every number: Datadog IR press releases, SEC filings, official shareholder letters — not matrixbcg.com / technologychecker / random Substack for load-bearing metrics.
- **NRR / net revenue retention / NDR:** If not found in primary Datadog IR/SEC after search, write exactly: `NRR: SEARCHED-AND-MISSING (sources tried: [list])`. Do not infer from blogs.
- **FY2025 scale metrics** (if cited): revenue, $1M+ ARR customer count, $100K+ ARR count — quote verbatim from primary or tag `[unknown]`.
- **Q3 2025 multi-product adoption** (2+/4+/8+ products): cite source with `read:body` or mark `[TBD]`.
- No decorative `[1][2]` without a reference table mapping number → URL → quote.
- Max ~900 words in the deliverable body + separate **Claim ledger** table.

## Deliverables (in order)

1. **P1 frame** — one-line question, stakes L2, pre-register prediction + what would change your mind.
2. **Report** — four sections above.
3. **Claim ledger** — columns: ID | Claim | Tag | Conf | Falsifier
4. **Kill list** — anything you refused to emit and why.
5. **REFERENCES** — tier, URL, read-depth (read:body / read:abstract / searched-and-missing).

## Save path (when done)

Write the full output to:

`palamedes/scenarios/manus-vs-palamedes-datadog-2026-06-04/artifacts/cursor_palamedes_YYYY-MM-DD_market.md`

Use today’s date. Do not read other files in `artifacts/` until your run is saved (blind arm).

## After you finish

Tell me: "Palamedes parity run complete — ready to diff against Manus."
```

---

## After both reports exist

In a **third** chat (or same thread after palamedes file exists):

```
Read:
- palamedes/scenarios/manus-vs-palamedes-datadog-2026-06-04/artifacts/manus_same_prompt_2026-06-04.md (or manus_freeform_*)
- palamedes/scenarios/manus-vs-palamedes-datadog-2026-06-04/artifacts/cursor_palamedes_*_market.md

@palamedes @review-rigor

Compare for **interview-crib utility** (not JFS):
1. Which load-bearing claims appear in both vs only one side?
2. Manus-only claims that palamedes killed or downgraded?
3. Palamedes-only value (SEARCHED-AND-MISSING, better cites)?
4. Time/token estimate: was Manus worth it vs palamedes-only path?
5. Verdict: keep Manus in toren 7.8 as (A) always (B) heavy research only (C) never — one letter + 3 bullets.
```
