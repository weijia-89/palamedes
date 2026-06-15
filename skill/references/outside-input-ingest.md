# Outside-input ingest — Pattern 8 (document → source-verify ladder)

Load when: operator drops **external artifacts** (Opus/ChatPRD returns, Downloads paths, pasted adversarial reviews, lane manifests, PDF excerpts) that must be **synthesized into canon** without parent monolithic merge.

**SSOT for:** Piranesi export **return path**, engram research W2 ingest, theory-canon merges, any "merge N external documents" task.

**Composes with:** Pattern 7 (`agentic-research.md`) · Pattern 9 (`literature-corpus-fanout.md` — when corpus is papers, not external returns) · `synthesizer-agent.md` · `source-manifest.schema.md` · `scripts/p7_ops.py`

---

## Problem

Parent agent that reads 6–12 external documents in one context:

- Loses quote fidelity and claim ids
- Treats external `[verified]` tags as ground truth (LLM cargo-cult)
- Skips primary-source fetch because the document *already cited* a URL
- Collapses mode when all docs share the same T3 monoculture (e.g. one practitioner blog)

**Fix:** **One sub-agent per document** → **sub-sub-agents per 1–5 primaries** → adversarial → synthesizer reduce → parent judge.

---

## When to invoke (mandatory)

| Trigger | Pattern |
|---------|---------|
| ≥2 external documents to merge | Pattern 8 |
| Single document but ≥5 distinct cited primaries on load-bearing claims | Pattern 8 |
| Piranesi/Opus session outputs saved as files | Pattern 8 return path |
| ≥3 peer-reviewed PDFs / full-text papers to synthesize | **Pattern 9** (`literature-corpus-fanout.md`) — not Pattern 8 |
| Systematic reviews / meta-analyses corpus + index | **Pattern 9** + `authoritative-review-literacy.md` |
| Stakes L2+ and external doc asserts operator viability | Pattern 8 |
| Fresh in-session retrieval only, no external docs | Pattern 7 only |
| One-lane L1 summary of one paste | Parent P4; skip fan-out |

**Piranesi rule:** Piranesi **exports** packets; it does **not** ingest returns. On artifact drop → **Palamedes Pattern 8** (this doc).

---

## Agent ladder (four levels)

```
Parent orchestrator
├── Document ingestor ×N          (1 sub-agent per external document)
│   ├── Source verifier ×⌈P/5⌉   (sub-sub-agents; 1–5 primaries each)
│   └── doc-manifest-{id}.yaml
├── Adversarial ×1 or ×N          (optional per doc; mandatory L3+)
├── Synthesizer ×1                (reduce only; no retrieval)
└── Parent judge                  (apply canon_ops / playbook patches)
```

| Level | Role | Retrieval? | Input | Output |
|-------|------|------------|-------|--------|
| **L0 Parent** | Dispatch, merge gates, apply patches | No | `dispatch-manifest.yaml` + synthesis output | Patched canon + `SIGNOFF.md` |
| **L1 Document ingestor** | Extract claims, cite list, normalize YAML | No | One file path or paste | `doc-manifest-{id}.yaml` |
| **L2 Source verifier** | Fetch primaries; Gate A/B | **Yes** | 1–5 `source_id` batch from L1 | `sources/{doc_id}/{source_id}.yaml` |
| **L3 Adversarial** | Challenge claim ids | Light (falsify only) | `doc-manifest-*.yaml` | `challenge-manifest.yaml` |
| **L4 Synthesizer** | Dedupe merge | **No** | All manifests | `synthesis-manifest.yaml` + `synthesis.md` |

**Hard caps**

- **1–5 primaries per source-verifier sub-sub-agent** (never 6+ in one agent)
- **25 claims max** per `doc-manifest`
- **3 quotes max** per claim in doc manifest
- Document ingestor **must not** upgrade tags using only in-document citations — upgrades require L2 `gate_b: in-source`

---

## Wave graph

```yaml
# dispatch-manifest.yaml (parent writes first)
case: {case-slug}
stakes: L3
outside_input: true
waves:
  - phase: ingest
    agents: [doc-ingestor-{id}, ...]   # parallel per document
    parallel: true
  - phase: verify
    agents: [source-verifier-{doc}-{batch}, ...]
    parallel: true
    consumes: [doc-ingestor-*]
    batch_size: 1-5                    # primaries per sub-sub-agent
  - phase: adversarial
    agents: [adversarial-unified]
    parallel: false
    consumes: [doc-ingestor-*, source-verifier-*]
  - phase: synthesize
    agents: [synthesizer-main]
    parallel: false
    consumes: [doc-ingestor-*, challenge-manifest]
  - phase: judge
    agents: [parent-judge]
    parallel: false
    consumes: [synthesizer-main]
synthesizer_retrieval: deny
token_budget:
  synthesizer_ingest_max: 12000
```

**Gate before synthesizer:** `python3 palamedes/scripts/p7_ops.py verify sources/*/*.yaml` — all must pass. Any fail → re-dispatch that batch only.

**Gate before judge:** `python3 palamedes/scripts/p7_ops.py merge sources/{doc_id}/` per document; exit 1 → `MODE-COLLAPSE-SUSPECT` → re-dispatch verifiers with **independent fetch** (different tool or query).

---

## L1 — Document ingestor contract (`doc-manifest-{id}.yaml`)

