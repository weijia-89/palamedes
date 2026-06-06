#!/usr/bin/env python3
"""Build an HTML research index from a triage CSV + per-company research docs.

This is a generalized/parameterized version of `toren/docs/research_index_builder.py`,
kept here so research-index functionality lives with palamedes (the general
research/utilities home) rather than inside a specific downstream repo.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def extract_verdict(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"## 9\. Verdict.*?\n(.*?)\n## Sources", text, re.DOTALL)
    if m:
        return m.group(1).strip().replace("\n", " ")
    return ""


def find_research_file(company: str, research_dir: Path) -> Path | None:
    slug = company.lower().replace(" ", "-").replace(".", "-").replace("&", "and")
    md_path = research_dir / f"{slug}_research.md"
    if md_path.exists():
        return md_path
    for p in research_dir.glob("*_research.md"):
        if slug.replace("-", "") in p.stem.replace("-", "") or p.stem.replace("-", "") in slug.replace("-", ""):
            return p
    return None


def classify_verdict(verdict: str) -> str:
    v_clean = verdict.strip().lstrip("*").lstrip().lower()
    if v_clean.startswith("skip"):
        return "skip"
    if v_clean.startswith("apply"):
        return "apply"
    return "conditional"


def ils_class(ils: str) -> str:
    try:
        val = int(float(ils))
        if val >= 60:
            return "ils-high"
        if val < 45:
            return "ils-low"
        return "ils-mod"
    except Exception:
        return "ils-mod"


def build_row_html(r: dict[str, str]) -> str:
    v_class = classify_verdict(r["verdict"])
    ic = ils_class(r["ils"])
    jd_link = f'<a href="{r["job_url"]}" target="_blank" title="Job Description">📝</a>' if r.get("job_url") else ""
    dossier_link = f'<a href="{r["research_rel_path"]}" title="Research Dossier">📄</a>' if r.get("research_rel_path") else ""
    return f"""
        <tr>
          <td><span class="role">{r['company']}</span>{' ' + jd_link if jd_link else ''}<br><span class="sub">{r['title']}</span></td>
          <td>{r['location']}</td>
          <td class="{ic}" data-sort="{r['ils'] if r['ils'] != '—' else '-1'}">{r['ils']}</td>
          <td><span class="badge tier-tag">{r['tier']}</span></td>
          <td><span class="flag">{r['flags']}</span></td>
          <td>{r['comp']}</td>
          <td class="{v_class}">{r['verdict'][:140]}{'…' if len(r['verdict'])>140 else ''}</td>
          <td>{dossier_link}</td>
        </tr>
        """


def build_table(rows: list[dict[str, str]], table_id: str) -> str:
    if not rows:
        return '<p class="empty">No entries.</p>'
    body = "\n".join(build_row_html(r) for r in rows)
    return f"""<table class="sortable" id="{table_id}">
  <thead>
    <tr>
      <th>Company</th>
      <th>Location</th>
      <th class="sort-num" data-sort="ils">ILS ↕</th>
      <th>Tier</th>
      <th>Flags</th>
      <th>Comp</th>
      <th>Verdict</th>
      <th>Doc</th>
    </tr>
  </thead>
  <tbody>
    {body}
  </tbody>
