# Financial evidence retrieval

Load when: SEC filings, earnings, audit evidence, accounting standards, or investment-material claims at L2+.

**Iron law:** Palamedes does not give investment advice. Retrieval protocol + tier mapping only.

## PCAOB AS 1105 hierarchy (audit evidence) [inferred T-tag mapping]

Auditor evidence quality ladder — use to grade *support* for financial assertions, not as substitute for reading filings:

| AS 1105 concept | Palamedes handling |
|-----------------|-------------------|
| Auditor's direct knowledge / observation | `[T1-verified]` when sourced to filing or audit report section read |
| External confirmation | `[T1-verified]` after confirmation doc retrieved |
| Documentary (internal/external) | `[T1-verified, read:body]` for line items; abstract/summary insufficient L2+ |
| Analytical procedures | `[T2-verified]` or `[inferred:basis]` — state procedure |
| Inquiries of client | `[user-asserted]` unless third-party corroboration |

## Source hierarchy

| Tier | Source types |
|------|--------------|
| T1 | 10-K/10-Q/8-K on EDGAR; PCAOB standards; FASB ASC citation with section; official exchange filing |
| T2 | Named-journalist FT/WSJ with filing links; Big-4 methodology guides citing ASC/PCAOB |
| T3 | Stocktwits; anonymous "DD"; unsourced DCF screenshots |

## Retrieval protocol

1. **Filing type match:** material event → 8-K; annual metrics → 10-K segment; quarterly → 10-Q.
2. **Read the table/note**, not the earnings press release alone, for numbers at L2+ (abstract-only iron law applies).
3. **Period alignment:** FY vs calendar vs adjusted EBITDA — mismatched periods = `[unknown]` until reconciled.
4. **Management vs auditor:** MD&A is `[T1-verified, read:body]` for *what management said*; audit opinion is separate T1 for *auditor conclusion*.
5. L3+: second independent retrieval (prior filing comparison, peer filing, or regulator action).

## FR mapping

- First press-release number without 10-K/10-Q body → `[priors-only]` at L2+ (FR-1 analog).
- Restatement or subsequent 8-K contradicting earlier claim → FR-2.

## Cross-links

- `source-grading.md`
- `replication-and-validity.md` — for empirical market studies, not GAAP line items
