from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6u01-supervised-live-use-adapter-wiring-map.md"
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

FORBIDDEN_BOUNDARY_ACTIONS = (
    "workspace scans",
    "family scans",
    "broad recall",
    "index queries",
    "source-stat calls",
    "source-read calls",
    "provider/backend callbacks",
    "Runtime Registry consumption",
)

GUARDED_ZERO_COUNTERS = (
    "provider_callback_count=0",
    "backend_callback_count=0",
    "source_stat_callback_count=0",
    "source_read_callback_count=0",
    "write_callback_count=0",
    "custody_callback_count=0",
    "delete_callback_count=0",
    "reindex_callback_count=0",
    "rollback_callback_count=0",
    "cache_purge_callback_count=0",
    "runtime_registry_consumption_count=0",
    "source_discovery_count=0",
    "allowed_result_count=0",
    "persistence_record_count=0",
    "activation_count=0",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6u01_adapter_wiring_map_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6u01-supervised-live-use-adapter-wiring-map.md" in docs_index
    assert "tests/test_l6u01_supervised_live_use_adapter_wiring_map.py" in inventory
    assert "L6U.01 supervised live-use adapter wiring map" in inventory
    assert "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF" in inventory


def test_l6u01_names_exactly_one_future_proof_target_shape():
    text = normalized(DOC)

    assert "Future proof target: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`." in text
    assert text.count("Future proof target:") == 1
    assert text.count("SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF") >= 2
    assert "one operator-approved, report-safe source-card/descriptor read-side proof" in text
    assert "only names the future target shape" in text
    assert "does not recognize any approval" in text


def test_l6u01_is_adapter_boundary_only_and_downstream_depends_on_core():
    text = normalized(DOC)

    required_terms = [
        "documentation and contract-test evidence only",
        "not approval, not a runtime adapter, not an activation path",
        "Memory Seam core remains standalone",
        "does not import Atlas Query, Hermes, provider backends, Runtime Registry clients, workspace scanners, source readers, source-stat helpers, or downstream adapter modules",
        "Any Atlas Query or Hermes adapter must live downstream and depend on Memory Seam contracts, not the reverse",
        "default-off until a later issue supplies explicit HITL approval",
        "Denial and HOLD decisions must happen before any provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callback family",
    ]
    for term in required_terms:
        assert term in text


def test_l6u01_allows_only_synthetic_report_safe_fixtures():
    text = normalized(DOC)

    required_fixture_terms = [
        "l6u01.synthetic.source-card.v1",
        "descriptor.synthetic.report-safe.v1",
        "caller.synthetic.operator-ref.v1",
        "receipt.synthetic.zero-callback-counters.v1",
        "metadata-only shapes",
        "safe source-card reference with title/classification/family labels and no body text",
        "disabled-by-default posture",
        "caller identity reference with subject/acting-for/audience/scope strings only",
        "all-zero counter fixture for guarded callback families",
    ]
    for term in required_fixture_terms:
        assert term in text

    assert "No fixture may include secrets, credentials, private paths, raw document content, raw prompt/query text, live source identifiers, OAuth/keychain/env material, or Runtime Registry references" in text


def test_l6u01_report_safe_shape_excludes_private_content_and_credentials():
    text = normalized(DOC)

    required_fields = [
        "source_card_ref",
        "descriptor_ref",
        "proof_target",
        "issue_ref",
        "caller_subject_ref",
        "acting_for_ref",
        "audience",
        "scope",
        "approval_ref",
        "expiry_ref",
        "guarded_callback_counters",
    ]
    for field in required_fields:
        assert field in text

    assert "excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw query/payload content, private correlation references, backend response bodies, and Runtime Registry data" in text
    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6u01_proves_no_live_no_source_discovery_no_runtime_registry():
    text = normalized(DOC)

    assert "without implementing or executing any live/private read" in text
    assert "does not select an actual private source" in text
    assert "read raw content" in text
    assert "discover sources" in text
    assert "query indexes" in text
    assert "perform broad recall" in text
    assert "consume Runtime Registry data" in text
    for action in FORBIDDEN_BOUNDARY_ACTIONS:
        assert action in text


def test_l6u01_guarded_callback_and_side_effect_counters_remain_zero():
    text = normalized(DOC)

    for counter in GUARDED_ZERO_COUNTERS:
        assert counter in text

    assert "all of these counters to remain zero" in text
    assert "unless a separate exact HITL-approved issue narrows one family" in text
    assert "no `allowed=true` path" in text
    assert "no persistence/audit/custody records" in text
    assert "no cache mutation" in text


def test_l6u01_preserves_production_activation_and_gate_holds():
    text = normalized(DOC)

    required_holds = [
        "no credentials, auth, env, keychain, OAuth, or auth-file reads",
        "no service/listener/startup/cron activation",
        "global Hermes/MCP/client/runtime config mutation",
        "package publication",
        "repository visibility change",
        "provider/prod/canary authority",
        "production authority",
        "Atlas Gate movement",
    ]
    for hold in required_holds:
        assert hold in text