</table>"""


def build_full_html(apply_rows: list[dict[str, str]], cond_rows: list[dict[str, str]], skip_rows: list[dict[str, str]]) -> str:
    style = """
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:13px;color:#302820;background:#e8e0d0;margin:0;padding:24px 32px;max-width:85rem;margin:0 auto;}
    h1{font-size:18px;color:#1a1208;margin-bottom:4px;}
    .meta{color:#5a4e44;font-size:11px;margin-bottom:28px;}
    h2{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:#486040;border-bottom:2px solid #486040;padding-bottom:4px;margin:28px 0 10px;}
    .section-skip h2{color:#8a2010;border-bottom-color:#c8a898;}
    .section-cond h2{color:#7a5010;border-bottom-color:#a89880;}
    table{width:100%;border-collapse:collapse;margin-bottom:16px;}
    th{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#5a4e44;border-bottom:1px solid #a89880;padding:5px 8px 5px 0;text-align:left;cursor:pointer;user-select:none;}
    th:hover{background:#d6cbb4;}
    th.sort-asc::after{content:" ▲";font-size:9px;}
    th.sort-desc::after{content:" ▼";font-size:9px;}
    td{padding:6px 8px 6px 0;border-bottom:1px solid #c8b8a0;vertical-align:top;line-height:1.45;font-size:12px;}
    tr:last-child td{border-bottom:none;}
    .role{font-weight:600;color:#1a1208;}
    .sub{font-size:11px;color:#5a4e44;}
    .ils-high{color:#2a5020;font-weight:700;}
    .ils-mod{color:#486040;font-weight:700;}
    .ils-low{color:#8a2010;font-weight:700;}
    .flag{color:#8a5c10;font-weight:600;}
    .skip{color:#8a2010;font-weight:600;}
    .apply{color:#2a5020;font-weight:600;}
    .conditional{color:#7a5010;font-weight:600;}
    a{color:#3a5a8a;text-decoration:none;}
    a:hover{text-decoration:underline;}
    .badge{display:inline-block;font-size:10px;font-weight:700;padding:1px 5px;border-radius:3px;margin-right:3px;background:#d2c5ac;}
    .tier-tag{background:#cdd8b8;color:#2a4020;}
    .empty{font-style:italic;color:#9a8c80;font-size:12px;margin:8px 0;}
    .count-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0 24px;max-width:420px;}
    .count-cell{background:#d8cfba;padding:8px 12px;border-radius:4px;font-size:12px;}
    .count-cell strong{display:block;font-size:16px;color:#1a1208;}
    .count-cell.apply-c strong{color:#2a5020;}
    .count-cell.skip-c strong{color:#8a2010;}
    .count-cell.cond-c strong{color:#7a5010;}
    """

    apply_table = build_table(apply_rows, "apply-table")
    cond_table = build_table(cond_rows, "cond-table")
    skip_table = build_table(skip_rows, "skip-table")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Research Index</title>
<style>{style}</style>
</head>
<body>
<h1>Research Index</h1>
<div class="meta">Generated by palamedes/scripts/build_research_index.py</div>

<div class="count-grid">
  <div class="count-cell apply-c"><strong>{len(apply_rows)}</strong> Apply</div>
  <div class="count-cell cond-c"><strong>{len(cond_rows)}</strong> Conditional</div>
  <div class="count-cell skip-c"><strong>{len(skip_rows)}</strong> Skip</div>
</div>

<div class="section-apply"><h2>Apply</h2>{apply_table}</div>
<div class="section-cond"><h2>Conditional</h2>{cond_table}</div>
<div class="section-skip"><h2>Skip</h2>{skip_table}</div>
</body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Build an HTML research index.")
    ap.add_argument("--triage-csv", type=Path, required=True)
    ap.add_argument("--research-dir", type=Path, required=True, help="Directory containing *_research.md files")
    ap.add_argument("--output-html", type=Path, required=True)
    args = ap.parse_args()

    triage = {}
    with args.triage_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            triage[row["company"]] = row

    rows: list[dict[str, str]] = []
    for company, data in triage.items():
        md_path = find_research_file(company, args.research_dir)
        verdict = extract_verdict(md_path) if md_path else ""
        comp_raw = f"{data.get('min_amount','')}–{data.get('max_amount','')}"
        comp = comp_raw.replace("nan–nan", "—").replace("–nan", "").replace("nan–", "")

        rows.append(
            {
                "company": company,
                "title": data.get("title", "—"),
                "location": data.get("location", "—") or "—",
                "ils": data.get("ils_estimate", data.get("ils_estimate", "—")) or "—",
                "tier": data.get("estimated_tier", "—") or "—",
                "flags": data.get("phase4_gate_flags", "—") or "—",
                "comp": comp,
                "verdict": verdict,
                "research_rel_path": md_path.as_posix() if md_path else "",
                "job_url": data.get("job_url", ""),
            }
        )

    def ils_key(r: dict[str, str]) -> float:
        try:
            return float(r["ils"])
        except Exception:
            return -1

    apply_rows = [r for r in rows if classify_verdict(r["verdict"]) == "apply"]
    cond_rows = [r for r in rows if classify_verdict(r["verdict"]) == "conditional"]
    skip_rows = [r for r in rows if classify_verdict(r["verdict"]) == "skip"]

    apply_rows.sort(key=ils_key, reverse=True)
    cond_rows.sort(key=ils_key, reverse=True)
    skip_rows.sort(key=ils_key, reverse=True)

    html = build_full_html(apply_rows, cond_rows, skip_rows)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")
    print(f"Wrote {args.output_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

