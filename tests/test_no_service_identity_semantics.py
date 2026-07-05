from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTE = REPO_ROOT / "docs" / "no-service-identity-semantics.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
NEGATIVE_MATRIX = REPO_ROOT / "tests" / "test_no_service_identity_negative_matrix.py"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_no_service_identity_semantics_note_is_discoverable_from_indexes():
    note_name = "no-service-identity-semantics.md"

    assert NOTE.exists()
    assert note_name in DOCS_INDEX.read_text(encoding="utf-8")
    assert note_name in README.read_text(encoding="utf-8")
    assert "tests/test_no_service_identity_semantics.py" in CONTRACT_TEST_INVENTORY.read_text(
        encoding="utf-8"
    )


def test_no_service_identity_semantics_note_names_required_identity_axes():
    text = _normalized(NOTE)

    required_terms = [
        "in-process, no-service authority contract",
        "Caller subject",
        "Acting-for",
        "Audience / scope",
        "Descriptor subject",
        "Query/body subject mismatch",
        "request body, query parameters, ambient process identity, or caller assertions cannot create this subject",
        "acting-for metadata may be recorded in metadata-only audit receipts, but it does not grant source access",
        "Descriptor presence is not identity proof",
        "query/body agreement as an intersection, not a union",
    ]
    for term in required_terms:
        assert term in text


def test_no_service_identity_semantics_note_states_can_and_cannot_prove_boundaries():
    text = _normalized(NOTE)

    required_terms = [
        "forged subject",
        "wrong audience",
        "wrong scope",
        "expired/invalid token shape",
        "query/body mismatch",
        "confused-deputy worker-vs-interactive paths deny before provider/backend reads",
        "service_started=false",
        "runtime_registry_consumed=false",
        "audit_persisted=false",
        "write_custody_or_reindex=false",
        "real credential, keychain, OAuth, auth-file, environment-secret, or external identity-provider verification",
        "persistent service/listener activation",
        "Runtime Registry runtime consumption",
        "global Hermes, MCP, client, or runtime configuration mutation",
        "live/private source reads",
        "writes, custody, reindex",
        "repository visibility changes",
        "Atlas Gate movement",
        "Issue `#6` remains held",
    ]
    for term in required_terms:
        assert term in text


def test_no_service_identity_semantics_preserves_denial_before_read_and_reportable_hygiene():
    text = _normalized(NOTE)

    required_terms = [
        "before source/provider/file/stat/backend reads",
        "zero source-read/stat/backend counters",
        "provider spies",
        "equivalent assertions",
        "Public issue/PR artifacts must not include raw private source text",
        "credentials",
        "auth/env/keychain material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "private correlation references",
        "tests/test_no_service_identity_negative_matrix.py",
        "The F4 verifier packet should collect the merged F4 issue/PR/test/doc evidence",
        "no persistent listener/service boundary",
    ]
    for term in required_terms:
        assert term in text


def test_no_service_identity_negative_matrix_contains_zero_read_spy_evidence():
    matrix = _normalized(NEGATIVE_MATRIX)

    required_terms = [
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
        "service_started",
        "runtime_registry_consumed",
        "audit_persisted",
        "write_custody_or_reindex",
    ]
    for term in required_terms:
        assert term in matrix

    forbidden_terms = [
        "launchctl load",
        "crontab -e",
        "twine upload",
        "gh repo edit --visibility public",
        "Runtime Registry endpoint",
    ]
    for term in forbidden_terms:
        assert term not in text if (text := _normalized(NOTE)) else False
