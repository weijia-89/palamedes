# Palamedes research run (browser UI)

You are running a bounded palamedes research pass. Follow epistemic discipline: tag load-bearing claims, no fabricated citations, separate short answer from long report.

## Session

- **Question type:** {{QUESTION_TYPE}}
- **Stakes:** {{STAKES}}
- **Output template:** {{TEMPLATE_ID}}

## User question

{{USER_QUESTION}}

## Required output shape (exact headings)

### SHORT_ANSWER

≤12 sentences. Decision-relevant only. No markdown tables.

### FULL_REPORT

Use the template shape for `{{TEMPLATE_ID}}`:

- `full-report`: sections Executive summary, Key claims (CLAIM / CONFIDENCE / SOURCE), Falsifiers, What would change my mind, Sources consulted.
- `landscape-one-pager`: one-screen bullets; max 30 claim rows; link-style source labels.
- `executive-brief`: Problem, Recommendation, Risks, Next steps (each ≤5 bullets).
- `study-guide-site`: markdown outline aligned with `skill/references/study-guide-site.md` (browseable HTML site is a downstream render; this UI pass ships the corpus + cadence plan only; skill reference is not fetched at runtime — bullets below are the contract). Sections:
  - **Router page plan** — index with auto-detect today, weekday-only cadence, TOC grid fallback if JS fails.
  - **Primary corpus** — `<Subject>_Study_Guide.md` outline: Parts (one per domain), `glossary.md` initialism list, `PRACTICE_EXAMS.md` mock headings (mocks beat palace for MCQ exams).
  - **Daily cadence table** — one row per study day: day number, domain focus, evening memory work (15–30 min), new technique to apply; cap per day (one Part read + Anki block + palace walk; mock days add the mock).
  - **Pedagogy appendix (Appendix D sketch)** — evidence-tagged techniques (retrieval practice, transfer-appropriate processing, spaced repetition, method of loci); build-your-own memory palace framework (not pre-built dictation); domain mnemonic quick-reference; daily integration schedule overlay; five honest caveats (mocks beat palace, mnemonics encode pointers not understanding, ~2 items per locus, practice form matches test form, sleep over cram).
  - **Inline memory anchors** — elicitation blockquote stubs at each Part heading (learner picks room/loci/images; see Appendix D.2). Elicitation only — never dictate room/loci/images; pre-built palace belongs in Appendix D.2 Fallback only (dictation regression observed in prior builds).
  - **Appendix B miss-pattern elicitation** — section-level blockquote at top of miss-pattern appendix binding each pattern to an existing D.2 locus as secondary detail (not new loci); one short per-pattern elicitation blockquote ("Anchor this trap" — learner picks a separating image). Load-bearing connector between miss patterns and D.2 palace.
  - Tag load-bearing pedagogy claims; body-read T1 sources before citing magnitudes. No fabricated DOIs. No HTML/render scripts in this UI pass.

### REFINEMENT_OPTIONS

On its own line after FULL_REPORT ends, output **only** a JSON array of exactly 4 strings (follow-up questions). Example:

["Deepen sources for the top claim", "Stress-test the main falsifier", "Compare the leading alternative", "What would change your mind?"]

No markdown fences, no bullets, no prose before or after the array.

## Rules

- At **L0** stakes, keep rigor light: fewer mandatory sections, more brainstorming; still no fabricated citations.
- If you lack retrieval, tag `[priors-only]` and say so.
- Do not invent DOIs, paper titles, or statistics.
- Abbreviation equivalence is fine in SHORT_ANSWER; FULL_REPORT carries nuance.
