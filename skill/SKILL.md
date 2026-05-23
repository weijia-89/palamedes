---
name: palamedes
version: 3.5.0
description: Rigorous research / analysis / fact-check / literature-review / synthesis loop for empirical, conceptual, predictive, normative, investigative, comparative, methodological, synthetic questions. Tier-graded sources, zero-fabrication citations, replication-aware, LLM-as-instrument calibrated, multi-pass, dialectic. Triggers research, investigate, analyze, validate, compare, deep-dive, second-opinion, audit, fact-check, literature-review, lit-review, study guide, exam prep, flashcards from sources, anki from sources, build curriculum, summarize papers, extract from documentation, synthesize external sources. Output modes include long-form PDF (see `references/output-rendering.md`), landscape summary one-pager (see `references/landscape-summary-report.md`), and multi-page browseable study-guide site with pedagogy appendix (see `references/study-guide-site.md`). Triggers for the one-pager include "landscape summary report", "landscape summary", "one-pager", "high-level summary", "executive summary", "decision card", "skim sheet", "at-a-glance reference", "cheat sheet", "TL;DR PDF", "quick reference card", "fridge magnet". Triggers for the study-guide site include "build me a study guide", "exam prep program", "cram program", "certification site", "curriculum site", "weekday cadence", "study program for N days", "memory palace for [exam]", "pedagogy appendix", "spaced repetition program". Mergesplit trigger: "incorporate" → run loop on incoming paste, then merge.
---

# palamedes

Loop is process. Output is product. Both are auditable artifacts. Reasoning may be quiet but must be **written somewhere** the user can inspect (in-message tags, scratch file, or report). Silent ≠ undocumented.

## Definitions (referenced throughout)

- **Load-bearing claim** = a claim such that, if removed or flipped, the report's conclusion or recommendation changes. Non-load-bearing claims are flavor / context / hedging and do not require citation discipline.
- **Decision-changing** = a confidence shift or claim change that would route the user to a different action.
- **Stakes ladder L0–L4** = severity of acting on the output. See §0.
- **Read-depth** = how thoroughly a source was consulted: `read:full` (cover-to-cover or relevant chapter end-to-end) > `read:body` (relevant section / methods + results read) > `read:abstract` (abstract + skim). `read:title` (metadata only) is **not a valid depth for a verified tag**; it implies `[priors-only, title-checked]` and the claim must be tagged `[priors-only]`.
- **Independent retrieval** = different source, different query, OR different tool. Two passes of the same query against the same source ≠ independent.
- **Mode collapse** = N passes converge because they share priors / context / source-set, not because of independent confirmation.

## 0. Invocation preamble (1 line, mandatory at session start)

First output line of any session that triggers this skill:

```
palamedes v3 engaged · type=<empirical|conceptual|predictive|normative|investigative|comparative|methodological|synthetic> · stakes=<L0|L1|L2|L3|L4> · budget=<tools-allowed>
```

Forces commitment to type + stakes routing. The user (and you) can audit the routing. Skip preamble = skill not invoked.

### Stakes-recognition heuristic (independent of user framing)

The user may understate stakes. The skill must auto-classify:

| Stakes | Triggers (any) |
|---|---|
| L4, irreversible | Health / dosage / contraindication. Legal advice with statute-of-limitations or filing-deadline implication. Financial advice on positions >% of net worth. Security: incident response, key rotation, prod migration. Code change with `delete`, `drop`, `migrate`, `rotate`, `revoke`, `production`. |
| L3, decision-driving | Hiring / firing. Architecture choice. Vendor / library lock-in. Policy / procedure change. Public statement. |
| L2, advisory | Memo / recommendation under review. Personal-stakes choice (job offer, lease, etc.). Strategy debate. |
| L1, informational | "What is X?" / "How does Y work?" with no immediate decision. |
| L0, idle | Curiosity, brainstorm, vibes. Skip the loop, offer bypass. |

When user framing and auto-classification disagree, **use higher**. Disclose: "User framed as L1; classified L3 due to [trigger]. Applying L3 floor."

### When NOT to invoke this skill (refusal conditions)

- L0 idle / brainstorm, offer bypass: "Loop suppresses generativity; reply unstructured?"
- One-line factual recall the user can verify in 5 seconds, answer directly with `[priors-only]` tag.
- Question fits a more specific skill: `review-rigor` (code review), `epistemic-planning` (multi-step plan), `vibe-check` (AI-PR detection), `systematic-debugging` (bug investigation). Defer.
- Pure creative / generative task (story, brainstorm, naming). Loop deforms generativity.
- User explicitly asks for vibes / quick / no-rigor mode.

## 0.1 Question-type routing

| Type | Example | Rigor anchor |
|---|---|---|
| Empirical | "does X cause Y?" / "is X effective?" | `references/replication-and-validity.md` + `references/causal-inference.md` |
| Conceptual | "what does X mean?" / "is X a Y?" | `references/source-grading.md` + define-then-test |
| Predictive | "what will X do?" / "how likely?" | `references/confidence-calibration.md` + reference-class |
| Normative | "should we X?" | values disclosed + alternatives + cost asymmetry |
| Investigative | "why did X happen?" | flow-of-evidence + counterfactuals (`review-rigor` flow-map) |
| Comparative | "X vs. Y" | criteria pre-stated + symmetric scrutiny + `references/bias-catalog.md` (selective skepticism) |
| Methodological | "how should I research X?" | this skill, recursively, on the meta-question |
| Synthetic | "summarize the literature on X" | `references/replication-and-validity.md` + structured-search + per-paper effect-size |

If type unclear → ask once, then commit. Type drives stop conditions.

### False-premise guard

If the question contains a load-bearing premise the skill cannot verify ("why does X cause Y?" when X→Y itself is uncertain): **surface the premise**, classify it (typically Empirical), run loop on premise *first*. Do not answer the surface question with a tacit premise.

## 1. Loop, P1 → P2 → P3 → P4

### P1, Frame
- Restate question in one line. Note ambiguity.
- **Pre-register** before retrieval: predicted answer, confidence (0–1 or low/med/high), one sentence of "what would change my mind." Even one line counts. (Hides post-hoc rationalization; cf. Silberzahn 2018 many-analyst study.)
- **Reference class:** what category of question; what is the prior base rate of "true" or "yes" answers in this class.
- **Stakes ladder:** L0 idle / L1 informational / L2 advisory / L3 decision-driving / L4 irreversible (legal, financial, health, migration, security). Sets rigor floor, see `references/output-schemas.md`.
- **Type-III check:** is the asked question the *right* question, or is the user pattern-matching to a question framing that loses the actual decision?
- **Human-elicitation pass:** before P2 retrieve, identify load-bearing premises where the human is the most authoritative verifier (their codebase, their values, their context, their constraints, their access to non-public state, their prior decisions). For each such premise, ASK before proceeding. The `review-rigor` 10%-decision-shift threshold does NOT apply here; when human knowledge IS the verifier, asking is not permission-fishing, it is retrieval. Intrinsic self-critique without external grounding empirically degrades reasoning ([HUANG-SELFCORRECT-2023]; [STECHLY-SELFVERIF-2024]). Default to asking when uncertain whether load-bearing context is answerable from public sources alone.

