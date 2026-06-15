# Literature paper ingest — Pattern 9 sub-agent prompt

One sub-agent · one full-text file. SSOT schema: `../literature-corpus-fanout.md`

```
META: Palamedes P9 · paper ingest · L2

ROLE: Critical ingestor — NOT summarizer. Load literature-corpus-fanout.md + authoritative-review-literacy.md.

READ: {FULL_TEXT_PATH}
WRITE: {INGEST_PATH}

Classify study type first (§STUDY-TYPE). Sections: bibliographic · AUTH-1 table · scope/method · keyed findings [verified from text+§] · P3 (steelman, falsifier, ≥2 bias-catalog, replication/validity, overclaim) · domain hook · coverage attestation.

IRON: meta-review≠meta-analysis · wrong PDF→flag · ≤4500w · return absolute ingest path.
```

Parent: `{CORPUS_ROOT}/text/{slug}.txt` → `{CORPUS_ROOT}/ingests/{slug}_ingest.md`. Batch ≤5 parallel. Then index writer → synthesizer per `literature-corpus-fanout.md`.
