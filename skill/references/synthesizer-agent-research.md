# Palamedes research — synthesizer agent design

```
palamedes v3 engaged · type=synthetic · stakes=L3 · budget=web-fetch+priors
```

**Question:** How should a **synthesizer agent** merge multi-lane research without context rot?

**Pre-registered prediction:** Structured reduce-stage manifests outperform prose mega-paste; synthesizer must not retrieve or debate. **Confidence:** 0.75. **Falsifier:** A/B shows prose synthesis matches manifest fidelity on quote retention.

---

## 1. Numbered quotes (external this session)

### S1 — LLM×MapReduce (ACL 2025)

- **URL:** https://aclanthology.org/2025.acl-long.1341v2.pdf  
- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE]

> **Q1:** "The disrupted long-range information can be divided into two categories: inter-chunk dependency and inter-chunk conflict."

> **Q2:** "If the mapped results are overly simplified, as seen in LongAgent (Zhao et al., 2024), crucial details needed for subsequent stages may be lost. On the other hand, if the mapped results are too complex, they introduce significant computational overhead."

> **Q3:** Structured map output includes "Extracted Information", "Rationale", "Answer", and "Confidence Score: a score (out of 5) reflecting the model's confidence in the answer" for "resolving inter-chunk conflicts."

### S2 — Co-Sight (arXiv 2510.21557)

- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE]

> **Q4:** "CAMV optimizes the verification process by concentrating computational resources on minimal conflict sets" rather than "re-verifying entire reasoning chains."

> **Q5:** "TRSF continuously organizes, validates, and synchronizes evidence across agents" as "source-verified, traceable information."

> **Q6:** "Co-Sight reconceptualizes debate as a detection process" — verification layer, not end-to-end solver.

### S3 — Huang et al. (2023) intrinsic self-correction

- **URL:** https://arxiv.org/html/2310.01798  
- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE]

> **Q7:** "LLMs struggle to self-correct their reasoning in this setting. In most instances, the performance after self-correction even deteriorates."

> **Q8:** Improvements in prior self-correction work "result from using oracle labels to guide the self-correction process, and the improvements vanish when oracle labels are not available."

### S4 — EligMeta (arXiv 2604.02678)

- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE]

> **Q9:** "Directly generating executable code from natural-language rules often leads to brittle implementations" — intermediate structured plan "separates information extraction from logical evaluation."

### S5 — DeepEvidence (arXiv 2601.11560)

- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE]

> **Q10:** "explicit evidence graph as a first-class memory structure" with "provenance from primary literature" — "Rather than encoding context as free text."

### S6 — Chain-of-Agents (NeurIPS 2024)

- **Gate A:** 200 OK · **Gate B:** [CLAIM IN SOURCE] [read:abstract+methods skim]

> **Q11:** Worker agents pass communication units; manager aggregates — "multi-step worker communication" expands effective context via collaboration not single-window paste.

---

## 2. Load-bearing claims

| ID | Claim | Tag | Conf. |
|----|-------|-----|-------|
| R-001 | Reduce-stage needs **structured protocol**, not prose summaries | [verified] | 70 — S1 Q2–Q3 |
| R-002 | Merge must handle **dependency** and **conflict** as distinct problems | [verified] | 70 — S1 Q1 |
| R-003 | Verification should target **conflict hotspots**, not full re-read | [verified] | 65 — S2 Q4,Q6 |
| R-004 | Shared substrate = **traceable facts module**, not chat history | [verified] | 65 — S2 Q5, S5 Q10 |
| R-005 | Synthesizer must **not** rely on intrinsic self-correction | [verified] | 70 — S3 Q7–Q8 |
| R-006 | Synthesizer must **not** retrieve (map/upstream owns evidence) | [inferred] | 60 — R-001+R-005: reduce without new map pollutes provenance |
| R-007 | Per-claim **confidence scores** enable conflict resolution at merge | [verified] | 65 — S1 Q3 |
| R-008 | Manifest too sparse → information loss; too dense → rot/latency | [verified] | 70 — S1 Q2 |
| R-009 | Debate belongs in **adversarial pre-pass**, not synthesizer merge | [inferred] | 55 — S2 Q6 + palamedes agentic Huang note |
| R-010 | External verifier (scripts, human) required for tag upgrades | [inferred] | 60 — S3 Q8 + engram verify_theory_canon pattern |

---

