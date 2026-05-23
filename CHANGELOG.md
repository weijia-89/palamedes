# Changelog

## browser UI v1.0.0 (2026-05-23): `ui/` — local research front end

Added the Palamedes browser UI to this repo (canonical home; previously prototyped under `cursor-sdk-playground/palamedes-ui`).

- **`ui/`** — static research app: L0–L4 stakes, question-type field, templates (full report, landscape one-pager, executive brief, study-guide-site outline), token/cost heuristic, refinement chips, markdown downloads.
- **`ui/prompts/research-system.md`** — runtime prompt bundle loaded by the app.
- **`scripts/serve-ui.sh`** — `python3 -m http.server` on `127.0.0.1:8765`.
- Footer links to [github.com/weijia-89/palamedes](https://github.com/weijia-89/palamedes) only (no local path or external queue references).
- **README** reframed: Palamedes is prompts + skill + browser UI, not prompts-only.

**Not in this release:** multi-agent orchestration, live retrieval, or server-side key storage — use [`prompts/`](./prompts/) and [`skill/SKILL.md`](./skill/SKILL.md) for that.

---

## skill v3.6.0 (2026-05-18): §5j scientific-credibility filter (citation-laundering guard) + §5c source-tier table reorganization

Codified §5j to close a pre-audit failure surfaced by Wei during the babytime sunscreen + skincare v1+v2+v2.1 review: EWG Sunscreen Guide had been tagged T1 (independent) and Mamavation XRF had been tagged T1 (independent testing) under §5c as it stood through v3.5.0, when both sources fail at least two of four scientific-credibility tests. Wei flagged the EWG placement: "EWG is a fake alarmist company that over-alerts on not scientifically credible ppms in products. why did this pop up as a source? palamedes should've caught and excluded quack sources."

**What's in the rule.**

- The failure mode named: **citation-laundering**. A source with documented methodology + heavy mainstream-citation count accumulates apparent credibility through citation frequency, but neither reproducibility-of-scoring nor mainstream-citation-count tests verify that the interpretive methodology is toxicologically and clinically credible.
- Four-tests scientific-credibility scan, applied to any source proposing hazard scores / safety ratings / curated product lists at consumer-product granularity:
  1. **Toxicological-threshold anchoring** — alignment with peer-reviewed regulatory reference doses (NOAEL / RfD / ADI / TDI from EPA, EFSA, JECFA, FDA, Health Canada). Aspirational thresholds below the regulatory threshold without per-ingredient toxicological justification = fail.
  2. **Clinical-consensus alignment** — alignment with the relevant clinical professional society's position (AAP, AAD, NEA, ACOG, AAFP). Ratings that would discourage use of products the clinical-T1 society explicitly recommends = fail.
  3. **Peer-reviewed critique scan** — search PubMed / Cochrane / clinical-professional-society journal for methodology critique. ≥2 independent critiques flagging as scientifically unsound = fail.
  4. **Funding-base COI scan** — funding base includes industry actors whose products score systematically well under the methodology = structural COI flag.
- Named failure exemplars demoted to **T2-FLAGGED (data-useful, framing-FLAG)**: EWG (Skin Deep + Sunscreen Guide + Dirty Dozen + Top-Rated lists; fails tests 1, 2, 3; peer-reviewed critique includes Carroll + Maldonado in *Pediatrics* 2019, Annals of Internal Medicine Dirty Dozen critique, Academy of Nutrition and Dietetics rejection, USDA Pesticide Data Program public dispute, AAD declination to endorse), Mamavation (XRF investigations + "Made Safe" labels; fails tests 1, 2 partial), "Gimme the Good Stuff" / "Green Choice Lifestyle" / "Lucie's List" lifestyle blogs (already T3 per §5c; §5j adds second flag).
- Use raw data only; ignore interpretive framings. EWG per-product database lookup for ingredient identification = data-useful. EWG 1-10 hazard scores, EWG Top-Rated lists, EWG 7-10 hard-disqualification triggers = do not use. Mamavation raw XRF ppm detection data re-anchored to FDA / EPA / EU regulatory limits = data-useful. Mamavation "lead-positive" / "PFAS-positive" / "Made Safe" labels = do not use.
- Picks framework implication: a pick anchored on a §5j-flagged source's framing alone is not picks-eligible. Pick must anchor on at least one credible source (T1 regulatory, T1 clinical, T1 peer-reviewed pharmacology / toxicology, or T1 independent testing per the four-tests pass).
- Hard-disqualification implication: "EWG hazard rating 7-10" or "Mamavation lead-positive" alone are NOT valid hard-disqualification triggers. Valid triggers: named regulatory ban (Hawaii Act 104, EU Annex II, FDA recall, CPSC recall), clinical-society contraindication, peer-reviewed pharmacology finding, independent testing result above the peer-reviewed regulatory threshold.
- Operational form: §5b pre-audit must include a scientific-credibility scan table (Source | Test 1 | Test 2 | Test 3 | Test 4 | Verdict) for every hazard-scoring source referenced in the report.

**§5c table reorganization (companion edit).**

- T1 (independent testing) criterion tightened to require alignment with toxicological reference doses (NOAEL / RfD / ADI from EPA / EFSA / JECFA).
- Mamavation XRF and EWG Skin Deep / Sunscreen Guide explicitly removed from T1 (independent testing); ÖKO-TEST added as a legitimate T1 replacement (peer-reviewed methodology with stated detection limits).
- New T2-FLAGGED row added: "Independent consumer-product investigators with documented but alarmist methodology" — Mamavation XRF + EWG Skin Deep + EWG Sunscreen Guide. Use raw data only; ignore interpretive framings.
- Penalty/bonus framework: −−− (hard-disqualify) now requires alignment with FDA / EPA / EU regulatory threshold for the specific contaminant; the bar "Mamavation lead-positive" alone is no longer valid for hard disqualification.
- T3 (flagged for affiliate format) row updated to include "Gimme the Good Stuff" explicitly.

**Motivation.** §5g (evidence-of-evidence floor) catches the citation-verification dimension — did the source actually say what the cite claims it said. §5g does NOT catch the source-credibility dimension — is the source's interpretive methodology toxicologically and clinically credible. The 2026-05-18 sunscreen + skincare deliverables passed §5g but failed the citation-laundering test that §5j now codifies. §5j is the missing gate between §5g and the final picks.

**Retroactive correction scope.** Babytime reports flagged for retrofit pass: sunscreen, skincare (active deliverable, corrected in same session as §5j codification), plus likely-affected: bath-toys, teething, feeding, formula, prenatal-early, prenatal-late, carriers, monitors, gates, activities, toys. Each report needs a §5j pass against its source list, with picks reframed onto credible anchors and hard-disqualifications re-examined. Dispatched as a separate retrofit wave.

---

## skill v3.5.0 (2026-05-18): §5i citation chip + marginalia markup coverage discipline

Codified §5i as an iron-law authoring discipline for L2+ reports. **Every load-bearing factual claim in REPORT.md must carry a backticked tier-tag chip resolving to a `REFERENCES.md` entry, and every granular aside currently interrupting the running argument must demote to `^[...]` marginalia.** The chips and marginalia are what the render pipeline (currently `/Users/wjia/Projects/babytime/render/render.py`) promotes into the right gutter of the rendered PDF or HTML. Where the markdown is unmarked, the gutter stays empty and the design feature is dead weight.

**What's in the rule.**

- Markup syntax: backticked `` `[T1, ID]` `` / `` `[T2, ID]` `` / `` `[T3, ID]` `` with optional tier suffix (`-clinical`, `-forum`) for citation chips; `^[content]` for marginalia. ID resolves to `REFERENCES.md`; placement is end-of-paragraph for chips, immediately-after-sentence for marginalia.
- Load-bearing test (gets a chip): references a regulatory standard, a regulator action (CPSC / FDA / NHTSA / EPA), a clinical study or guideline, an EU-T1 testing body finding (ADAC / Stiftung Warentest / ÖKO-TEST / TCS / IHDI), a brand-attribution verification, or a numerical fact tied to a source.
- Marginalia test (gets demoted): granular subset breakdowns, source-verification details, methodology asides, date-of-access notes, attribution chains, mid-sentence parentheticals >~15 words. If a reader can skip the parenthetical and the sentence still carries the argument, it's marginalia.
- Coverage floor: 200-line L2+ REPORT.md targets 20-30 chips minimum and 8-15 marginalia, scaled with density of factual claims. Decision Card, picks tables, hard disqualifications, source-tier-weighting section, and stakes section each chip per load-bearing claim. Chips only in Decision Card OR only in back half is partial compliance.
- Missing REFERENCES.md ID → `NEEDS-CITATION-<slug>` placeholder, never fabrication.
- Operational integration: extends §5h step 2 (`REPORT.md v1 drafted`). REPORT.md is not v1-complete without the §5i coverage floor met; grep-check before proceeding to step 3 (companion files).
- Parallel-agent corollary: each wave-N category agent applies §5i to its own REPORT.md; integration agent (§5e) verifies coverage as part of cross-category audit.

**Motivation.** 2026-05-18 wave-3 audit found 7 of 18 babytime categories (teething, bath-toys, prenatal-late, skincare, strollers, sunscreen, travel) had ZERO citation chips after the v3.1 retrofit + §5e + §5f + §5g + §5h discipline was applied to each. The §5h gate caught Wei-voice issues; the §5g gate caught hallucinated attributions; none of the existing gates caught the absent-typographic-markup pattern because every prior rule operated on prose content, not on the markup that the render pipeline relies on. Wei flagged the empty gutter in the teething PDF on 2026-05-18 21:04. Wave-3 marker-discipline retrofit dispatch infrastructure built same day at `/Users/wjia/Projects/babytime/localonly/handoff/parallel_dispatch_v3/`; §5i codified to prevent recurrence.

**Worked example.** `/Users/wjia/Projects/babytime/carriers/REPORT.md` (the best-marked-up exemplar; 6 chips + 4 marginalia across 270 lines as of v1; mirrors the syntax + placement + coverage discipline §5i prescribes). Future agents building L2+ reports read this file alongside §5i to ground the discipline.

---

## skill v3.2.0 (2026-05-18): study-guide-site template option

Added a third output mode to the skill: **multi-page browseable study-guide site with pedagogy appendix**. Documented in new reference `references/study-guide-site.md` (~17 KB). Joins the existing long-form PDF mode and landscape one-pager mode.

**What's in the template.**

- Output structure: corpus markdown, multi-page HTML site, Anki deck.
- Pedagogy appendix template (6 subsections D.1-D.6): evidence summary with T1-verified citations, memory palace walkthrough (N rooms for N domains, ~2 items/locus capacity ceiling from Ondrej et al. 2025), domain-by-domain mnemonic quick reference, daily integration schedule, honest caveats (mocks beat the palace, transfer-appropriate processing, sleep matters), tier-tagged sources.
- Inline memory-anchor blockquote pattern at the top of each Part.
- Generator and Anki integration with exclusion-list pattern for user's known terms.
- Locus-pattern table (multi-shelf pantry / four-cushion couch / stove burners / spice rack / mirror reflection / sponges in a row) mapping spatial patterns to content shapes.
- Failure modes specific to study-guide sites (citation laundering on pedagogy claims, unfamiliar-space palace, >2 items/locus, mnemonics for unordered material, em-dashes, missing the mocks-beat-the-palace caveat).

**Citations (T1-verified, body-read).**

- Ondrej J. et al. (2025). The method of loci in the context of psychological research: A systematic review and meta-analysis. British Journal of Psychology. PMC12514325. Effect sizes d=0.42-0.88; GRADE very low to low.
- Serra M.J. et al. (2025). The Use of Retrieval Practice in the Health Professions: A State-of-the-Art Review. PMC12292765. Two decades of retrieval-practice replication confirmed.

**Worked example.** `/Users/wjia/Projects/cc-prep/study_guide/` (ISC2 CC certification cram, 10 weekdays, 16 HTML pages, full Appendix D, Anki deck with 107 cards). Builds 2026-05-17 with pedagogy appendix added 2026-05-18.

**Trigger expansion.** Added to skill `description:`: "build me a study guide", "exam prep program", "cram program", "certification site", "curriculum site", "weekday cadence", "study program for N days", "memory palace for [exam]", "pedagogy appendix", "spaced repetition program". Mirror-synced to `~/.claude/skills/palamedes/` and `.cursor/rules/palamedes.mdc`.

**Reference cross-links.** `references/output-rendering.md` updated to point at the new file for exam-prep variants. `references/study-guide-site.md` cross-references `source-grading.md`, `llm-failure-modes.md`, `output-rendering.md`, `landscape-summary-report.md`.

**Motivation.** Wei's CC-prep work (2026-05-17 to 2026-05-18) developed a complete pedagogy pattern that generalized beyond the ISC2 CC subject matter: 5-room palace mapping, 6-section appendix structure, inline memory-anchor blockquotes, daily integration schedule overlay, T1-verified citation backbone. Incorporating it into palamedes makes the pattern reusable for any future exam-prep / certification / cram / curriculum deliverable. Triggered by user's "incorporate this into the study guide output for palamedes" 2026-05-18.

---

## skill v3.1.0 (2026-05-17): expanded synthesis-task triggers

Added trigger phrases to the skill `description:` field to catch synthesis tasks that previously slipped past the load criteria: "study guide, exam prep, flashcards from sources, anki from sources, build curriculum, summarize papers, extract from documentation, synthesize external sources." Also added "synthesis" to the loop description.

**Motivation.** A 4-pass audit on `qa-prep` (Wei's QA exam-prep deliverables) found that the skill's `read:body` iron-law floor never fired because the user phrased the task as "create anki cards / find resources / fully read parse" — synthesis-task phrasings that did not match any of the skill's trigger keywords. The skill was loaded by the user invoking it explicitly several passes later. Trigger expansion closes the routing gap so future synthesis tasks load the skill automatically.

**Mirror sync.** `~/.claude/skills/palamedes/SKILL.md`, `<workspace>/.claude/skills/palamedes/SKILL.md`, and `<workspace>/.cursor/rules/palamedes.mdc` all refreshed.

**Deployment mirror cleanup (same session).** The legacy `ai-research` deployment mirrors at `~/.claude/skills/ai-research/`, `<workspace>/.claude/skills/ai-research/`, and `<workspace>/.cursor/rules/ai-research.mdc` were removed; replaced by `palamedes` mirrors. The standalone `weijia-89/ai-research` local repo was already gone. Backups at `/tmp/ai-research*pre-rename-2026-05-17*`.

---

## v5.0.0 (2026-05-16): renamed to `palamedes`; merged with `ai-research`

**Renamed** `research-synthesis-prompt` → `palamedes`. Greek mythology: Palamedes was the inventor of measurement, the one who exposed Odysseus's feigned madness, and was framed and stoned to death in revenge. Patron of "the clever one who catches the deceiver and loses anyway." Apt for a tool whose job is catching where an LLM is bluffing.

**Merged** `weijia-89/ai-research` (the agent-loadable skill v2.0.0 covering rigorous research at the coding-task level) into this repo. The skill now lives at [`skill/`](./skill/); the two synthesis prompts moved to [`prompts/`](./prompts/). The two surfaces share the same underlying epistemic methodology (hierarchy of evidence, dialectic adversarial review, no-fabrication citations, mode-collapse recognition); previously they lived in separate repos and risked drifting.

**License** changed from MIT to PolyForm Noncommercial 1.0.0 with an Iron Law addendum (for-profit contact requirement + AI / LLM ingestion covenant). See [`LICENSE`](./LICENSE).

### Layout

- `prompts/research-synthesis.md` (was `prompt.md`): the multi-agent dialectic synthesis prompt.
- `prompts/adversarial-review.md` (was `adversarial-review-prompt.md`): the post-synthesis adversarial-pass prompt.
- `skill/SKILL.md` (was `weijia-89/ai-research/SKILL.md`): the agent-loadable research-loop skill.
- `skill/REFERENCES.md`, `skill/REVIEW.md`, `skill/references/*.md`: supporting docs for the skill.
- `assets/`: image assets for the README.

### Predecessor repos

- `weijia-89/research-synthesis-prompt`: this repo's git history, renamed via `gh repo rename`.
- `weijia-89/ai-research`: content merged here; the standalone repo is archived as of 2026-05-16.

---

## v4.2 (May 2026)

Stripped model-specific references from `prompt.md`, `adversarial-review-prompt.md`, and `README.md`. The prompts now describe **capability classes** (live-web search model, deep-research model with broad web access, strong reasoning model, highest-reasoning long-context model) rather than naming specific providers or model versions. The Mode B selection step asks the user to name the actual provider and model variant for each phase, so the model-diversity warning lands on whatever the user picked instead of going stale every six months when a provider rebrands.

The empirical model-diversity claim (~60% correlated error on same-provider pairs, arXiv 2506.07962) stays. That's a finding about architecture similarity, not about any specific provider.

Added an MIT `LICENSE`.

---

## v4.1 (May 2026)

Adversarially reviewed adversarial-review-prompt.md and found five things wrong or overstated.

The calibration check was targeting middle compression: "flag if 70% of scores fall in 72–85." That's not what the literature shows. The failure direction is overconfidence toward high scores, not the middle. The old check would have flagged legitimate scoring while missing the actual problem. Fixed the threshold and direction.

URL verification was still just a URL-existence check. A model can hallucinate a citation pointing to a real paper on a related domain, fetch it successfully, and call it verified. Phase 1 and Prompt 1 now parse body text and look for the specific assertion. [CLAIM NOT IN SOURCE] drops to speculative. [ABSTRACT-ONLY] for paywalled pages where you can't verify methodology. [CLAIM AMBIGUOUS IN SOURCE] when the source discusses the same domain but not the specific number.

The "Mode A is broken" classification was too broad. Huang et al. (ICLR 2024) is specifically about intrinsic self-correction with no external feedback. Phases with URL fetching have external grounding that partially escapes it. Phase 6, pure reasoning, no tools, is the specific failure point. Narrowed it there.

"Genuinely independent" for Mode B was overstated. arXiv 2506.07962 puts cross-model error correlation at about 60% for same-provider pairs. Better than single-model, not independent. Added a model diversity warning and a model-selection prompt so the tradeoff is visible before you run anything.

The context isolation instruction was listed as the primary fix for anchoring bias. Instruction-based debiasing has weak evidence for deep anchoring. Promoted the fresh context Final Gate, pass the revised claims table to a new session with no reasoning chain, as the actual structural escape.

---

## v4 (May 2026)

Separate adversarial review stage: adversarial-review-prompt.md.

The synthesis prompt could put together a coherent initial report but had no mechanism for actively trying to break what it built. This stage starts from finished claims and tries to prove them wrong. Zombie stat tracing, disconfirmation searches, cross-tool indirectness checks, attack rating on every counterargument.

Two modes. Mode A runs all eight phases in one pass for models with live web access. Mode B generates five prompts for distributing phases across capability classes, a live-web search model for source verification and disconfirmation, a strong reasoning model for indirectness, and the highest-reasoning long-context model available for re-synthesis. Mode B Prompt 5 is always the final step regardless of how you ran phases 1–4.

---

## v3.1 (May 2026)

Ported the fixes from adversarial-review-prompt back into prompt.md. Some of these should've been there from the start.

URL verification in the synthesis stage was checking whether a link resolved, not whether the source actually said what I was citing it for. A 200 OK pointing to a real paper on a related topic is not verification. Two gates now: HTTP status first, then parse the body text and find the specific assertion. Not in the source text: drops to speculative regardless of tier. Paywalled (abstract-only): can't verify methodology or population, one-tier downgrade and flagged.

Same gap in zombie stat tracing. I was looking for the source, not confirming the number was actually in it. Fixed.

The calibration failure direction was wrong. LLMs skew toward high confidence, not the middle. Added a check: if more than half the final scores come in at 80+, run a downward pressure pass. Three independent papers confirm the overconfidence direction (arXiv 2502.11028, 2508.06225, 2603.09985).

Added the attack rating taxonomy to adversarial self-review: [strong, downgrade] / [partial, survives with caveats] / [no viable attack found]. And the "consensus ≠ compounded confidence" rule now includes the correlated error data, same-provider models agree about 60% of the time when both get something wrong (arXiv 2506.07962), so convergence from architecturally similar models isn't the independent signal it looks like.

---

## v3 (May 2026)

Evidence methodology layer. v2 could find sources but had no enforcement of a consistent evidence hierarchy and no way to catch common methodological failure modes.

Study design hierarchy with tier-based confidence ceilings, tier sets the maximum possible score, quality issues reduce from there. Pre-registration checks (ClinicalTrials.gov, PROSPERO, OSF). Effect size gate: ≥70 confidence claims need an effect size alongside any p-value. HARKing detection, hypothesis appearing in Discussion rather than Introduction, post-hoc subgroups framed as primary findings, suspiciously clean hypothesis-result alignment. Meta-analysis quality checklist: I², fixed vs. random effects model selection, funnel plot symmetry, double-counting of underlying RCTs, CI interpretation.

The tier-ceiling system makes the rubric internally consistent. A claim can't reach 85 on expert opinion alone.

---

## v2 (April 2026)

v1 could find sources but had no way to tell whether three agents agreeing meant "this is well-established" or "all three trained on the same papers."

Verbatim quote passthrough for ≥70 confidence claims, direct source text required, not paraphrase. Reconstructed from memory: [QUOTE UNVERIFIED]. Atomic handoff format for downstream synthesis agents (CLAIM / CONFIDENCE / SOURCE / QUOTE / STATUS), grouped by [AGREEMENT] / [CONFLICT] / [SINGLE SOURCE]. [CONFLICT] flagging for cross-agent disagreement. [RECENCY RISK] for claims where primary evidence may fall within 12 months of training cutoff.

---

## v1 (early 2026)

Initial version. Source discovery across academic databases (PubMed, JSTOR, Google Scholar, Semantic Scholar, Scopus), preprints (arXiv, SSRN, bioRxiv, OSF), citation chains forward and backward, grey literature, lateral disciplines, non-English lit, contrarian sources, Retraction Watch. Per-source trustworthiness: venue quality, author credentials, funding/COI, methodology, replication status, recency, citation context. Confidence scoring 0–100. Adversarial self-review pass. Structured HTML output with evidence ledger.