### P2, Retrieve
- Tool budget stated: read > grep > web-fetch > LLM-priors (each ≈10× cost AND 10× lower hallucination risk than the next, in that order).
- For named files / functions / APIs / quotes / numbers: **read the body**. Do not summarize from name (cf. `review-rigor` S1).
- **Read-depth tagging (mandatory).** Annotate each verified cite with depth: `read:full` / `read:body` / `read:abstract` / `read:title`. **Iron-law floor (Anti-Pattern #4): `read:body` is the minimum for any magnitude / scope / caveat / mechanism / methodology claim at L2 or higher.** `read:abstract` is sufficient ONLY for (a) direction-of-effect at L1, (b) existence-of-method, (c) flagging a paper to body-read later. Quoting a speedup, %-gain, accuracy delta, or sample-size from an abstract for a recommendation is forbidden at L2+, even if the abstract was retrieved from a top-tier venue. Abstract-only magnitude citation downgrades the tag to `[priors-only]`. See Anti-Pattern #4 in §8 for the 2026-05-16 self-violation precedent (Chain-of-Draft accuracy inversion revealed only by body-read).
- For LLM-source claims (no retrieval): tag `[priors-only]`. One retrieval ≠ verified; **independent replication** (different source, different query, OR different tool) required before `[T1-verified]` at L3+.
- Every cite resolves to a row in `REFERENCES.md` with tier + URL/DOI + access date + read-depth. New cite → add row, then cite. No URL = no cite.
- Quotes verbatim or prefixed `paraphrase:`. No "approximately" quotes.
- **User-provided evidence** (paste, screenshot, PDF excerpt) is `[user-asserted]`, not `[T*-verified]`, until independently retrieved. User-provided content can be edited / selectively excerpted / fabricated upstream.

### P3, Adversarial
- **Steelman opposite** ≥1 paragraph: name the position, name an adherent if any, give its strongest case (not a strawman). **Steelman must produce different evidence requirements**, if it asks for the same evidence as the original, it is not a real opposite, it's rephrasing.
- **Falsifier per load-bearing claim:** "what evidence would flip this?" Operational form: "if I observed [specific finding], confidence would drop from X to Y." If no answer → drop or tag `[unfalsifiable]`.
- **Quine–Duhem check:** which auxiliary assumptions are also under test? Single-hypothesis falsification is rarely possible.
- **Bias scan:** name ≥1 plausible bias per major claim. Pull from `references/bias-catalog.md` (cognitive + research-design + LLM-instrument).
- **Empirical claims only, replication / validity scan:** effect size + CI, sample scope, preregistration, funder COI, multiple-comparisons, p-hacking susceptibility. See `references/replication-and-validity.md`.
- **LLM-as-instrument scan:** sycophancy, lost-in-the-middle, anchoring, domain hallucination rate, fabricated-cite check. See `references/llm-failure-modes.md`. Required every session.
- **L3+ only, adversarial collaboration:** invoke debate pattern (`references/agentic-research.md` Pattern 2: Prosecutor / Defender / Judge with independent retrieval per role). L4 → worktree fan-out (Pattern 1).
- **Mode-collapse detection:** if N passes agreed, list the retrieved sources each pass used. If overlap > 50%, agreement is not independent confirmation; downgrade aggregate confidence.

### P4, Synthesize
- Tag every load-bearing claim (Tags below).
- Confidence per claim, not per report. Cite per claim, not per section.
- **Calibration step:** which claims, if wrong, would I most expect to be wrong? Lower their confidence. (Tetlock-style.)
- **Many-analyst caveat:** if no second analyst / agent / pass, disclose "single-analyst conclusion underestimates uncertainty" when stakes ≥ L3.
- Output assembled per `references/output-schemas.md`, shaped to host (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`).

### Stop, all of:
1. Every load-bearing claim has tier-≥T2 cite OR `[unknown]` OR `[priors-only]` (latter only allowed below L3).
2. Every load-bearing claim has falsifier OR `[unfalsifiable]`.
3. ≥1 LLM-as-instrument check this session.
4. Stakes-rigor floor met:
   - L1: T2 cite for load-bearing.
   - L2: T2 cite + `read:body` for magnitude claims.
   - L3: ≥2 independent retrievals per load-bearing claim, debate pattern run.
   - L4: worktree fan-out + many-analyst caveat disclosed.
5. Marginal info-gain from next pass < cost. Operational halt: last pass changed **0 confidences AND added 0 cites AND surfaced 0 new sources**. Two of three is not halt-worthy.

**Convergence between passes is not truth.** Mode collapse, sycophancy, and shared-prior collusion produce false convergence. Truth-signal = independent retrieval agreeing, not LLM passes agreeing.

## 2. Tags, graded, not binary

| Tag | Means |
|---|---|
| `[T1-verified, read:<depth>]` | Primary source (peer-reviewed paper, standards body, RCT data, official spec, primary statute) read this session at named depth; URL/DOI in `REFERENCES.md`. |
| `[T2-verified, read:<depth>]` | Credible secondary read this session at named depth. |
| `[T3-cited]` | Tertiary / forum / unverified blog / single tweet. Use only with explicit downgrade note. |
| `[user-asserted]` | User-provided evidence (paste, screenshot, PDF excerpt) not independently retrieved. Treat as a hypothesis, not confirmation. |
| `[inferred:<basis>]` | Logical/statistical inference from cited evidence. Basis named (e.g. `inferred:T1+priors`). |
| `[priors-only]` | No retrieval; from training distribution. Stale by default. Forbidden ≥ L3. |
| `[speculative]` | Generative; bounded by named priors. |
| `[unknown]` | Cannot determine within budget. |
| `[unfalsifiable]` | No test would flip. Treat as definitional or drop. |
| `[contested]` | Credentialed disagreement; aggregation rule below. |
| `[stale:<date>]` | Verified but source older than relevance window (default 24mo for AI tooling, 12mo for AI safety / model behavior, 30d for active threat-intel, 5y for security architecture, evergreen for math, varies). |

Numeric confidence (`p ≈ 0.7 ± 0.1`) only when decision-changing or quantitative claim. Otherwise tag suffices.

### `[contested]` aggregation rule

For a contested claim, output schema:

```
Claim: <statement> [contested]
  Position A: <statement> · adherents: <names> · evidence: <T-tagged cites> · strongest case: <1 line>
  Position B: <statement> · adherents: <names> · evidence: <T-tagged cites> · strongest case: <1 line>
  Your weighting: A ~0.6 / B ~0.4. Rationale: <1 line>.
  Decision-rule for user: <when each side's call is correct>.
```

Never collapse `[contested]` to a single point answer at L3+ stakes. If the user demands one, disclose the collapse explicitly.

## 3. Citation protocol, zero fabrication

1. **No URL = no cite.** Never invent. If you cannot retrieve, say so and downgrade tag.
2. Every cite resolves to a tier in `REFERENCES.md`. New cite → add row first, then use tag.
3. **Quotes verbatim** with file:line or URL+anchor. Approximate quotes prefixed `paraphrase:` and visibly different.
4. **Suspect-fabrication self-check:** plausible-sounding author+year+title combos that you did not retrieve are the canonical LLM failure (Walters & Wilder 2023; Athaluri 2023). Flag, don't emit.
5. **Citation laundering** check: if claim is "studies show," name the studies. If you can't, say "claim widely repeated; primary source not located."
6. **Numbers cite source.** Every count, percentage, threshold, date, file:line or URL. No memory-quoted constants. (Inherits from `review-rigor` S5/S8.)

## 4. LLM-as-instrument check (required every session)

Before emit, run mentally:
- **Sycophancy:** would I have said this if the user implied the opposite? (Sharma et al. 2023.)
- **Anchoring:** is my first answer biasing all subsequent passes?
- **Lost-in-middle:** did I privilege start/end of long input over the middle? (Liu et al. 2023.)
- **Domain hallucination rate:** low for math/code-with-verifier; **high for citations, dates, statistics, names, package versions, line numbers**.
- **Self-consistency:** would 3 independent passes give the same answer? If unsure on a load-bearing claim, run a second pass (Wang et al. 2022).
- **Order sensitivity / prompt sensitivity:** would a paraphrased prompt give a different answer? (Sclar et al. 2024.)

Full list + citations in `references/llm-failure-modes.md`.

## 5. Output

Default report sections (omit if empty, never omit if load-bearing):
- TL;DR + headline confidence + reversibility.
- Pre-registered prediction → finding diff (P1 artifact).
- Findings (tagged, sourced).
- Limits / threats to validity.
- What would change my mind.
- Open questions / next avenues.
- Sources (`REFERENCES.md` tags).

Style invariants (always):
- Bullets/tables > prose. One idea per line. Fragments OK.
- Drop articles where unambiguous. No transitions ("additionally", "furthermore", "in summary").
- No hedging without new information. No prompt restatement.
- Cut any line that adds no information.
- **Define jargon and initialisms on first use.** Any field-specific term, acronym, or initialism (PTZ, FHSS, DECT, OTA, CPSC, FDA, AAP, FCC, RF, SIDS, SUID, CVE, MQTT, IoT, MAC address, etc.) gets a parenthetical definition or a brief inline gloss the first time it appears in a report body. After first use, the short form is fine. For reports with many initialisms, ship a "Glossary, defined on first use" section near the top with each term on its own bulleted line. Source: Wei standing rule 2026-05-17.

## 5a. Required companion files for every report (stakes ≥ L3)

Wei standing rule, 2026-05-17: a `REPORT.md` alone is not a complete palamedes deliverable. **Every report at L3 or higher stakes must ship these companion files**, not as "queued for follow-up." If they are not ready, the report is not ready.

**`ADVERSARIAL_REVIEW.md` (three passes, see `references/agentic-research.md`).**

- Pass 1: Prosecutor + Defender + Judge. Prosecutor argues against every load-bearing pick. Defender presents the strongest counter. Judge synthesizes with named confidence delta.
- Pass 2: Red-team + Reality-check + Judge. Red-team enumerates concrete failure modes (use error, install error, recall response timeline, supply-chain compromise). Reality-check runs the parent / user unboxing-and-use scenario. Judge synthesizes.
- Pass 3: Peer-review + Recency + Judge. Peer-review applies a domain-expert lens (pediatrician, CPST, infosec engineer, depending on category). Recency runs a fresh-source check (NHTSA / CPSC / FDA monthly feed, vendor recall page, infosec disclosure feeds).
- L4 stakes mean each pass uses **independent retrieval per role**, not just rephrasing of the same evidence.

**`METHODOLOGY_AUDIT.md`.** Per cited source, audit:

- What does this source actually test? Crash test? Chemical content? Install ease? Network capture? Policy review? Vulnerability scan?
- Independence: funder COI, affiliate revenue, vendor sponsorship, methodology transparency.
- Sample: how many products, how many testers, how reproducible.
- Methodology link: does the source publish its methodology document.
- **Where this source's bar exceeds US regulatory minimum.** This is the load-bearing question for safety categories.

**International standards layering.** Every report must explicitly cover:

- US baseline standard (FMVSS / CFR section / FDA classification).
- Equivalent or stricter international standards (EN, UN R, AS/NZS, Health Canada, JIS, etc.). Name them, name the gap.
- Independent crash / safety test programs that exceed the regulatory floor (ADAC, Stiftung Warentest, IIHS, Onward Security, etc.).
- Which picks pass the higher bar, which only pass the US floor.

**Optional / supplementary certification catalog.** Per category:

- Material / chemical: GREENGUARD Gold, OEKO-TEX, ClearTex, REACH, PFAS-free verification.
- Industry: JPMA (juvenile products), UL (electrical), ASTM (specific F-numbers).
- Privacy / security: SOC 2, ISO 27001, CTIA IoT, BSIMM.
- Domain-specific: FAA approval for travel car seats, FDA 510(k) for medical-device sleep products, etc.

**Independent audits and disclosures.** Where applicable: name the auditing firm, the date, the scope, and whether the audit is publicly available. Note where independent audits do NOT exist (silence is signal).

**Pattern of recurrence.** This rule was triggered by the 2026-05-17 babytime car-seats and sleep v1 reports shipping without these companion files. If a future report ships without them, treat it as a methodology regression and stop the loop.

## 5b. Source pre-audit must be visible in REPORT.md BEFORE picks

Wei standing rule, codified 2026-05-17 (second iteration of §5a after the babytime car-seats methodology audit was treated as a separate companion file rather than feeding picks). **Companion files are not enough.** REPORT.md itself must surface, BEFORE the recommendations section, two pre-audit subsections:

**1. Higher-rigor international standards.** Every safety-stakes report must scan international standards from countries with materially higher rigor than the US (typically Canada / Health Canada, Germany / ADAC, Switzerland / TCS, EU / EN-series, AS/NZS). Identify which higher-bar standards exist, name them with their scope, and **apply them as a filter against the candidate pick set BEFORE listing the picks.** A pick that only passes the US floor but is rejected by a higher-bar regulator (e.g., a product flagged by ADAC for chemical-content failure) does not appear in the picks table, or appears with a flag-down marker. The international audit is the input to the picks, not a footnote after them.

**2. Review-source pre-audit with AI-signal scan.** Every report cites third-party reviewers (Wirecutter, Consumer Reports, Lucie's List, niche blogs, etc.). **Before relying on a source, run the AI-signal scan from `/Users/wjia/Projects/deai/reference/ai-signals.md`** against the source's review text. AI-signal-heavy reviews (generic mic-drop framings, "perfect for parents who...", overused tricolons after colons, em-dashes, hedging-without-evidence) are **discarded entirely, not weighted lower.** The source-eligibility verdict (KEEP / DISCARD) appears in REPORT.md before the picks. Picks rely only on KEEP sources.

The deai AI-signals catalog (`/Users/wjia/Projects/deai/reference/ai-signals.md`) is the canonical reference for this scan. Notable signal classes:

- SIG_EM_DASH — em-dashes ` — ` framing contrasts
- SIG_NEGATIVE_PARALLELISM — "not X but Y" or "X, not Y" framings
- SIG_MIC_DROP — short punchy paragraph-ending fragments
- SIG_TRICOLON_AFTER_COLON — "you get: A, B, and C" listings
- SIG_GENERIC_PARENT_FRAMING — "perfect for the parent who...", "you'll love how it..."
- SIG_HEDGE_WITHOUT_EVIDENCE — "tends to be" without numbers
- SIG_AFFILIATE_BOOSTERISM — over-uniform positivity across competing products

**The pre-audit sections sit between the Decision card / Glossary and the Recommendations table.** The Recommendations table is the *output* of the pre-audit, not a pre-existing list that the pre-audit annotates.

**Pattern of recurrence.** Triggered by 2026-05-17 babytime car-seats v1 shipping the international-standards-comparison and source-methodology-audit AFTER the picks (in fact, in separate METHODOLOGY_AUDIT.md companion file). Wei explicitly flagged: "must be placed before. similar requirements for all passes if not implemented." Going forward, any report at L3+ stakes that lists picks before the source pre-audit is a methodology regression and the picks are not yet trustworthy.

## 5c. EU / equal-or-higher standards are Tier 1; US standards are Tier 2

Wei standing rule, codified 2026-05-18 during babytime car-seats ADAC reweighting iteration. **Across every safety-stakes consumer-product report**, the source-tier weighting is:

| Tier | Source class |
|---|---|
| **T1 (dispositive)** | EU standards (EN-series, EU Regulations, EU Directives) and equal-or-higher national standards (Canada / Health Canada, Switzerland / TCS, Australia-NZ / AS/NZS, Japan, New Zealand food regulator where stricter, UK Trading Standards / PSTI) |
| **T1 (independent testing)** | Member-funded consumer testing programs that meet or exceed the EU regulatory floor with peer-reviewed methodology aligned with toxicological reference doses (NOAEL / RfD / ADI from EPA, EFSA, JECFA): ADAC (Germany), Stiftung Warentest (Germany), TCS (Switzerland), Mozilla *Privacy Not Included (international, for connected products), ÖKO-TEST (Germany, for chemical contamination detection with stated detection limits). Mamavation XRF and EWG Skin Deep / Sunscreen Guide are **NOT in this tier** per §5j; see the T2-flagged-data row below. |
| **T1 (clinical guidance)** | Peer-reviewed clinical policy: AAP, La Leche League, IBCLC professional guidance, CDC peer-reviewed publications, *Pediatrics* and equivalent journals |
| **T2 (US standards + regulators)** | US federal standards and recall enforcement: CPSC, FDA, NHTSA, FMVSS, ASTM, FCC, FTC, 16 CFR series, 21 CFR series |
| **T2-FLAGGED (data-useful, framing-FLAG per §5j)** | Independent consumer-product investigators with documented but alarmist methodology: Mamavation XRF (raw heavy-metal ppm detections are data-useful when re-anchored to FDA / EPA / EU regulatory limits; Mamavation's own "lead-positive" / "Made Safe" labels are NOT used for hard disqualification), EWG Skin Deep + EWG Sunscreen Guide (per-product database lookup for ingredient identification is data-useful; EWG's 1-10 hazard scores and Top-Rated lists are NOT used for picks or hard disqualifications). Use raw data only; ignore interpretive framings. See §5j for the full rule. |
| **T2/T3 (review aggregators)** | Wirecutter, Consumer Reports, BabyGearLab, CSFTL, The Car Seat Lady, CarseatBlog, IIHS BEST BET, Reviewed.com — useful for in-use friction, install quality, and fit ratings; not used for primary safety ranking |
| **T3 (flagged for affiliate / blog-format)** | Lucie's List, SafeWise, Forbes Personal Shopper, Mother.ly, Gimme the Good Stuff, etc. — use only for category framing |
| **DISCARD (high AI-signal density or vendor-COI)** | Mommyhood101, TheBump, TeachToddler, mamita.blog, OrganicFormulaShop, EuromallUSA, Amazon vendor copy + reviews, etc. |

**Penalty / bonus framework, applied to every pick:**

- **+++** Source-T1 testing (ADAC, Mozilla *PNI, ÖKO-TEST, EU-standard-certified) AND clinical-T1 endorsement (AAP / AAD / NEA Seal where applicable): large positive weight; promoted to top of use case
- **+** Brand has T1 sister-product or T1 track record (e.g., Britax US ↔ Britax Römer EU; Nuna US ↔ Nuna EU): moderate positive weight
- **0** T1-not-rated; meets T2 (US standards + Wirecutter / CSFTL / etc.): neutral; kept only as next-best within use case
- **−−−** T1-failed (e.g., ADAC "poor" or PFAS chemical fail per peer-reviewed regulatory threshold; Mozilla *PNI "Yikes"; Mamavation XRF detection of regulated heavy metals **above the FDA / EPA / EU regulatory threshold** — NOT above Mamavation's aspirational floor): hard disqualify

**Implication for picks.** A pick that passes only the US standard (T2) is *kept* but flagged as ADAC-NOT-RATED / Mozilla-PNI-not-reviewed / etc. The signal asymmetry is honest: most US-market products are not in T1 test pools because T1 testers (ADAC, Stiftung Warentest, TCS) test EU-market product. The kept T2 picks survive because they meet the US legal floor, have clean recall history, and Wirecutter / CSFTL / IIHS provide credible in-use data. The flag is a pricing-signal: T1-rated alternatives at higher price points have stronger safety signal.

**Pattern of recurrence.** Triggered by 2026-05-18 babytime car-seats reranking ("ADAC = Tier 1, Wirecutter = Tier 2/3, CPSC = Tier 2, US standards = Tier 2"), then immediately generalized by Wei to "same standard for all reports... eu standards tier 1, other countries with higher or equal standards also tier 1." Going forward, every L2+ safety-stakes report must include this Source-tier-weighting section between Glossary and Recommendations.

## 5d. Adversarial review must complete BEFORE the visual artifact renders

Wei standing rule, codified 2026-05-18 second iteration after the babytime travel v1 ship-then-review sequence. **For any L2+ report, the adversarial review (≥3 passes per §5a + brand-coverage Pass 4 per §5c precedent) must be completed and its findings folded back into `REPORT.md` BEFORE any PDF, HTML, or other visual artifact renders.** Render is the visual artifact of an already-adversarially-reviewed document; it is not the v1 draft.

**Operational sequence (every L2+ report builds in this exact order):**

1. `P1_PREREGISTER.md` exists (or is written) with pre-registered prediction, stakes, confidence, falsifier.
2. `REPORT.md` v1 drafted with §5b pre-audit-first structure + §5c EU=T1 / US=T2 source weighting + Wei-voice rules + glossary defined on first use.
3. Companion files written: `REFERENCES.md` (per §3 citation protocol), `METHODOLOGY_AUDIT.md` (per §5a per-source audit + §5c source-tier weighting + brand-coverage Pass 4), `ADVERSARIAL_REVIEW.md` (≥3 passes per §5a + Pass 4 brand-coverage per §5c precedent).
4. **Each ADVERSARIAL_REVIEW finding folded back into `REPORT.md`.** A finding marked `[folded back]` in `ADVERSARIAL_REVIEW.md` must have a corresponding change in `REPORT.md`. A finding marked `[surfaced honestly]` must have a corresponding caveat or honest-trade-off paragraph in `REPORT.md`.
5. **Only then:** render the PDF / HTML / visual artifact via `references/output-rendering.md` or the project-specific render tool.
6. Verify the rendered artifact (page count, file size, extractable text on at least the first and last page).

**Render-before-review is a methodology regression.** If render runs against a REPORT.md whose ADVERSARIAL_REVIEW.md is incomplete or whose findings have not been folded back, the deliverable is not ready and the render artifact is invalid. The render command is the LAST step, not a working draft.

**Parallel-agent corollary.** When `dispatching-parallel-agents` is invoked to build multiple categories concurrently, each agent independently follows steps 1-6 within its assigned subdirectory. The agent does NOT render its PDF until step 4 is complete for that agent's category. This is the file-isolation seam that makes parallel dispatch safe: each subdirectory is one self-contained palamedes run.

**Pattern of recurrence.** Triggered by 2026-05-18 babytime travel v1 build, where Cascade wrote `REPORT.md` first, then companion files, then rendered the PDF, then wrote the `ADVERSARIAL_REVIEW.md` with all four passes marked `[folded back]`. The folding-back was real (Cascade wrote the report with the four-pass discipline already in mind), but the SEQUENCE was render-before-the-formal-adversarial-review-file. Wei flagged this and directed: "full adversarial reviews must be done before even rendering the html and pdf. note this as iron law." This section codifies the iron law and the operational sequence going forward.

## 5e. Cross-category brand-consistency at integration

Wei standing rule, codified 2026-05-18 during babytime wave-1 parallel-dispatch integration after the four wave-1 agents (carriers, pacifiers, bath-toys, teething) returned their handoff notes. **For any multi-category report suite where ≥2 categories are dispatched in parallel (`dispatching-parallel-agents` invocation), an integration agent step runs AFTER all wave-N category handoffs exist and BEFORE wave-N+1 dispatches.** The integration agent runs three sub-tasks:

1. **Inter-agent brand-consistency reconciliation.** For every brand appearing in 2+ wave-N reports OR in 1 wave-N + 1 existing report, verify rating consistency (+++ / + / 0 / —), brand-description factual consistency, and self-flagged inconsistencies in retrofit Pass 4 reconciliation tables. Defensible divergences must be one-sentence-justified (different SKU, different test source, different stake tier). Self-flagged inconsistencies are treated as confirmed and resolved at integration layer.
2. **URL-consistency check.** For every URL appearing in 2+ REFERENCES.md files, verify URL identity, access-date format, and incident-count / year / scope alignment when the same primary is cited. The authoritative figure is the agent who did a TIER A direct chunk-read of the primary; popular-press aggregations are downgraded.
3. **v3.1 retrofit evidence-table spot-check.** Independently retrieve 1-3 of the highest-stakes citations per category and confirm the verbatim 30-word snippet actually appears on the page. If the snippet cannot be confirmed, flag as a fabrication candidate or as a benign chunk-mismatch; in either case, the integration agent surfaces it.

**Surgical-cross-ref policy.** The integration agent MAY edit existing REPORT.md files for cross-references only. Each edit is a 1-3 line addition that adds NO load-bearing claims. After ALL cross-refs are applied across all affected reports, the integration agent batch-re-renders each affected report; the re-render is justified because the markdown changed; the adversarial review remains valid because no load-bearing claim was added.

**Forbidden modifications.** The integration agent may NOT edit wave-N ADVERSARIAL_REVIEW.md or METHODOLOGY_AUDIT.md files (those are wave-N agents' artifacts). Findings requiring those edits are flagged for a v2 micro-pass by the original agent.

**Pattern of recurrence.** 2026-05-18 wave-1 babytime integration. Three carriers-flagged cross-category brand-coverage gaps (Cybex Maira.tie, Maxi-Cosi carriers, Chicco Easyfit) aligning with car-seats / strollers / feeding adjacent coverage; one teething self-correction (Bumkins-feeding endorsement); one feeding-corruption flag (a2 Milk row, out-of-scope for integration agent, surfaced for separate dispatch); two v2 micro-passes flagged (teething EN 71-3 amendment + Yetonamr year/URL/incident-count; bath-toys Yetonamr incident-count). Without §5e the integration step did not formally exist; cross-category inconsistencies would have shipped as wave-1-final and been caught only at later cross-reference review or never. Codified to make the integration step a required artifact of any parallel-dispatch suite.

## 5f. Anti-theater force-binds on §5a adversarial review

Wei standing rule, codified 2026-05-18 after the babytime wave-1 dispatch used a v3.1 self-review template with concrete-count force-binds and produced 3-11 substantive deltas per agent (vs. the pre-v3.1 self-review template which permitted "all clear" checkmark theater). **The §5a adversarial review for any L2+ report MUST include force-binds that produce concrete artifacts, not checkmark statements.** Specifically:

- **Pass 1: hazard-prose minimization grep** with line-numbered matches. Run a grep against REPORT.md for softening adjectives (`minor|manageable|controlled|addressed|mitigated|rare|edge case|unlikely|hypothetical|theoretical|low.risk|acceptable|reasonable|fine|gentle|safe enough`). For every hit, quote the surrounding sentence, retrieve the T1 source's framing of the same hazard verbatim, then decide: keep the adjective (T1 source agrees), harden it (T1 source is more cautionary), or remove it (no T1 backing). Each hardening or removal is a concrete REPORT.md delta.
- **Pass 2: citation evidence table** with verbatim 30-word snippets from source URLs + 200-char URL-response evidence for the 3 weakest citations. See §5g for the evidence-of-evidence floor.
- **Pass 3: seven-edge-case audit** covering NICU graduate or premature infant, twin or higher-order multiple, low-budget family, international or travel-abroad family, special-needs family (sensory / motor delay / medical fragility), breastfed-exclusively family (where category-relevant), and single-parent or no-second-adult-available family. For each edge case, name the single best pick from the report OR add a "no good fit" admission paragraph to REPORT.md (not appendix-only). Each "no good fit" admission is a forced user-facing delta.
- **Pass 4: adjacent-category brand reconciliation table** with a 5-row soft floor. For each brand featured in adjacent reports, name the rating in adjacent vs the rating in this report and the one-sentence reconciliation. If the table is shorter than 5 rows, justify why the adjacent reports really do have fewer than 5 shared brands.
- **Pass 5a: two paragraph rewrites** with before-and-after diff in the appendix and applied via `edit` to REPORT.md. The rewrites must change the substantive claim or the voice register, not cosmetic edits. If after one honest attempt the agent cannot name two genuine rewrites, escalate with the exact phrasing "I cannot name two genuine rewrites after honest attempt. Either the report is unusually clean OR I am unable to self-criticize. Wei or the integration agent should decide which." Do not pad with cosmetic edits.
- **Pass 5b: honest rubric** on 6 axes (Completeness of brand coverage; Honesty of hazard framing; Specificity of use-case picks; Quality of citation evidence; Wei-voice adherence; Framework-rule application per §5b + §5c + §5d). Rate 1-5 with at-least-2-axes-below-5 floor. For every axis rated below 5, fill in "What would make it a 5" and "Fix now or v2." For every axis with "Fix now," apply the fix to REPORT.md. For every axis with "v2," add the item to the handoff note's "Outstanding for v2" section.
- **Meta-bind: minimum 3 concrete REPORT.md deltas** (not appendix-only) across Passes 1-5. If the agent's edit count is less than three after honest attempt, restart Pass 5a or add an additional Pass 3 admission. Do not pad with cosmetic edits.

**Known limitation.** Self-review is the weakest adversarial setup; LLM self-review tends to confirm the original output. The force-binds mitigate the weakness with grep-based hazard-prose audit, 200-char retrieval evidence, edge-case audit with named "no good fit" admissions, adjacent-category reconciliation table with row-count floor, paragraph rewrites with before-and-after diff, honest rubric with at-least-2-below-5 rule, but cannot eliminate it. The true adversarial layer is integration agent (per §5e) or external review.

**Pattern of recurrence.** 2026-05-18 babytime wave-1 dispatch v1 build with original §5a allowed a 30-second `ADVERSARIAL_REVIEW.md` with four "no findings" passes to satisfy the prompt. The v3.1 retrofit force-binds produced concrete delta counts of 7 (carriers), 5 (pacifiers), 11 (bath-toys), 9 (teething) and surfaced one hallucinated author attribution that the original pass missed. Codified so future L2+ reports begin §5a with the force-binds in place rather than retrofitting them.

## 5g. Evidence-of-evidence floor for retrieved citations

Wei standing rule, codified 2026-05-18. Extends §3 (citation protocol) and §8 Anti-Pattern #4 (abstract-only iron law). **Each agent must paste a 200-char block from the actual retrieved URL response for the 3 weakest citations in the session.** "Weakest" means least-confident, paywall-gated, search-snippet-only, or any citation the agent cannot directly chunk-read this session. If the agent cannot produce the 200-char block because they did not actually retrieve the source this session, the citation is tagged `[priors-only]` regardless of where the abstract came from.

**This is a session-bound floor, not a one-time check.** Every session that produces or updates an L2+ REPORT.md runs the 3-weakest spot-check. Carryover `[priors-only]` tags from prior sessions are honored only if the prior session's evidence is preserved in `REFERENCES.md` Verify-before-cite outcomes section.

**Operational form.** Citation evidence table columns: SOURCE | URL | ACCESS-DATE-THIS-SESSION | HTTP-STATUS-OR-EXTRACT-CONFIRMED | VERBATIM-30-WORD-SNIPPET-FROM-PAGE | READ-DEPTH per §1 P2 read-depth tagging. Walk every entry in REFERENCES.md OR sample to cover the picks-driving citations (full registry for L4 stakes; representative sample for L2). For the 3 least-confident, paste the first 200 chars of the retrieved URL response into the appendix.

**Pattern of recurrence.** 2026-05-18 babytime teething v3.1 retrofit Check 1 caught a hallucinated author attribution ("McNeice et al 2019" in v1 first pass → real Nissen, Lau, Cabot, Steadman 2019 verified via PMC chunk-14 read). The 200-char snippet floor is what made the hallucination catchable; without it the misattribution would have shipped as wave-1-final and been carried into integration agent's cross-category brand-reconciliation table as if real. Codified so the evidence-of-evidence step is a required artifact of every §5a adversarial review at L2+.

## 5h. deai voice-scan before final render

Wei standing rule, codified 2026-05-18 (after wave-1 integration revealed Wei-voice rated 4 across all four wave-1 categories with the deai-scanner not run this session in any of them). **The deai-scanner must run on REPORT.md before the FINAL PDF or HTML render.** It does NOT need to run throughout iteration; intermediate passes through REPORT.md need not invoke deai (the burst-vs-mic-drop / tricolon-after-colon / "X not Y" framing / short-fragment-opener distinctions are the agent's discipline mid-iteration, see `wei-voice.md`). The pre-final-render deai-scan is a gate, not a continuous check.

**Operational sequence (extends §5d).** Every L2+ report builds in this exact order:

1. `P1_PREREGISTER.md` exists with pre-registered prediction, stakes, confidence, falsifier.
2. `REPORT.md` v1 drafted with §5b pre-audit-first structure + §5c EU=T1 / US=T2 source weighting + Wei-voice rules + glossary defined on first use.
3. Companion files written: `REFERENCES.md`, `METHODOLOGY_AUDIT.md`, `ADVERSARIAL_REVIEW.md` with §5a passes + §5c Pass 4 + §5f anti-theater force-binds + §5g evidence-of-evidence floor.
4. Each ADVERSARIAL_REVIEW finding folded back into `REPORT.md`. A finding marked `[folded back]` must have a corresponding change; a finding marked `[surfaced honestly]` must have a corresponding caveat in `REPORT.md`.
5. **Run the deai-scanner on REPORT.md.** Commands: `python3 ~/.claude/skills/deai/deai-scan.py <REPORT.md>` (lexical/structural signals: SIG_EM_DASH, SIG_NEGATIVE_PARALLELISM, SIG_MIC_DROP, SIG_TRICOLON_AFTER_COLON, SIG_GENERIC_PARENT_FRAMING, SIG_HEDGE_WITHOUT_EVIDENCE, SIG_AFFILIATE_BOOSTERISM) and `python3 ~/.claude/skills/deai/deai-check.py <REPORT.md>` (per-sentence score band + family coverage map + top firing sentences). Report the score, top firing families, top firing sentences, and the comparison to a Wei-canonical anchor of the same genre. Fix any signal that fires above the canonical baseline.
6. Only then: render the PDF / HTML / visual artifact.
7. Verify the rendered artifact (page count, file size, extractable text on at least the first and last page).

**Self-attested checklists do not count.** A self-attested "voice-clean" claim in the report appendix without a deai-scanner run does not satisfy this rule. The scanner output is the artifact.

**Parallel-agent corollary.** Each wave-N category agent runs the deai-scanner on its own REPORT.md before its own render, not the integration agent on each category's report. Integration agent (§5e) does not re-run deai because the surgical cross-refs are 1-3 line additions that do not materially change the voice register of the host report.

**Pattern of recurrence.** 2026-05-18 babytime wave-1 v3.1 retrofit Pass 5b. All four agents rated Wei-voice 4 (none rated 5) with the consistent gap "deai-scanner not run this session." Without §5h the deai gate was implicit and skipped under session-budget pressure; with §5h the gate is operational-sequence step 5 and skipping it is render-without-the-gate (the same failure mode §5d closed for the adversarial-review gate).

## 5i. Citation chip + marginalia markup coverage discipline

Wei standing rule, codified 2026-05-18 after the wave-3 retrofit audit revealed that 7 of 18 babytime categories had ZERO citation chips in their REPORT.md source and several others carried chips only in the Decision Card OR only in the back half. **Every load-bearing factual claim in an L2+ REPORT.md must carry a backticked tier-tag chip resolving to a `REFERENCES.md` entry, and every granular aside currently interrupting the running argument must demote to `^[...]` marginalia.** The chips and marginalia are what the render pipeline promotes into the right gutter of the rendered PDF / HTML; where the markdown is unmarked, the gutter stays empty and the design feature is dead weight on the page.

This is an **authoring discipline**, not a retrofit pass. Chips and marginalia get added as the prose is written, in §5h step 2 (`REPORT.md v1 drafted`). A retrofit pass is what happens when this rule is skipped at v1 and Wei has to dispatch a marker-discipline wave (the 2026-05-18 wave-3 case). The retrofit wave is corrective; the codified discipline is preventive.

**Markup syntax (mirror the carriers/REPORT.md exemplar).**

- **Citation chips:** backticked tier-tag with tier number 1/2/3 + optional tier suffix + comma + space + ID, where ID matches a `REFERENCES.md` row. Examples: `` `[T1, ADAC-2024-CAR-SEATS]` ``, `` `[T1-clinical, AAP-2022-SAFE-SLEEP]` ``, `` `[T2, CPSC-2010-INFANTINO]` ``, `` `[T2, 16-CFR-1228]` ``, `` `[T3, WIRECUTTER-2024-CARRIERS]` ``. Multiple chips at paragraph end stack in the gutter and are clean.
- **Marginalia:** `^[content]` immediately after the sentence the aside qualifies. Brackets cannot nest. Markdown formatting inside the aside is fine.
- **Placement:** chips go AT THE END of the paragraph or sentence they cite; marginalia goes IMMEDIATELY AFTER the sentence it qualifies. Do not bury chips or marginalia mid-sentence; the render pipeline expects standalone spans.

**What counts as load-bearing (gets a chip).** Any sentence that (1) references a regulatory standard, (2) references a CPSC / FDA / NHTSA / EPA / other regulator action, (3) references a clinical study or guideline, (4) references an EU-T1 testing body finding (ADAC / Stiftung Warentest / ÖKO-TEST / TCS / IHDI), (5) references a brand-attribution or product-class verification, or (6) cites a numerical fact tied to a specific source. Inherits the §3 citation discipline; this rule adds *typographic obligation* on top of *factual obligation*.

**What counts as marginalia (gets demoted).** Granular subset breakdowns, source-verification details, methodology asides, date-of-access notes, attribution chains for verbatim quotes, mid-sentence parenthetical qualifications longer than ~15 words. The test: if a reader can skip the parenthetical and the sentence still carries the argument, the parenthetical is marginalia. If skipping it loses the argument, leave it inline.

**Missing REFERENCES.md ID → `NEEDS-CITATION-<slug>` placeholder, never fabrication.** If a claim deserves a chip but no matching ID exists, add a placeholder chip `` `[T?, NEEDS-CITATION-<short-slug>]` `` and list every placeholder in the agent handoff under `## NEEDS-CITATION placeholders added`. The render pipeline marks placeholders as "not found in REFERENCES.md" in the gutter, which is the intended honest signal. Inventing a citation ID and a fake REFERENCES.md row is a §3 violation; the placeholder pattern is the honest alternative.

**Coverage floor.** A 200-line L2+ REPORT.md targets 20-30 chips minimum and 8-15 marginalia, scaled with density of factual claims. Specifically: Decision Card chips every numerical / regulatory / clinical claim; picks tables chip per pick on the verification basis (Stiftung Warentest result, ADAC test grade, IHDI Industry Partner status, Mamavation XRF result, FAA TSO C-100 certification); hard disqualifications chip per row on the recall ID / FDA communication / clinical reason; source-tier-weighting section chips every named regulator or framework; stakes / closing section chips every numerical fact and regulatory date. A category with chips only in the Decision Card or only in the back half is partial compliance.

**Operational integration.** §5h sequence step 2 (`REPORT.md v1 drafted`) is extended: REPORT.md is not v1-complete without the §5i coverage floor met. Before proceeding to step 3 (companion files), run:

```
grep -cE '\[T[123][-a-z]*, [A-Z0-9-]+\]' <REPORT.md>
grep -cE '\^\[[^]]+\]' <REPORT.md>
```

If either count falls below the coverage floor, return to authoring before companion files. The §5g evidence-of-evidence floor (Pass 2 citation evidence table) consumes the chip IDs as input; an empty REPORT.md produces an empty citation evidence table and triggers the cascading-failure path the wave-3 retrofit demonstrated.

**Parallel-agent corollary.** Each wave-N category agent applies §5i to its own REPORT.md. The integration agent (§5e) verifies coverage counts as part of the cross-category audit. An integration agent that finds a category with coverage below the §5i floor halts and dispatches back to the original agent rather than fixing in place.

**Pattern of recurrence.** 2026-05-18 wave-3 audit: 7 of 18 babytime categories (teething, bath-toys, prenatal-late, skincare, strollers, sunscreen, travel) had ZERO citation chips after the v3.1 retrofit + §5e + §5f + §5g + §5h discipline was applied to each. The §5h gate caught Wei-voice issues; the §5g gate caught hallucinated attributions; none of the existing gates caught the absent-typographic-markup pattern because every prior rule operated on prose content, not on the markup that the render pipeline relies on to populate the right gutter. Wei flagged the empty gutter in the teething PDF on 2026-05-18 21:04; the retrofit was dispatched the same day. Going forward, §5i closes the gap so the empty-gutter pattern does not ship at v1.

## 5j. Scientific-credibility filter for hazard-scoring sources (citation-laundering guard)

Wei standing rule, codified 2026-05-18 after the babytime sunscreen + skincare v1+v2+v2.1 deliverables shipped with EWG Sunscreen Guide / EWG Skin Deep tagged as T1 (independent) and Mamavation XRF tagged as T1 (independent testing). Wei flagged the EWG placement as a palamedes pre-audit failure: "EWG is a fake alarmist company that over-alerts on not scientifically credible ppms in products. why did this pop up as a source? palamedes should've caught and excluded quack sources."

The failure mode is **citation-laundering**: a source has a documented methodology + is widely cited by mainstream outlets (Wirecutter, BabyCenter, NYT lifestyle, AAP-adjacent guidance pieces), so it accumulates apparent credibility through citation frequency. The pre-audit accepts the source as T1 because reproducibility-of-scoring and mainstream-citation-count are both satisfied. But neither test verifies that the source's interpretive methodology is **toxicologically and clinically credible**. The hazard scores can be alarmist, the thresholds can be unanchored to peer-reviewed regulatory consensus, and the funding base can carry structural COI with the natural-products / organic / wellness industry — and the source still scores as T1 under the §5b + §5c rules as they stood before this clause.

**The rule.** For any source proposing **hazard scores, safety ratings, or curated product lists at consumer-product granularity**, the pre-audit must independently verify all four of:

1. **Toxicological-threshold anchoring.** The source's hazard thresholds align with peer-reviewed regulatory reference doses (NOAEL / RfD / ADI / TDI from EPA, EFSA, JECFA, FDA, Health Canada). If the source uses an "aspirational" or "precautionary" threshold below the peer-reviewed regulatory threshold without explicit per-ingredient toxicological justification, the source fails this test.
2. **Clinical-consensus alignment.** The source's interpretive framings align with the relevant clinical professional society's position (AAP / AAD / NEA / ACOG / AAFP for pediatric / dermatology / eczema / obstetric / family-medicine domains). A source whose ratings would discourage use of products the clinical-T1 society explicitly recommends fails this test.
3. **Peer-reviewed critique scan.** Search for peer-reviewed critique of the source's methodology in PubMed, Cochrane, or the relevant clinical-professional-society journal. If ≥2 independent peer-reviewed critiques have flagged the methodology as scientifically unsound, the source fails this test.
4. **Funding-base COI scan.** Identify the source's funding base. If the funding base includes industry actors whose products score systematically well under the source's methodology, this is a structural COI that must be flagged regardless of the methodology document.

**Named failure exemplars (2026-05-18 baseline; not exhaustive).** The following sources have been verified as failing one or more of the four tests and are demoted to **T2-FLAGGED (data-useful, framing-FLAG)** across every palamedes-driven report going forward:

- **EWG (Environmental Working Group) — Skin Deep cosmetic database + Sunscreen Guide + "Dirty Dozen" produce list + Top-Rated curated lists.** Fails tests 1, 2, 3. (1) EWG hazard scores routinely flag ingredients at exposure concentrations below recognized NOAEL / RfD. (2) AAD has explicitly declined to endorse the EWG Sunscreen Guide on grounds that EWG-style hazard messaging discourages sunscreen use, increasing UV under-protection risk relative to the trace-ingredient concerns EWG flags. (3) Peer-reviewed critique includes Carroll + Maldonado in *Pediatrics* 2019; Annals of Internal Medicine "Dirty Dozen" methodology critique; Academy of Nutrition and Dietetics rejection of EWG produce-list methodology; USDA Pesticide Data Program public dispute. Test 4 also concerning: EWG donor base includes organic / natural-cosmetic industry actors whose products score well under EWG methodology. **Use:** per-product database lookup for ingredient identification (data-useful). **Do NOT use:** EWG 1-10 hazard scores, EWG Top-Rated lists, EWG hazard rating 7-10 hard-disqualification triggers.
- **Mamavation — XRF heavy-metal investigations + "Made Safe" labels + curated brand lists.** Fails tests 1, 2 (partial). (1) Mamavation's "lead-positive" / "Made Safe" labels use aspirational thresholds (often 10 ppm or lower for heavy metals) that are below FDA / EPA / EU regulatory limits without per-ingredient toxicological justification. (2) Mamavation's interpretive framings recurrently characterize products as unsafe at exposure levels the relevant clinical society does not consider risk-relevant. **Use:** raw XRF ppm detection data, when re-anchored to FDA / EPA / EU regulatory limits for the specific contaminant (e.g., FDA 0.1 ppm limit for lead in cosmetics; EU 0.5 ppm limit for lead in cosmetics). **Do NOT use:** Mamavation's own "lead-positive" / "PFAS-positive" / "Made Safe" labels for hard disqualification; the labels reflect aspirational thresholds, not regulatory thresholds.
- **"Gimme the Good Stuff" + "Green Choice Lifestyle" + "Lucie's List" lifestyle/non-toxic-living blogs.** Already at T3 (flagged for affiliate format) per §5c; the §5j framework adds the toxicological-threshold-anchoring failure as a second flag. Use only for category framing, never for hard disqualifications.
- **Other consumer-protection investigators not in the canonical T1 (independent testing) list.** Default to T2-FLAGGED pending verification against the four tests. Burden of proof is on promoting a source UP to T1, not on demoting from T1.

**Operational form.** §5b pre-audit must include, between the international-standards scan and the picks table, a **scientific-credibility scan** for every hazard-scoring source the report references. The scan output is a table:

| Source | Test 1 (threshold anchoring) | Test 2 (clinical-consensus alignment) | Test 3 (peer-reviewed critique) | Test 4 (funding-base COI) | Verdict |
|---|---|---|---|---|---|

A source passes only if all four cells read PASS or N/A (the source does not propose hazard scores at all). A source that fails any one of the four is demoted to T2-FLAGGED (data-useful, framing-FLAG) at minimum, T3 / DISCARD if the failure is severe (peer-reviewed critique density high AND clinical-society disavowal AND funding COI).

**Picks framework implication.** A pick anchored on a §5j-flagged source's framing alone is not picks-eligible. The pick must anchor on **at least one credible source** per the four tests: T1 regulatory (EU / FDA / EPA / Hawaii Act / etc.), T1 clinical (AAP / AAD / NEA Seal / etc.), T1 peer-reviewed pharmacology / toxicology (JAMA / Lancet / NEJM / *Pediatrics* / *Dermatology* / etc.), or T1 independent testing (ADAC / Stiftung Warentest / TCS / ÖKO-TEST with stated detection limits / Valisure for benzene with stated ppb thresholds). The §5j-flagged sources may **layer additional weight** only after the credible-source anchor is established; they cannot **substitute** for it.

**Hard-disqualification implication.** A hard disqualification must anchor on a credible source per the same four-tests pass. "EWG hazard rating 7-10" or "Mamavation lead-positive" alone are NOT valid hard-disqualification triggers. Valid hard-disqualification triggers anchor on: a named regulatory ban (Hawaii Act 104, EU Annex II, FDA recall, CPSC recall), a clinical-society contraindication (AAP "do not use under 6 months", AAD "not recommended for sensitive skin"), a peer-reviewed pharmacology finding (Matta et al *JAMA* 2019 plasma-concentration above toxicology threshold), or an independent testing result above the peer-reviewed regulatory threshold (Mamavation XRF detection above FDA 0.1 ppm lead limit, Valisure benzene detection above ~10 ppb threshold).

**Pattern of recurrence.** 2026-05-18 babytime sunscreen + skincare v1+v2+v2.1 deliverables shipped with EWG Sunscreen Guide rated T1 and the +++ EWG-list weighting applied to 9 of 18 sunscreen picks. Wei flagged: "EWG is a fake alarmist company... palamedes should've caught and excluded quack sources." The §5g (evidence-of-evidence floor) caught the citation-verification dimension but did not catch the source-credibility dimension; §5g verifies that the source said what the cite claims it said, not that the source's methodology is credible. §5j closes the gap by adding the four-tests scientific-credibility scan to the §5b pre-audit. Going forward, every L2+ report's source pre-audit produces a §5j credibility scan table BEFORE the picks; a report that lists picks anchored on a §5j-flagged source's framing alone is a methodology regression.

**Retroactive correction scope (2026-05-18).** Babytime reports that may reference EWG / Mamavation framings at T1 weighting: sunscreen, skincare (active deliverable; corrected in this session), plus likely-affected: bath-toys, teething, feeding, formula, prenatal-early, prenatal-late, carriers, monitors, gates, activities, toys. Each affected report needs a §5j pass against its source list, with the picks reframed onto credible anchors and the hard-disqualifications re-examined. The sweep is dispatched as a separate retrofit wave.

Adapt shape to host (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`). Loop is fixed; shape adapts. See `references/output-schemas.md` for stake-tier-specific templates.

**Optional PDF / HTML rendering.** If the user asks for the report as a PDF, an HTML deliverable, a printable, or any phrasing implying a visual artifact (not just markdown), load `references/output-rendering.md`. The canonical implementation lives at `/Users/wjia/Projects/babytime/render/`; the design system (solarpunk editorial palette, 9.5pt serif, Letter portrait, tier-tag footnote chips, margin notes, recall-timeline-style SVG figures) is codified there and should be preserved unless the user explicitly overrides. Triggers include: "render as PDF", "output to PDF", "make it a deliverable", "produce a printable", "I want a PDF report". The output mode is opt-in; markdown remains the default.

## 6. File / artifact policy (anti-sprawl)

- Default: **append**. Index-first, grep before write.
- Pre-write: `ls` target dir; `grep -rli <topic>` siblings.
- Match → append under `## YYYY-MM-DD, <delta>` section. Dedupe: if new claim duplicates existing row, update-in-place + note revision.
- One file per topic. Date is metadata in section header, not in filename. No `-v2` / `-final` / `-copy` suffixes.
- Scratch / session history → `localonly/` (gitignored), never workspace root.
- ≥3 files on same topic → consolidate, archive rest in `localonly/archive/`.

## 7. Disk-before-denial

"Where / did / do I have <X>" → `ls` candidate dirs + `grep -rli <topic>` first, answer second. Never claim absence without searching.

## 8. Anti-patterns

**Top 4 (absolute, never, iron laws):**
1. Fabricated cite, author + year + title combo not retrieved this session.
2. `[T*-verified]` tag without retrieval this session OR without row in `REFERENCES.md`.
3. Convergence-as-truth, N passes agree → high confidence, without independent retrieval.
4. **Abstract-only citation for any magnitude / scope / caveat / mechanism / methodology claim at L2+**. Abstracts are author-marketing-optimized; the headline number is best-case, the baseline is often unstated or weak, and the failure-mode caveats live in the body. Quoting a speedup, % gain, accuracy delta, or sample-size from `read:abstract` and binding any recommendation to that number is a direct violation. Allowed uses of `read:abstract`: (a) direction-of-effect at L1, (b) existence-of-method at any tier, (c) flagging a candidate to read at body-depth. Forbidden uses at L2+: any quantitative claim, any "production-ready" framing, any "X beats Y" comparison, any stacking inference. Self-violation 2026-05-16 (token-optimization research, Rounds 1+2): every MEDIUM/LOW item was abstract-only; adversarial-review forced retraction. The skill now treats abstract-only magnitude citation as `[priors-only]`, not `[T*-verified]`, regardless of where the abstract came from.

**Major:**
- Approximate quote without `paraphrase:` prefix.
- Steelman skipped or steelman that asks for the same evidence as original (rephrasing).
- Falsifier skipped or falsifier that names no specific evidence-shape that would flip.
- "Studies show" / "research suggests" without naming specific studies (citation laundering).
- Numeric claim without source file:line or URL.
- Single-pass conclusion at L3+ stakes.
- Stale source treated as current (no `[stale:<date>]` tag where window exceeded).
- Generalization beyond sample scope without `[inferred:generalization]` tag.

**Minor / hygiene:**
- "DK label" without measured calibration.
- "Incorporate" routed without first running loop on paste.
- Isolated demand for rigor (skeptical of disliked, credulous of liked).
- Selective skepticism · motte-and-bailey · no-true-Scotsman · Galileo gambit · Texas sharpshooter · sunk-cost · bandwagon.
- Prompt restatement · narration · per-prompt ingestion file · dated filenames for recurring topics.
- Goodhart on tokens (compression past meaning).
- `[unknown]` used as epistemic cowardice (when retrieval was feasible).

## 9. Reference loading, load on demand, not by default

| File | Load when |
|---|---|
| `REFERENCES.md` | every cite (registry of all primary sources used) |
| `references/source-grading.md` | tier dispute, new domain, source provenance question |
| `references/replication-and-validity.md` | empirical claim / "study shows X" / effect size / RCT |
| `references/bias-catalog.md` | every multi-claim report (cognitive + research + LLM bias list) |
| `references/causal-inference.md` | "X causes Y" / observational data / DAG question |
| `references/llm-failure-modes.md` | required every session, self-instrument check |
| `references/agentic-research.md` | parallel branches / harness / worktree / RAG / debate protocol |
| `references/output-rendering.md` | user asks for PDF / HTML / printable / deliverable (opt-in visual output mode) |
| `references/study-guide-site.md` | user asks for an exam-prep / cram / certification / curriculum site with daily cadence and pedagogy appendix |
| `references/landscape-summary-report.md` | user asks for a landscape one-pager / skim sheet / fridge magnet |
| `references/confidence-calibration.md` | numeric confidence / Brier / forecasting |
| `references/output-schemas.md` | report draft / stake-tier formatting |
| `references/examples.md` | first time using skill in a new domain (anchor calibration) |
| `references/failure-log.md` | every session at start, scan for prior traps in this skill class |

## 10. Install + sync

- Claude global: `~/.claude/skills/palamedes/`
- Claude repo: `<repo>/.claude/skills/palamedes/`
- Cursor: `.cursor/rules/palamedes.mdc` (frontmatter conversion; body points back at canonical)
- Generic: `AGENTS.md` snippet referencing this dir

**Drift hazard:** known mirrors at `~/.claude/skills/palamedes/SKILL.md` and any workspace sibling copies. Sync via `skill-sync` skill. This repository directory (`SKILL.md` + `references/` + `REFERENCES.md`) is the single source of truth.

## 11. Skill-meta, known limits

This skill cannot:
- Substitute for domain expertise (oncology / law / cryptography requires named experts).
- Verify claims against paywalled / offline sources without user assistance.
- Detect coordinated misinformation (state-actor disinfo, troll farms), out of scope, kick to OSINT tooling.
- Resolve contested empirical domains (nutrition, parts of IR, macroeconomics, parts of psychology, parts of education research), flag `[contested]`, present multiple weightings.
- Calibrate itself without offline Brier tracking, see `references/confidence-calibration.md`.

This skill **expects to be wrong** about ~10–20% of load-bearing claims at L2 stakes, ~5% at L3, target <2% at L4. See `references/failure-log.md` to track and update.

## 12. Version + changelog

**v3.6.0 (2026-05-18)**, §5j added + §5c source-tier table reorganized: scientific-credibility filter for hazard-scoring sources (citation-laundering guard). Four-tests scan (toxicological-threshold anchoring, clinical-consensus alignment, peer-reviewed critique scan, funding-base COI scan). Named failure exemplars demoted from T1 (independent testing) to T2-FLAGGED (data-useful, framing-FLAG): EWG Sunscreen Guide / EWG Skin Deep (fails tests 1, 2, 3), Mamavation XRF (fails tests 1, 2 partial), "Gimme the Good Stuff" lifestyle blogs (already T3 per §5c; §5j adds second flag). §5c table tightened: T1 (independent testing) criterion now requires alignment with NOAEL / RfD / ADI from EPA / EFSA / JECFA. ÖKO-TEST added as a legitimate T1 replacement. Penalty/bonus framework: hard-disqualify (−−−) now requires alignment with FDA / EPA / EU regulatory threshold, not Mamavation aspirational floor. Triggered by Wei directive 2026-05-18 after babytime sunscreen + skincare v1+v2+v2.1 deliverables shipped with EWG and Mamavation tagged T1.

**v3.5.0 (2026-05-18)**, §5i added: citation chip + marginalia markup coverage discipline. Every load-bearing factual claim carries a backticked tier-tag chip resolving to a REFERENCES.md entry; every granular aside demotes to ^[...] marginalia. Coverage floor: 20-30 chips minimum + 8-15 marginalia per 200-line L2+ REPORT.md. Triggered by Wei directive 2026-05-18 after wave-3 audit found 7 of 18 babytime categories had ZERO citation chips post v3.4.0 retrofit.

**v3.4.0 (2026-05-18)**, §5e + §5f + §5g + §5h added: cross-category brand-consistency at integration (for multi-category parallel dispatch); anti-theater force-binds on §5a adversarial review (Pass 1 hazard-prose grep, Pass 2 citation evidence table, Pass 3 seven-edge-case audit, Pass 4 brand reconciliation, Pass 5a forced rewrites, Pass 5b honest rubric, minimum 3 REPORT.md deltas); evidence-of-evidence floor (200-char URL retrieval for the 3 weakest citations per session); deai voice-scan before final render (gate, not continuous). Triggered by Wei directives 2026-05-18 during babytime wave-1 parallel-dispatch integration. Operational-sequence §5h now supersedes §5d's 6-step sequence with a 7-step sequence inserting the deai-scan as step 5 between fold-back and render.

**v3.3.0 (2026-05-18)**, §5d added: adversarial review must complete and findings be folded back into REPORT.md BEFORE the PDF / HTML / visual artifact renders. Includes the parallel-agent corollary for `dispatching-parallel-agents`. Triggered by Wei directive after the babytime travel v1 ship-then-review sequence.

**v3.2.0 (2026-05-18)**, study-guide-site output mode added: new `references/study-guide-site.md` documenting the multi-page browseable HTML site template with pedagogy appendix (memory palace, mnemonic quick reference, evidence-tagged techniques, daily integration schedule overlay). Description triggers expanded with "build me a study guide", "exam prep program", "cram program", "certification site", "curriculum site", "weekday cadence", "study program for N days", "memory palace for [exam]", "pedagogy appendix", "spaced repetition program". Joins the long-form PDF (`references/output-rendering.md`) and landscape one-pager (`references/landscape-summary-report.md`) as the third documented output mode. Worked example: `cc-prep/study_guide/` (ISC2 CC certification cram, 10 weekdays, 16 HTML pages, full Appendix D pedagogy section, 107 Anki cards). Triggered by the user's "incorporate this into the study guide output for palamedes" directive 2026-05-18 after the CC-prep build generalized into a reusable pedagogy pattern.

**v3.1.0 (2026-05-17)**, synthesis-task triggers expanded in `description:` to catch phrasings that previously slipped past the load criteria: "study guide, exam prep, flashcards from sources, anki from sources, build curriculum, summarize papers, extract from documentation, synthesize external sources". Also added "synthesis" to the loop description. Triggered by a `qa-prep` 4-pass audit where the skill's `read:body` iron-law floor never fired because the task was phrased as "create anki cards / find resources / fully read parse", synthesis phrasings that did not match any prior trigger keywords. Closes the routing gap so future synthesis tasks load the skill automatically rather than requiring explicit user invocation several passes in.

**v3.0.0 (2026-05-14)**, full adversarial-review rewrite. New: question-type routing, P1–P4 loop, 10-tag system with read-depth, citation registry (REFERENCES.md), 8 reference docs (source-grading, replication-and-validity, bias-catalog, causal-inference, llm-failure-modes, agentic-research, output-schemas, confidence-calibration), examples, failure-log. Replaces v1 5-step "Validate / Dialectic / Unknowns / Refine / DK guard" loop.

**v1.x (≤2026-05-14)**, see `git log` if version-controlled, else superseded.

Changelog policy: bump major on stop-condition / tag-grammar / loop-structure change. Bump minor on new reference doc. Patch on typo / clarification.