## 3. Design synthesis (evidence-backed)

### Optimal role graph

```
MAP (Producers)     → lane-manifest.yaml     [Extract + quotes + rationale + confidence]
CHECK (Adversarial) → challenge-manifest.yaml [CAMV: conflict hotspots only]
REDUCE (Synthesizer)→ synthesis-manifest.yaml [No retrieval; merge + canon_ops]
VERIFY (Parent)     → scripts + human        [External oracle — not LLM self-grade]
```

This mirrors **LLM×MapReduce** (map/collapse/reduce) + **Co-Sight** (TRSF facts + CAMV) + **Huang** (no intrinsic fixup).

### Schema upgrades (v1.1 recommended)

Add to each producer claim (from S1 Q3):

```yaml
extract: "..."       # ≤50w factual pull from source
rationale: "..."     # ≤40w inference chain (not new facts)
confidence_1_5: 1-5  # merge-time conflict resolution
```

Synthesizer outputs `merge_decision` per conflict pair: `prefer_a | prefer_b | unresolved | downgrade_both`.

### Token budget (from S1 Q2)

| Artifact | Target |
|----------|--------|
| lane-manifest | ≤4k tokens / lane |
| challenge-manifest | ≤2k tokens |
| synthesizer ingest | ≤12k tokens total |
| synthesis.md | ≤800 words |

### When synthesizer fails → escalate to Parent, not self-fix

Per S3: if `gaps_remaining` blocks merge, Parent either (a) re-runs one producer, or (b) authorizes one bounded retrieval pass — **not** synthesizer freelancing.

---

## 4. Hostile objections

**O1:** "YAML manifests are bureaucracy."  
Response: S1 Q2 shows oversimplified summaries lose details; S4 Q9 shows end-to-end prose→action is brittle. Bureaucracy is the structured protocol.

**O2:** "Just use multi-agent debate."  
Response: S2 Q6 + Huang — debate as merge operator fails without asymmetry; adversarial challenges claim ids, synthesizer does not debate.

**O3:** "One smart model with 1M context."  
Response: S1 Q1 — long-range dependency/conflict still appears across sections; monolithic context exhibits lost-in-the-middle [priors-only: Liu et al. 2023 — not body-read this session].

---

## 5. Kill list (design options rejected)

| Option | Verdict | Reason |
|--------|---------|--------|
| Synthesizer runs web search by default | **WRONG** | Breaks provenance chain (R-006) |
| Synthesizer upgrades tags to verified | **WRONG** | Intrinsic self-correction pattern (S3) |
| Single mega-summary instead of manifests | **WRONG** | S1 Q2 LongAgent information loss |
| Synthesizer = Prosecutor/Defender/Judge | **OVERSTATED** | Merge ≠ debate (S2 Q6) |
| Skip adversarial wave | **OVERSTATED** | CAMV cost savings need conflict id first (S2 Q4) |

---

## 6. Implementation checklist (palamedes + engram)

- [ ] Bump `lane-manifest` to v1.1 (extract, rationale, confidence_1_5)
- [ ] Adversarial outputs `severity: kill` only with qid or explicit none
- [ ] Synthesizer emits `unresolved_conflicts` — never silent pick
- [ ] Parent runs deterministic verifier post-merge
- [ ] Piranesi Packet SYN forbids retrieval (already)
- [ ] Eval: 10 snippet corpus with gold lens sets + manifest fidelity metric

---

## 7. Sources

| ID | Citation | Tier | Read |
|----|----------|------|------|
| S1 | LLM×MapReduce, ACL 2025 | T1 | body |
| S2 | Co-Sight, arXiv:2510.21557 | T2 | abstract+intro |
| S3 | Huang et al., arXiv:2310.01798 | T1 | body |
| S4 | EligMeta, arXiv:2604.02678 | T2 | body skim |
| S5 | DeepEvidence, arXiv:2601.11560 | T2 | body skim |
| S6 | Chain-of-Agents, NeurIPS 2024 | T1 | abstract |

---

## 8. Self-instrument check

- Retrieval coverage: S1,S3 body; S2,S4,S5 skim — **partial**
- Many-analyst caveat: **single analyst** — confidence capped on R-009, R-010
- Sycophancy: flagged on "manifests are always worth it" — mitigated by S1 Q2 tradeoff

**Next:** Piranesi greenfield packet + schema v1.1 patch to `synthesizer-agent.md`.
