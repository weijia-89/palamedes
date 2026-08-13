from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
CONTEXT = (ROOT / "context.md").read_text(encoding="utf-8")


def test_l3_behavior_rules_are_present_on_their_declared_surfaces() -> None:
    required_skill_phrases = (
        "Authority boundary (iron law)",
        "P1.5, Decompose (MECE + citation markers)",
        "Lossless condensation (P2 output discipline)",
        "Anti-no-op nudge (finish_empty_nudge)",
        "Protocol-conformance check (UP-B02)",
        "Schema-validate-then-repair (UP-B03)",
        "Anti-no-op continuation (UP-B08)",
    )
    for phrase in required_skill_phrases:
        assert phrase in SKILL
    context_flat = " ".join(CONTEXT.split())
    assert "Guardrails (budget, stop conditions, rigor floor) are engine state" in context_flat
    assert "The model cannot grant itself more budget" in context_flat
    assert "lower the rigor floor" in context_flat
    assert "skip a gate" in context_flat


def test_l3_context_keeps_piranesi_as_a_separate_export_only_surface() -> None:
    assert "Piranesi remains export-only" in CONTEXT
    assert "Piranesi counterpart work must preserve its" in CONTEXT
