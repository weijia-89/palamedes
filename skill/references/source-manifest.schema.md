# source-manifest v1.1 (Pattern 7 SSOT)

Load when: per-source agent output or parent merge. Ops: `palamedes/scripts/p7_ops.py`.

```bash
python3 scripts/p7_ops.py count-primaries REFERENCES.md   # → primaries	N
python3 scripts/p7_ops.py should-fanout --stakes L3 --primaries N
python3 scripts/p7_ops.py verify sources/*/source-manifest.yaml  # mandatory before merge
python3 scripts/p7_ops.py merge sources/   # exit 1 → MODE-COLLAPSE-SUSPECT; re-dispatch sources
```

```yaml
manifest_version: 1.1
source_id: REFERENCES-row-id
url: "..."
tier: T1|T2|T3
read_depth: read:full|read:body|read:abstract
gate_a: ok|redirect|broken-url|paywall
gate_b: in-source|not-in-source|ambiguous|unverifiable
evidence_block_200: "..."   # ≥200 chars from fetch this session
claims:                     # max 25; this source only
  - id: C-001
    text: "..."
    extract: "..."          # ≤50w
    quotes:
      - qid: Q1
        excerpt: "..."      # ≤30w verbatim
        gate_b: in-source|not-in-source
    population_match: yes|no|unverifiable
    quote_status: verified|unverified|n/a
    effect_size: present|missing|n/a
    flags: []
gaps: []
```

**Fan-out if any:** L3+ ∧ primaries≥5 · Phase1 URLs≥3 · ingest≥8k tokens.  
**Skip:** L0–2 ≤4 primaries · T3-only · verified-this-session reuse · §5f · synthesizer reduce.  
**Dispatch:** N>3 → daily manifest (`trainer-dispatch-gates.md`). Dedupe by `source_id`. Verifier prompt only.
