# Calibration scenarios

Frozen research runs used to regression-test the palamedes skill against real outputs: wrong citations, tier laundering, and “looks rigorous” formatting without proof.

| ID | Scenario | Report |
| --- | --- | --- |
| `manus-vs-palamedes-datadog-2026-06-04` | Same L2 public-company brief; Cursor+palamedes vs Manus (free-form + same Palamedes prompt) | [`report.md`](./manus-vs-palamedes-datadog-2026-06-04/report.md) |

## How to use

1. Read the scenario `README.md` for scope and pass criteria.
2. Run `prompt.md` in a **new** agent session (do not open `artifacts/` first if reproducing the blind Cursor arm).
3. Diff your output against `artifacts/` and the case-study `report.md`.
4. Optional: add a row to [`skill/references/failure-log.md`](../skill/references/failure-log.md) if you find a new failure mode.

Scenarios are **not** part of the browser UI or merge gates. They document epistemic discipline under fire, not product features.
