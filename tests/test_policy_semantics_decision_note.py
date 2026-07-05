from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTE = REPO_ROOT / "docs" / "policy-semantics-decision-note.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_policy_semantics_note_is_discoverable_from_indexes():
    note_name = "policy-semantics-decision-note.md"

    assert NOTE.exists()
    assert note_name in DOCS_INDEX.read_text(encoding="utf-8")
    assert note_name in README.read_text(encoding="utf-8")
    assert "tests/test_policy_semantics_decision_note.py" in CONTRACT_TEST_INVENTORY.read_text(
        encoding="utf-8"
    )


def test_policy_semantics_note_names_required_axes_and_intersection_decision():
    text = _normalized(NOTE)

    required_terms = [
        "fail-closed, no-live control-plane contract",
        "Subject",
        "Include family / scope",
        "Descriptor registration",
        "Grant / control-plane authority",
        "Receipt and source-floor labels",
        "Reportable reason hygiene",
        "descriptor registration and grant authority as an intersection, not a union",
        "A descriptor without a grant is not enough",
        "a grant without a descriptor is not enough",
        "an unknown family is not a prompt to discover a source",
        "a degraded provider is not permission to fall back to raw reads",
    ]
    for term in required_terms:
        assert term in text


def test_policy_semantics_note_preserves_denial_reason_and_zero_read_evidence_contract():
    text = _normalized(NOTE)

    required_terms = [
        "source_grant_missing",
        "source_grant_disabled",
        "unsupported_context_include",
        "unsupported_recall_scope",
        "provider-unconfigured degradation",
        "before source materialization",
        "zero provider/backend/read/stat calls",
        "equivalent spy/monkeypatch assertion",
        "public issue/PR artifacts",
        "must not include raw source text",
        "raw query payloads",
    ]
    for term in required_terms:
        assert term in text


def test_policy_semantics_note_keeps_held_surfaces_and_next_evidence_explicit():
    text = _normalized(NOTE)

    required_terms = [
        "service/listener activation or installation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "global Hermes, MCP, client, or runtime configuration mutation",
        "Runtime Registry runtime consumption",
        "live/private source reads or source discovery",
        "unsupervised reads, cron/startup activation, canaries",
        "provider/prod authority",
        "Atlas Gate movement",
        "writes, custody, reindex",
        "repository visibility changes",
        "package publication",
        "Issue `#6` remains held",
        "the verifier packet must collect local and CI evidence",
        "For F3, the next safe unlock requires the F2 verifier issue to close/PASS",
    ]
    for term in required_terms:
        assert term in text

    forbidden_terms = [
        "twine upload",
        "gh repo edit --visibility public",
        "crontab -e",
        "launchctl load",
        "Runtime Registry endpoint",
    ]
    for term in forbidden_terms:
        assert term not in text
