#!/usr/bin/env python3
"""Deterministic tests for Pattern 7 source-manifest operations."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scripts import p7_ops


def _manifest(evidence: str = "e" * 220, *, gate_a: str = "ok", gate_b: str = "in-source", claims: str = "") -> str:
    return (
        "manifest_version: 1.1\n"
        "source_id: source-a\n"
        "url: https://example.test/source\n"
        f"gate_a: {gate_a}\n"
        f"gate_b: {gate_b}\n"
        f"evidence_block_200: {evidence}\n"
        f"{claims}"
    )


def test_verify_accepts_valid_manifest(tmp_path: Path) -> None:
    path = tmp_path / "source-manifest.yaml"
    path.write_text(_manifest(), encoding="utf-8")
    assert p7_ops.cmd_verify([path]) == 0


def test_verify_rejects_bad_gate_and_short_evidence(tmp_path: Path) -> None:
    path = tmp_path / "source-manifest.yaml"
    path.write_text(_manifest("short", gate_a="bogus"), encoding="utf-8")
    err = StringIO()
    with redirect_stderr(err):
        assert p7_ops.cmd_verify([path]) == 1
    assert "bad gate_a" in err.getvalue()
    assert "evidence_block_200" in err.getvalue()


def test_verify_rejects_missing_manifest(tmp_path: Path) -> None:
    err = StringIO()
    with redirect_stderr(err):
        assert p7_ops.cmd_verify([tmp_path / "missing.yaml"]) == 1
    assert "missing" in err.getvalue()


def test_merge_emits_claim_rows_without_collapse(tmp_path: Path) -> None:
    for name, evidence in (("a", "a" * 220), ("b", "b" * 220)):
        directory = tmp_path / name
        directory.mkdir()
        directory.joinpath("source-manifest.yaml").write_text(
            _manifest(evidence, claims="  - id: C-001\n    population_match: exact\n    quote_status: quoted\n    effect_size: none\n"),
            encoding="utf-8",
        )
    out = StringIO()
    err = StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        assert p7_ops.cmd_merge(tmp_path) == 0
    assert "source_id\tclaim_id" in out.getvalue()
    assert "PASS  merge (2 manifests, 2 claims)" in err.getvalue()


def test_merge_rejects_mode_collapse(tmp_path: Path) -> None:
    evidence = "same evidence block " * 20
    for name in ("a", "b", "c"):
        directory = tmp_path / name
        directory.mkdir()
        directory.joinpath("source-manifest.yaml").write_text(
            _manifest(evidence), encoding="utf-8"
        )
    err = StringIO()
    with redirect_stderr(err):
        assert p7_ops.cmd_merge(tmp_path) == 1
    assert "MODE-COLLAPSE-SUSPECT" in err.getvalue()


def test_count_primaries_counts_selected_tiers(tmp_path: Path) -> None:
    refs = tmp_path / "REFERENCES.md"
    refs.write_text(
        "## T1, primary\n| ID | Title | URL |\n|---|---|---|\n| A | A | https://a.test |\n"
        "## T3, tertiary\n| ID | Title | URL |\n|---|---|---|\n| B | B | https://b.test |\n",
        encoding="utf-8",
    )
    out = StringIO()
    with redirect_stdout(out):
        assert p7_ops.cmd_count_primaries(refs, {"T1", "T2"}) == 0
    assert "primaries\t1" in out.getvalue()


def test_should_fanout_covers_stakes_and_url_thresholds(capsys) -> None:
    assert p7_ops.cmd_should_fanout("L3", 5, 0) == 0
    assert "fanout\tyes" in capsys.readouterr().out
    assert p7_ops.cmd_should_fanout("L2", 4, 0) == 0
    assert "fanout\tno" in capsys.readouterr().out
    assert p7_ops.cmd_should_fanout("L1", 0, 3) == 0
    assert "fanout\tyes" in capsys.readouterr().out


def test_gate_a_reads_status_and_first_200_chars() -> None:
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def getcode(self):
            return 200

        def read(self, size):
            return b"body" * 100

    out = StringIO()
    with patch("scripts.p7_ops.urllib.request.urlopen", return_value=Response()), redirect_stdout(out):
        assert p7_ops.cmd_gate_a("https://example.test", 1) == 0
    assert "gate_a\tok\t200" in out.getvalue()
    assert "evidence_block_200\t" in out.getvalue()


def test_gate_a_returns_failure_when_body_fetch_fails() -> None:
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def getcode(self):
            return 200

    out = StringIO()
    with patch(
        "scripts.p7_ops.urllib.request.urlopen",
        side_effect=[Response(), OSError("body fetch failed")],
    ), redirect_stdout(out):
        assert p7_ops.cmd_gate_a("https://example.test", 1) == 1
    assert "gate_a\tbroken-url\tbody fetch failed" in out.getvalue()
