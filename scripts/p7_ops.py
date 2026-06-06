#!/usr/bin/env python3
"""Pattern 7 deterministic ops — no LLM. verify | merge | should-fanout | gate-a | count-primaries."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VALID_GATE_A = {"ok", "redirect", "broken-url", "paywall"}
VALID_GATE_B = {"in-source", "not-in-source", "ambiguous", "unverifiable"}
REQUIRED_TOP = (
    "manifest_version",
    "source_id",
    "url",
    "gate_a",
    "gate_b",
    "evidence_block_200",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _field(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


def _field_in(text: str, key: str) -> str | None:
    m = re.search(rf"{re.escape(key)}:\s*(\S+)", text)
    return m.group(1).strip().strip('"').strip("'") if m else None


def _claim_count(text: str) -> int:
    return len(re.findall(r"^\s{2}- id:\s", text, re.M))


def cmd_verify(paths: list[Path]) -> int:
    errs: list[str] = []
    for path in paths:
        if not path.is_file():
            errs.append(f"{path}: missing")
            continue
        text = _read(path)
        for req in REQUIRED_TOP:
            if f"{req}:" not in text:
                errs.append(f"{path}: missing {req}")
        ver = _field(text, "manifest_version")
        if ver and ver != "1.1":
            errs.append(f"{path}: manifest_version must be 1.1")
        ga = _field(text, "gate_a")
        if ga and ga not in VALID_GATE_A:
            errs.append(f"{path}: bad gate_a {ga!r}")
        gb = _field(text, "gate_b")
        if gb and gb not in VALID_GATE_B:
            errs.append(f"{path}: bad gate_b {gb!r}")
        ev = _field(text, "evidence_block_200")
        if ev is not None and len(ev) < 200:
            errs.append(f"{path}: evidence_block_200 len {len(ev)} < 200")
        n = _claim_count(text)
        if n > 25:
            errs.append(f"{path}: {n} claims > 25")
    if errs:
        for e in errs:
            print(f"FAIL  {e}", file=sys.stderr)
        return 1
    print(f"PASS  verify ({len(paths)} manifest(s))")
    return 0


def cmd_merge(sources_dir: Path) -> int:
    files = sorted(sources_dir.glob("*/source-manifest.yaml"))
    if not files:
        print(f"FAIL  no manifests under {sources_dir}", file=sys.stderr)
        return 1
    rows: list[tuple[str, str, str, str, str]] = []
    blocks: list[str] = []
    for f in files:
        text = _read(f)
        sid = _field(text, "source_id") or f.parent.name
        ga = _field(text, "gate_a") or "?"
        gb = _field(text, "gate_b") or "?"
        ev = _field(text, "evidence_block_200") or ""
        blocks.append(ev[:80])
        for m in re.finditer(
            r"^\s{2}- id:\s(\S+).*?(?=^\s{2}- id:|\Z)", text, re.M | re.S
        ):
            chunk = m.group(0)
            cid = m.group(1)
            pop = _field_in(chunk, "population_match") or "?"
            qs = _field_in(chunk, "quote_status") or "?"
            es = _field_in(chunk, "effect_size") or "?"
            rows.append((sid, cid, ga, gb, f"{pop}|{qs}|{es}|{ev[:80]}"))
    collapse = False
    if blocks:
        from collections import Counter

        top = Counter(b[:40] for b in blocks if b).most_common(1)
        if top and top[0][1] > len(blocks) / 2:
            collapse = True
    print("source_id\tclaim_id\tgate_a\tgate_b\tpop|quote|fx|ev80")
    for r in rows:
        print("\t".join(r))
    if collapse:
        print("FAIL  MODE-COLLAPSE-SUSPECT (>50% manifests share evidence_block prefix)", file=sys.stderr)
        print(f"merge\t{len(files)} manifests, {len(rows)} claims, collapse=yes", file=sys.stderr)
        return 1
    print(f"PASS  merge ({len(files)} manifests, {len(rows)} claims)", file=sys.stderr)
    return 0


def cmd_count_primaries(refs: Path, tiers: set[str]) -> int:
    if not refs.is_file():
        print(f"FAIL  missing {refs}", file=sys.stderr)
        return 1
    text = _read(refs)
    current: str | None = None
    n = 0
    for line in text.splitlines():
        m = re.match(r"^## (T[123]),", line)
        if m:
            current = m.group(1)
            continue
        if current not in tiers:
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 3 or cells[1] in ("Tag", ""):
            continue
        n += 1
    print(f"primaries\t{n}")
    return 0


def cmd_should_fanout(stakes: str, primaries: int, phase1_urls: int) -> int:
    level = int(stakes[1]) if stakes.upper().startswith("L") and stakes[1:].isdigit() else 0
    yes = (level >= 3 and primaries >= 5) or phase1_urls >= 3
    print("fanout\tyes" if yes else "fanout\tno")
    return 0


def cmd_gate_a(url: str, timeout: int) -> int:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "palamedes-p7/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
    except urllib.error.HTTPError as e:
        print(f"gate_a\tbroken-url\t{e.code}")
        return 1
    except OSError as e:
        print(f"gate_a\tbroken-url\t{e}")
        return 1
    get = urllib.request.Request(url, headers={"User-Agent": "palamedes-p7/1.0"})
    with urllib.request.urlopen(get, timeout=timeout) as resp:
        body = resp.read(4096).decode("utf-8", errors="replace")
    block = body[:200].replace("\n", " ")
    print(f"gate_a\tok\t{code}")
    print(f"evidence_block_200\t{block}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Pattern 7 deterministic ops")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="validate source-manifest.yaml")
    v.add_argument("paths", nargs="+", type=Path)

    m = sub.add_parser("merge", help="TSV phase-1 log + collapse flag")
    m.add_argument("sources_dir", type=Path)

    s = sub.add_parser("should-fanout", help="emit fanout\tyes|no")
    s.add_argument("--stakes", default="L2")
    s.add_argument("--primaries", type=int, default=0)
    s.add_argument("--phase1-urls", type=int, default=0)

    c = sub.add_parser("count-primaries", help="count T1/T2 rows in REFERENCES.md")
    c.add_argument("references", type=Path, nargs="?", default=Path("REFERENCES.md"))
    c.add_argument("--tiers", default="T1,T2", help="comma tiers, default T1,T2")

    g = sub.add_parser("gate-a", help="HTTP check + first 200 chars")
    g.add_argument("url")
    g.add_argument("--timeout", type=int, default=30)

    args = p.parse_args()
    if args.cmd == "verify":
        return cmd_verify(args.paths)
    if args.cmd == "merge":
        return cmd_merge(args.sources_dir)
    if args.cmd == "should-fanout":
        return cmd_should_fanout(args.stakes, args.primaries, args.phase1_urls)
    if args.cmd == "count-primaries":
        tiers = {t.strip().upper() for t in args.tiers.split(",") if t.strip()}
        return cmd_count_primaries(args.references, tiers)
    if args.cmd == "gate-a":
        return cmd_gate_a(args.url, args.timeout)
    return 2


if __name__ == "__main__":
    sys.exit(main())
