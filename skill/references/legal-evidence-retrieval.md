# Legal evidence retrieval

Load when: statute, case law, regulation, contract, litigation, compliance, or legal-hold questions at L2+.

**Iron law:** Palamedes does not give legal advice. This file is retrieval protocol + tier mapping only.

## Source hierarchy (US-centric; adapt jurisdiction)

| Tier | Source types | T-tag guidance |
|------|--------------|----------------|
| T1 | Statute/regulation (USC, CFR, state code); binding court opinion (reporter cite); agency final rule in Federal Register | `[T1-verified, read:body]` for operative text |
| T2 | Restatements; treatises with pinpoint cites; reputable legal journalism linking primaries | `[T2-verified]`; trace to T1 for load-bearing |
| T3 | Law-firm marketing blogs; anonymous explainers; LLM summaries of cases | `[user-asserted]` or `[priors-only]` max |

## Retrieval protocol

1. **Identify jurisdiction** before search (federal vs state vs EU, etc.). Wrong jurisdiction = fail.
2. **Primary first:** statute section or slip opinion from official source (govinfo, eCFR, court site).
3. **Citator validation (→ FR-1/FR-2):** for case law, check whether later authority distinguishes, overrules, or limits the holding. A single case cite without treatment check is `[inferred:first-read-only]` until second independent source confirms still good law.
4. **Shepardize/KeyCite equivalent:** if no citator tool, second retrieval = later appellate decision or reputable citator summary with primary links.
5. **Quote operative language** verbatim for definitions, elements, standards of review; paraphrase only with `paraphrase:` prefix.

## FR mapping

- **FR-1:** first case/statute opened cannot be sole support for load-bearing legal conclusion — need independent treatment check or second primary.
- **FR-2:** if later authority contradicts first cite, emit Contradiction block before claim.

## Common failure modes

- Headnote / Westlaw synopsis treated as holding (abstract-only at L2+).
- Blog post citing "Court holds X" without reading opinion body.
- Precedent from wrong circuit treated as binding.

## Cross-links

- `source-grading.md` — tier definitions
- `replication-and-validity.md` — not primary for law; use for empirical claims about legal outcomes
