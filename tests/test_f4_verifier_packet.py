from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "f4-verifier-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
NEGATIVE_MATRIX = REPO_ROOT / "tests" / "test_no_service_identity_negative_matrix.py"
SEMANTICS_NOTE = REPO_ROOT / "docs" / "no-service-identity-semantics.md"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_f4_verifier_packet_is_discoverable_from_indexes():
    packet_name = "f4-verifier-packet.md"

    assert PACKET.exists()
    assert packet_name in DOCS_INDEX.read_text(encoding="utf-8")
    assert packet_name in README.read_text(encoding="utf-8")
    assert "tests/test_f4_verifier_packet.py" in CONTRACT_TEST_INVENTORY.read_text(
        encoding="utf-8"
    )


def test_f4_verifier_packet_cites_issue_pr_test_and_doc_evidence():
    text = _normalized(PACKET)

    required_terms = [
        "F4 PASS",
        "#80",
        "#81",
        "#82",
        "#95",
        "#96",
        "f278146329f25182a7c2832963a255cd8d5dae00",
        "f50781ffe97659282be81733e892862f1f895cb9",
        "tests/test_no_service_identity_negative_matrix.py",
        "docs/no-service-identity-semantics.md",
        "GitHub `pytest (3.10)`, `pytest (3.11)`, and `pytest (3.12)` checks passed",
    ]
    for term in required_terms:
        assert term in text


def test_f4_verifier_packet_records_required_verifiers_and_focused_command():
    text = _normalized(PACKET)

    required_terms = [
        "pytest -q",
        "python scripts/public_hygiene_scan.py",
        "python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py",
        "git diff --check",
        "pytest -q tests/test_f4_verifier_packet.py",
        "local verifier plus GitHub CI before merge",
    ]
    for term in required_terms:
        assert term in text


def test_f4_verifier_packet_preserves_no_service_and_no_authority_boundaries():
    text = _normalized(PACKET)

    required_terms = [
        "No persistent listener or service has been started, installed, authorized, or required by F4",
        "does **not** authorize issue `#6`",
        "service/listener activation or installation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "global Hermes/MCP/client/runtime configuration mutation",
        "Runtime Registry runtime consumption",
        "live/private source reads or source discovery",
        "unsupervised reads",
        "writes/custody/reindex",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
        "production-authoritative claims",
        "F4 does **not** unlock F5 execution",
        "design-only packet",
    ]
    for term in required_terms:
        assert term in text


def test_f4_verifier_packet_proves_denial_before_read_evidence_and_safe_hygiene():
    text = _normalized(PACKET)
    matrix = _normalized(NEGATIVE_MATRIX)
    note = _normalized(SEMANTICS_NOTE)

    required_packet_terms = [
        "denied before provider/backend reads",
        "ReadSpyProvider",
        "provider.read_calls == 0",
        "zero source-read/stat/backend counter evidence",
        "forged subject",
        "wrong audience",
        "wrong scope",
        "expired token shape",
        "invalid token shape",
        "query/body agent mismatch",
        "query/body include mismatch",
        "confused-deputy worker recall",
        "service_started=false",
        "service_start_allowed=false",
        "runtime_registry_consumed=false",
        "audit_persisted=false",
        "write_custody_or_reindex=false",
    ]
    for term in required_packet_terms:
        assert term in text

    for term in [
        "ReadSpyProvider",
        "provider.read_calls == 0",
        "forged_subject",
        "wrong_audience",
        "wrong_scope",
        "expired_token_shape",
        "invalid_token_shape",
        "query_body_agent_mismatch",
        "query_body_include_mismatch",
        "confused_deputy_worker_recall",
    ]:
        assert term in matrix

    for term in [
        "before source/provider/file/stat/backend reads",
        "Public issue/PR artifacts must not include raw private source text",
        "private absolute paths",
        "raw query payloads",
    ]:
        assert term in note


def test_f4_verifier_packet_unlocks_only_f10_hygiene_prep():
    text = _normalized(PACKET)

    required_terms = [
        "Proceed to **`#83` F10.01: public/private hygiene inventory**",
        "#84",
        "#85",
        "F10 should stay hygiene/prep only",
        "must not change repository visibility",
        "publish a package",
        "expose private Atlas fixtures",
        "activate services/listeners",
        "consume Runtime Registry",
        "perform writes/custody/reindex",
        "move Atlas Gate status",
        "Issue `#6` remains open and held unless Jeremy explicitly unholds it",
    ]
    for term in required_terms:
        assert term in text
