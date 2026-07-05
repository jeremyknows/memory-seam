from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "l6-positive-authorization-boundary-matrix.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

PRIVATE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6i08_packet_is_docs_tests_only_and_tied_to_frontier_source_truth():
    text = normalized(PACKET)

    required_terms = [
        "L6I.08 positive-authorization boundary matrix packet",
        "docs/tests-only preparation packet",
        "does not approve implementation",
        "does not unhold runtime behavior",
        "does not create any positive allowed runtime path",
        "Source floor: `7980a5b` or later `origin/main`",
        "SPLIT_AGAIN_DOCS_TESTS_ONLY",
        "Dependency: L6I.07 closed/PASS via issue `#149` and PR `#156`",
    ]
    for term in required_terms:
        assert term in text

    assert "I approve Memory Seam to implement" not in text


def test_l6i08_boundary_matrix_names_required_axes_without_runtime_unhold():
    text = normalized(PACKET)

    required_axes = [
        "Authorization result",
        "Operation class",
        "Source and provider access",
        "Runtime activation",
        "Receipt shape",
        "Callback counters",
        "Persistence",
    ]
    for axis in required_axes:
        assert axis in text

    held_terms = [
        "no positive allowed runtime path",
        "Any implementation path returning an allowed result",
        "Write execution",
        "custody transfer",
        "custody receipt persistence",
        "delete",
        "reindex",
        "rollback",
        "cache purge",
        "Provider/backend/source-stat/source-read callbacks",
        "live/private source reads",
        "source discovery",
        "credential/auth/keychain/env reads",
        "Runtime Registry consumption",
        "Service/listener/startup/cron activation",
        "canary authority",
        "production authority",
        "repository visibility changes",
        "package publication",
        "Atlas Gate movement",
        "Storage engines",
    ]
    for term in held_terms:
        assert term in text


def test_l6i08_future_approval_binding_is_specific_but_not_approval():
    text = normalized(PACKET)

    binding_terms = [
        "exact candidate operation class and non-goals",
        "exact future approval language, separated from documentation examples",
        "actor, subject, owner, approver, expiry, max-operation-count, and rollback/audit expectations",
        "explicit callback families that must remain at zero",
        "receipt fields that are report-safe and non-persistent",
        "public artifact hygiene rules",
        "Proceed to L6I.09 as docs/tests/schema-fixture work only",
        "non-persistent positive-authorization receipt shape fixture contract",
    ]
    for term in binding_terms:
        assert term in text


def test_l6i08_discoverability_and_contract_inventory_are_updated():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-positive-authorization-boundary-matrix.md" in docs_index
    assert "L6I.08 docs/tests-only positive-authorization boundary matrix" in docs_index
    assert "tests/test_l6i08_positive_authorization_boundary_matrix.py" in inventory
    assert "future approval request must bind before any positive-authorization implementation" in inventory


def test_l6i08_public_artifacts_remain_report_safe():
    combined = " ".join(
        normalized(path)
        for path in (PACKET, DOCS_INDEX, CONTRACT_TEST_INVENTORY)
    )

    allowed_public_terms = [
        "public issue numbers",
        "repository file names",
        "synthetic operation-class names",
        "boolean/counter facts",
        "safe status strings",
    ]
    for term in allowed_public_terms:
        assert term in combined

    forbidden_terms = [
        "private absolute paths",
        "OAuth/auth-file material",
    ]
    for term in forbidden_terms:
        assert term in combined

    for marker in PRIVATE_MARKERS:
        assert marker not in combined