```yaml
manifest_version: 1.1
doc_id: lane-operator-grammar-adversarial
source_path: "~/Downloads/Adversarial Review_ lane-operator-grammar manifest.md"
producer: external-opus-4.6
ingest_date: YYYY-MM-DD
claims:
  - id: doc-C-001
    text: "Parentheses grouping works on Google"
    extract: "..."
    tag: user-asserted          # max until L2 verifies
    confidence_1_5: 3
    cited_primaries:
      - source_id: russell-google-search-2024
        url: "https://..."
        tier: T1
        as_cited_by_doc: "quoted in adversarial §2"
    falsifier: "..."
    depends_on: []
primaries_to_verify:            # deduped union of cited_primaries
  - source_id: russell-google-search-2024
    url: "https://..."
    tier: T1
    claim_ids: [doc-C-001, doc-C-004]
gaps: []
killed_in_doc: []               # if input IS adversarial review, import kill list
```

**Document ingestor iron laws**

1. **No web search** — only structure what the document contains.
2. **No tag upgrades** — external `verified` → `user-asserted` until L2 confirms.
3. **Emit `primaries_to_verify`** — dedupe URLs; split list into batches of 1–5 for L2 dispatch.
4. If input is already `lane-manifest.yaml` / fenced YAML → validate schema; do not prose-summarize.
5. If input is markdown essay → extract ≤25 load-bearing claims; drop uncited fluff.

---

## L2 — Source verifier contract (sub-sub-agent)

**Prompt skeleton:** `references/prompts/source-verifier-batch.md` (or inline in dispatch packet).

Per batch of 1–5 primaries from one document:

1. Fetch each URL (`web-fetch` / `Read` / `curl` — record tool in manifest).
2. Emit one `source-manifest.yaml` per `source_id` per `source-manifest.schema.md`.
3. `evidence_block_200` ≥200 chars from **this session's** fetch — not from external doc paste.
4. `gate_a`: ok | redirect | broken-url | paywall
5. `gate_b`: in-source | not-in-source | ambiguous | unverifiable
6. Map which `doc-C-*` claims each source supports or falsifies.

**Sub-sub-agent iron laws**

- **Read body** for any magnitude/operator/existence claim at L2+ (`read:body` floor).
- **1–5 sources only** — if batch has 6, parent splits before dispatch.
- **Readonly** recommended — verifiers do not edit canon.
- T3-only support for a load-bearing claim → doc claim stays `inferred` max at L3.

---

## Tag promotion rules (after L2)

| Before L2 | After `gate_b: in-source` + read-depth floor | After `gate_b: not-in-source` |
|-----------|-----------------------------------------------|-------------------------------|
| `user-asserted` | `verified` or `inferred` per read depth | `killed` or `speculative` |
| external `verified` | Re-tag from fetch; may **downgrade** | **kill** claim id |
| `inferred` | May stay or upgrade with body evidence | downgrade or kill |

Synthesizer **never** promotes tags — only merges L1+L2+adversarial manifests.

---

## 2-pass piranesi ingest handling

When an external document is a Piranesi/ChatPRD `*_ingest.md` with **2-PASS GENERATION** markers:

- **PASS 2 (formatted)** content is canonical for structured extraction, claim ids, and canon_ops.
- **PASS 1 (freeform)** is context only — do not treat as final schema shape.
- Document ingestor must record `pass_boundary: detected` in doc-manifest when markers present.

---

## L3 — Adversarial on outside input

Same as `challenge-manifest.yaml` in `synthesizer-agent.md`, with extra checks:

- **T3 monoculture:** if >50% primaries are one author/blog → `severity: downgrade` on all uncorroborated claims
- **Cargo-cult operators:** claim cites help page but L2 `gate_b: not-in-source` → `severity: kill`
- **Cross-doc contradiction:** same operator, conflicting tags → `conflicts[]` unresolved

Minimum challenges: `max(15, 2 × doc_count)`.

---

## Parent context budget (anti-rot)

Parent holds **only:**

- `dispatch-manifest.yaml`
- Per-doc: `doc-manifest-{id}.yaml` (not raw Downloads files)
- `challenge-manifest.yaml`
- `synthesis-manifest.yaml` + `synthesis.md`
- `canon_ops` / `patch_list` diff

Parent **does not** load: raw adversarial prose, full lane-manifest essays, or verifier fetch bodies.

---

## Operator routing table

| Step | Agent type | Tool |
|------|------------|------|
| Inventory paths | Parent | local shell / glob |
| Per document | L1 Document ingestor | Task `generalPurpose` or `explore` |
| Per 1–5 primaries | L2 Source verifier | Task `generalPurpose` **readonly:true** |
| Verify manifests | Parent | `p7_ops.py verify` |
| Attack claims | L3 Adversarial | Task or Opus paste |
| Merge | L4 Synthesizer | Task or Opus paste |
| Apply | L0 Parent judge | local edits |

**Parallelism:** All L1 in parallel; all L2 batches in parallel **after** their L1 completes; L3–L4 sequential.

---

## Falsifiers (pattern failed if…)

- Parent read all external docs inline and shipped synthesis without L2 fetch.
- One verifier agent received >5 primaries.
- External `verified` tags survived without `gate_b: in-source` in source manifest.
- Synthesizer ran web search or upgraded tags.
- `p7_ops.py verify` skipped before synthesizer.

---

## Related packets

- `engram.skill/references/research/packets/packets-palamedes-synthesizer-dispatch.md` — PACKET OUTSIDE-INGEST, PACKET DOC-INGEST, PACKET SRC-VERIFY
- `piranesi/SKILL.md` — Return path → Pattern 8
