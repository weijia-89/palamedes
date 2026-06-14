# Source verifier batch prompt (Pattern 8 L2)

Use inside Task sub-sub-agent. Parent passes **1–5** primaries only.

```text
palamedes SRC-VERIFY · readonly · stakes={{STAKES}}

Verify these primaries independently of any external document that cited them.

## Batch (max 5)
{{SOURCE_BATCH_YAML}}

## Related doc claim ids
{{CLAIM_ID_LIST}}

## Deliver per source
One YAML file per source_id matching source-manifest.schema.md v1.1.

## Gates
- gate_a: fetch URL this session
- gate_b: in-source | not-in-source | ambiguous | unverifiable
- evidence_block_200: ≥200 chars from fetch, not from external doc

## Read-depth floor (L2+)
Operator viability / existence / magnitude claims require read:body.

FORBIDDEN: >5 sources · tag upgrades without in-source · canon edits
```
