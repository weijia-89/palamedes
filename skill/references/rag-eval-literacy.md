# RAG / LLM-judge eval literacy (deterministic)

Load when: `type=methodological` and question matches **§TRIGGER** below, OR user asks how Ragas / RAG eval / faithfulness / context recall works, OR reporting ≥2 automated RAG metrics.

Palamedes scope: **research synthesis about eval** — not CI config, not repo harnesses. Code/eval-corpus tiering → **trainer** (`~/Projects/trainer.skill/references/trainer-epistemic-layers.md`).

---

## §TRIGGER (load gate)

Load this file **iff** any:

1. User question contains (case-insensitive): `ragas`, `rag eval`, `faithfulness`, `context recall`, `context precision`, `answer relevancy`, `llm-as-judge`, `retrieval augmented`, `RAG pipeline eval`.
2. Session `type=methodological` **and** subject is LLM/RAG output quality (not generic research design).
3. Output includes ≥2 numeric automated metrics on the same RAG trace.

If none → do **not** load (avoid eval noise on pure lit-review).

---

## §MET-1 Metric definitions (use these names only)

| ID | Metric | Measures | Does **not** measure |
|----|--------|----------|----------------------|
| M-F | Faithfulness | Answer claims supported by **retrieved** context | Medical/legal truth; correctness of retrieval |
| M-CR | Context recall | Reference claims attributable to retrieved context | Generation quality |
| M-CP | Context precision | Useful chunks ranked high (variant-dependent) | Faithfulness |
| M-AR | Answer relevancy | Answer addresses the question | Faithfulness |

---

## §REF-1 Reference requirement (decision tree — run before any eval claim)

```
INPUT: metric name M, inputs available {reference, reference_contexts, response, retrieved_contexts}

IF M = context recall (M-CR):
  IF reference OR reference_contexts missing → STOP: emit "[unknown: recall requires reference]" — do NOT claim "no gold needed"

IF M = context precision (M-CP):
  IF reference present → variant = with-reference (compare chunks to reference)
  ELIF response present AND reference absent → variant = without-reference (compare chunks to response) — label explicitly
  ELSE → STOP: "[unknown: precision variant indeterminate]"

IF M = faithfulness (M-F):
  IF retrieved_contexts missing → STOP: "[unknown: faithfulness requires retrieved context]"

IF M = answer relevancy (M-AR):
  IF reference present → variant = with-reference (Ragas-style: synthetic questions from reference)
  ELIF user question present AND reference absent → variant = prompt-only (response vs question) — label explicitly
  ELSE → STOP: "[unknown: relevancy variant indeterminate]"

IF user says "reference-free RAG eval":
  FORBID inferring "no reference fields anywhere"
  ALLOW ONLY: M-F, M-AR prompt-only variant, and M-CP without-reference variant — state variant in output
```

**Iron law:** Never collapse variants. Wrong variant = **methodology regression** (SKILL §8 #5).

---

## §TRI-1 Metric-drop triage (deterministic)

When metric **decreases** vs prior run or baseline, emit **exactly one** primary locus row:

| Metric drop | Primary locus (assign first match) | Mandatory falsifier test |
|-------------|-----------------------------------|---------------------------|
| M-F ↓ | Generation / prompt / model | Oracle context held fixed; swap model only — if M-F still ↓ → generation |
| M-CR ↓ | Retrieval / index / chunking | Known reference fact absent from all retrieved chunks |
| M-CP ↓ | Retriever ranking or chunk boundaries | Re-order chunks manually; if M-CP ↑ → ranking |
| M-AR ↓ | Task spec / prompt / question mismatch | Oracle context + frozen retrieval; if M-AR still ↓ → task spec |

If two metrics drop with **different** loci → `[contested:multi-metric]` (§MM-1).

---

## §MM-1 Multi-metric contested (mandatory when ≥2 metrics reported)

**Gate MM-1:** If output includes ≥2 of {M-F, M-CR, M-CP, M-AR} on the **same** pipeline run:

1. **FORBID** a single headline score or one-word verdict ("good", "passed", "green").
2. **REQUIRE** one table row per metric: `metric | value | direction vs baseline | locus if down (§TRI-1)`.
3. **IF** any pair implies conflicting loci (e.g. M-F ↑ and M-CR ↓):
   - Tag block `[contested:multi-metric]`
   - **REQUIRE** `Decision-rule:` one sentence naming which metric blocks action (default: **recall or faithfulness regression blocks** unless user states otherwise in session).

Stop condition: MM-1 violated → do not emit ship/release recommendation from metrics alone.

---

## §JUD-1 LLM-judge instrument rules (deterministic)

| Rule | Condition | Action |
|------|-----------|--------|
| J-1 | High M-F + wrong retrieval | Tag `[inferred:circular-grounding]` — faithfulness is w.r.t. retrieved text only |
| J-2 | Same judge + same prompts, N≥2 runs averaged | **NOT** independent replication — tag `[single-instrument]` |
| J-3 | Independent replication claim | **REQUIRE** ≥1 of: different judge model, human spot-check, rule-based check on structured fields |
| J-4 | Metric score → safety / clinical / legal conclusion | **STOP** — forbidden without separate human/domain gate |

Cross-ref: `llm-failure-modes.md` §RAG-judge rows.

---

## §OUT-1 Required output block (when this file loaded)

Append to Findings or standalone block:

```
### RAG eval literacy (deterministic)
- Metrics reported: [list IDs M-F / M-CR / M-CP / M-AR]
- REF-1 variant per metric: [with-reference | without-reference | N/A]
- TRI-1 locus (if any regression): [one row or "none"]
- MM-1 contested: [yes + decision-rule | no]
- JUD-1 instrument: [judge id / single-instrument flag / replication instruments]
```

Missing block when §TRIGGER fired = stop condition fail.
