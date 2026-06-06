# Palamedes synthesizer agent — spec & best practices

Load when: final synthesis risks **context rot** (multi-lane research, 75+ canon entries, ChatPRD packet 3 output, tisarwat-scale merges).

**Evidence base:** `synthesizer-agent-research.md` (MapReduce structured reduce, Co-Sight CAMV/TRSF, Huang intrinsic self-correction limits).

**Problem:** Producers dump unbounded prose; parent agent loses quote fidelity, duplicates claims, and invents bridges.

**Solution:** **Synthesizer** = **reduce-stage only** with strict manifest ingest. Maps to LLM×MapReduce `freduce`; does not map or retrieve.

---

## Role separation (four hats)

| Hat | Retrieval? | Input | Output |
|-----|------------|-------|--------|
| **Producer (map)** | Yes (independent per lane) | PIR / lane charter | `lane-manifest.yaml` |
| **Adversarial (CAMV)** | Optional light | Producer manifest(s) | `challenge-manifest.yaml` |
| **Synthesizer (reduce)** | **No** (default) | Manifests only | `synthesis-manifest.yaml` + ≤800w `synthesis.md` |
| **Parent / Judge (verify)** | No | Synthesis manifest + scripts | Final artifacts |

Synthesizer is **not** Prosecutor/Defender/Judge (`agentic-research.md` Pattern 2). Debate detects conflicts **before** merge (Co-Sight: "debate as detection process"). Synthesizer **merges tagged claims**.

**Huang rule:** Synthesizer must not intrinsically self-correct tags or quotes — external adversarial + parent verifier only.

---

## When to invoke

| Trigger | Pattern |
|---------|---------|
| ≥2 independent producer lanes | Wave fan-out → synthesizer |
| ≥5 load-bearing primaries | Pattern 7 → `source-manifest.schema.md` + `scripts/p7_ops.py` |
| Ingest budget ≤1200 tokens downstream (tisarwat, engram) | Mandatory synthesizer |
| Stakes L3+ and single analyst >8k tokens of notes | Mandatory synthesizer |
| Inter-lane dependency OR conflict expected | Structured manifest required |
| One-lane L1 answer | Skip synthesizer; parent P4 only |

---

## Input contract — `source-manifest.yaml`

See `source-manifest.schema.md`. Merge with `p7_ops.py merge`.

## Input contract — `lane-manifest.yaml` (v1.1)

```yaml
manifest_version: 1.1
lane: soc | psy | crt | custom
producer_id: soc-greenfield-1
stakes: L2
claims:
  - id: soc-C-001
    text: "..."
    extract: "..."
    rationale: "..."
    tag: verified | inferred | speculative | unknown
    confidence_1_5: 1-5
    quotes:
      - qid: Q1
        source_url: "..."
        excerpt: "..."
        gate_a: ok | abstract-only | broken-url
        gate_b: in-source | not-in-source | ambiguous
    falsifier: "..."
    depends_on: []
gaps: []
killed: []
```

**Producer limits:** max 25 claims/lane; max 3 quotes/claim; ≤4k tokens/manifest.

---

## Input contract — `challenge-manifest.yaml`

```yaml
manifest_version: 1.1
reviewer: adversarial-unified
challenges:
  - target: soc-C-004
    objection: "..."
    proposed_tag: speculative
    evidence_qid: Q12 | none
    severity: kill | downgrade | note
conflicts:
  - a: soc-C-002
    b: psy-C-011
    type: dependency | contradiction
    note: "..."
```

---

## Synthesizer output — `synthesis-manifest.yaml`

```yaml
manifest_version: 1.1
synthesizer_id: syn-1
ingested: []
merged_claims: []
superseded: []
merge_decisions: []
unresolved_conflicts: []
canon_ops: []
gaps_remaining: []
downstream_budget:
  tokens_estimate: 950
  mvp_subset: []
```

Plus **`synthesis.md`** (≤800w).

---

## Synthesizer iron laws

1. **No retrieval** unless `gaps_remaining` + parent `synthesizer_retrieval: allow`.
2. **No new claim ids** or quotes.
3. **No tag upgrades** (Huang intrinsic self-correction failure).
4. **Dedupe** by mechanism + author + falsifier hash.
5. **Conflicts:** `confidence_1_5` + adversarial severity; else `unresolved`.
6. **Budget:** >50 `canon_ops` → `mvp_subset`.
7. **Failure:** Parent re-runs producer — no synthesizer self-fix loop.

---

## Wave graph

```
Wave 0: Producers (parallel)
Wave 1: Adversarial (CAMV)
Wave 2: Synthesizer (reduce)
Wave 3: Parent Judge (external verifier)
```

---

## References

| Doc | Purpose |
|-----|---------|
| `synthesizer-agent-research.md` | Palamedes evidence pass |
| `piranesi/packets-synthesizer-agent-research.md` | ChatPRD R-SYN + R-SYN-ADV |
| `packets-palamedes-synthesizer-dispatch.md` | Operational dispatch |
