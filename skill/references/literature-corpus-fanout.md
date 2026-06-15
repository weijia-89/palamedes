# Literature corpus fan-out — Pattern 9

Load when: **ingest N papers**, **literature fan-out**, **systematic review corpus**, **one sub-agent per paper**, or `literature/{pdfs,text,ingests}/` tree.

**vs Pattern 8:** P8 = external artifacts + verify citations inside; P9 = **papers are the corpus**, each gets critical teardown → index → synthesis.

**Composes with:** P7 (primaries inside a review) · P8 (external returns in same session) · `authoritative-review-literacy.md` · `synthesizer-agent.md`

---

## Invoke when

| Trigger | Pattern |
|---------|---------|
| ≥3 peer-reviewed papers for canon/reference | 9 |
| Systematic reviews / meta-analyses / "authoritative" corpus | 9 + `authoritative-review-literacy.md` |
| Sub-agent per paper + index | 9 |
| Single paper L2+ | one paper-ingest agent; index when ≥3 |
| ChatPRD/Piranesi return only | 8, not 9 |

---

## Ladder + waves

```
extract → paper_ingest ×N (parallel) → index → adversarial (L3+) → synthesize → parent judge
```

| Agent | Output |
|-------|--------|
| Paper ingestor ×N | `{slug}_ingest.md` |
| Index writer | `LITERATURE_INDEX.md` |
| Adversarial | cross-corpus CAMV |
| Synthesizer | `SYNTHESIS.md` |

**Caps:** 1 paper/agent; parent must not monolith-read N≥5 PDFs; ingest ≤4,500w; wrong PDF → flag in attestation + refetch at L2+.

Prompt SSOT: `prompts/literature-paper-ingest.md`

---

## Paper ingest schema (mandatory)

1. Bibliographic (DOI/arXiv)
2. **Study type** (`authoritative-review-literacy.md` §STUDY-TYPE)
3. **AUTH-1** A-1–A-10 (or subset for empirical/position)
4. Scope & method (N, search, limitations authors state)
5. Key findings — `[verified from text]` + section anchor only
6. **P3 teardown:** steelman · falsifier · ≥2 `bias-catalog.md` rows · replication/validity · overclaim audit
7. Domain hook — `[inferred]` unless paper states
8. Coverage attestation (path, lines, sections, wrong-file flag)

**Forbidden:** cheerleading summary; `[verified]` without anchor; meta-review as meta-analysis.

---

## Index (`LITERATURE_INDEX.md`)

Rows: slug · citation · study type · AUTH-G1 pass/weak · headline · corpus role (anchor/supporting/catalog) · **absolute ingest path**. Plus convergent themes table.

## Synthesis (`SYNTHESIS.md`)

Role-relabel ingests as external. Sections: epistemic status + session bet · ontology/failure modes · themes `[convergent]`/`[contested]` · corpus gaps · falsifiers · operator paths (absolute). **FR-1–FR-3** before ship.

Review-type weighting: `authoritative-review-literacy.md` §STUDY-TYPE + §ROUTING-1.

---

## Worked example (reference — do not build)

`/Users/dubs/Projects/piranesi.skill/research/llm-benchmark-routing/literature/`

## Piranesi boundary

Piranesi = fresh web packets. P9 = downloaded corpus teardown. `SYNTHESIS.md` may attach to ChatPRD S2 — not substitute for per-paper P9 ingests.

---

## Index / synthesizer dispatch (parent)

**Index writer:** read all `ingests/*_ingest.md` → index only, no new claims.

**Synthesizer:** read index + ingests → `SYNTHESIS.md` per schema above; test session bet if given.

Cross-links: `outside-input-ingest.md` (P8) · `agentic-research.md` (P7/9 index)
