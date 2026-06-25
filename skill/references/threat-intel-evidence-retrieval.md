# Threat-intel evidence retrieval

Load when: CVE, incident, malware, APT, vuln disclosure, IOC, or security-advisory questions at L2+.

## Source hierarchy

| Tier | Source types | T-tag guidance |
|------|--------------|----------------|
| T1 | Vendor advisory with CVE ID; NVD/CVE record; CISA KEV entry; MITRE ATT&CK technique page; original IR report with IOCs | `[T1-verified, read:body]` for severity/exploitability claims |
| T2 | Reputable IR firm report linking primaries; CERT/CC; national CSIRT with named authors | `[T2-verified]`; upgrade to T1 when primary fetched |
| T3 | Anonymous paste; forum IOC dumps; unverified "0-day" tweets | `[user-asserted]`; never `[T*-verified]` |

## CISA AIS veracity ladder (5-level) [inferred mapping to T-tags]

Map AIS/confidence-style labels to Palamedes tags — **not proven equivalence**:

| AIS-style level | Palamedes handling |
|-----------------|-------------------|
| Confirmed / Firmed | Eligible for `[T1-verified]` after body read of linked primary |
| Probable | `[T2-verified]` max until primary retrieved |
| Possible | `[inferred:basis]`; name basis |
| Doubtful | `[contested]` or `[unknown]` |
| Unverified | `[user-asserted]` or `[priors-only]` |

## Retrieval protocol

1. **CVE or advisory ID first** — then vendor bulletin, then NVD metadata (metadata alone ≠ verified exploit chain).
2. **Version scope:** affected versions, fixed versions, workaround — `read:body` on advisory for L2+ magnitude claims.
3. **Second independent source** for L3+ (e.g., vendor + CISA, or two independent IR writeups with distinct primaries).
4. **IOC freshness:** IP/domain hashes decay fast; tag `[stale:<date>]` when past 30-day window for active-threat claims.

## FR mapping

- First opened advisory cannot be sole support for "actively exploited in production" — need KEV or second corroboration (FR-1).
- Contradicting vendor vs researcher claims → FR-2 Contradiction block.

## Cross-links

- `source-grading.md`
- `llm-failure-modes.md` — fabricated CVE/advisory checks
