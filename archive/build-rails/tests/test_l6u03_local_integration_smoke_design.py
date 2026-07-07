from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6u03-local-integration-smoke-design.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"

OPERATION_CLASS = "SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF"

ZERO_COUNTERS = (
    "source_discovery_count",
    "runtime_registry_consumption_count",
    "provider_callback_count",
    "backend_callback_count",
    "source_stat_callback_count",
    "source_read_callback_count",
    "write_callback_count",
    "custody_callback_count",
    "delete_callback_count",
    "reindex_callback_count",
    "rollback_callback_count",
    "cache_purge_callback_count",
    "persistence_record_count",
    "cache_mutation_count",
    "service_activation_count",
)

PUBLIC_FIELDS = (
    "status",
    "operation_class",
    "fixture_id",
    "source_card_ref",
    "descriptor_ref",
    "caller_subject_ref",
    "acting_for_ref",
    "local_only",
    "synthetic_fixture_only",
    "default_off",
    "live_adapter_invoked",
    "guarded_callback_counters",
    "unsupported_behavior",
    "public_hygiene_result",
)

FORBIDDEN_HELD_SURFACES = (
    "no implementation or execution of live/private reads",
    "no credentials, auth, env, keychain, OAuth, or auth-file reads",
    "no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption",
    "no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks",
    "no mutation execution, no `allowed=true` path",
    "no persistence/audit/custody records",
    "no cache mutation",
    "no service/listener/startup/cron activation",
    "no global Hermes/MCP/client/runtime config mutation",
    "no package publication",
    "no repository visibility change",
    "no provider/prod/canary authority",
    "no production authority",
    "no Atlas Gate movement",
)

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


def test_l6u03_smoke_design_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6u03-local-integration-smoke-design.md" in docs_index
    assert "tests/test_l6u03_local_integration_smoke_design.py" in inventory
    assert "L6U.03 local integration smoke design" in inventory
    assert OPERATION_CLASS in inventory


def test_l6u03_is_docs_tests_only_default_off_and_not_implementation():
    text = normalized(DOC)

    required_terms = [
        "Status: `LOCAL_ONLY_SYNTHETIC_SMOKE_DESIGN_NOT_IMPLEMENTATION`",
        "documentation and contract-test evidence only",
        "does not implement an adapter",
        "does not implement an adapter, execute a live/private read",
        "default-off and non-executable",
        "not a live-read proof",
        "not approval to connect to private sources",
    ]
    for term in required_terms:
        assert term in text


def test_l6u03_names_exactly_one_future_target_and_synthetic_fixture_family():
    text = normalized(DOC)

    assert f"Future smoke target: `{OPERATION_CLASS}`." in text
    assert text.count("Future smoke target:") == 1
    assert "exactly one future proof target and exactly one local smoke operation" in text
    assert "Allowed future fixture family: `tests/fixtures/l6u03_synthetic_source_card_read_smoke.json`." in text
    assert "committed synthetic fixture data" in text


def test_l6u03_smoke_flow_is_local_only_synthetic_only_no_live_no_registry():
    text = normalized(DOC)

    required_terms = [
        "Load the committed synthetic fixture by repository-relative path only",
        "Validate `synthetic_fixture_only=true`, `local_only=true`, `default_off=true`, and `live_adapter_invoked=false`",
        "Validate all source discovery and Runtime Registry counters are zero before any adapter import boundary is touched",
        "Produce a stdout-only public-safe smoke summary",
        "Exit with `HOLD_NO_LIVE_ADAPTER`",
        "No step may perform a live/private read, source discovery, workspace scan, family scan, broad recall, index query, source-stat call, source-read call, provider/backend callback, Runtime Registry lookup",
    ]
    for term in required_terms:
        assert term in text


def test_l6u03_public_stdout_shape_is_report_safe_and_excludes_private_content():
    text = normalized(DOC)

    for field in PUBLIC_FIELDS:
        assert f"`{field}`" in text

    required_exclusions = [
        "must not echo raw prompts, raw source content, private paths, source URIs, credentials",
        "env values, OAuth material, keychain material, auth-file content",
        "raw backend responses, Runtime Registry references, audit/custody bodies, persistence bodies, or private correlation references",
        "excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw prompt/query text, raw payload content, private correlation references",
    ]
    for term in required_exclusions:
        assert term in text

    for marker in PRIVATE_MARKERS:
        assert marker not in text


def test_l6u03_zero_counters_and_no_callbacks_are_required():
    text = normalized(DOC)

    for counter in ZERO_COUNTERS:
        assert f"`{counter}`" in text

    assert "Any non-zero guarded counter is a HOLD before callbacks and before any live adapter invocation." in text
    assert "all guarded callback families fixed at zero" in text
    assert "callback counters remain zero" in text
    assert "no provider callbacks" in text
    assert "no source-read callbacks or live/private reads" in text


def test_l6u03_keeps_write_custody_delete_reindex_rollback_cache_purge_unsupported():
    text = normalized(DOC)

    assert "`write/custody/delete/reindex/rollback/cache-purge` as unsupported behavior" in text
    assert "write/custody/delete/reindex/rollback/cache-purge behavior" in text
    assert "before callbacks, persistence, cache mutation, or mutation execution" in text
    assert "It must never produce an `allowed=true` path." in text


def test_l6u03_proves_no_live_adapter_invocation():
    text = normalized(DOC)

    assert "Required sentinel: `live_adapter_invoked=false`." in text
    assert "The smoke design proves local import/wiring only." in text
    assert "If a future implementation attempts to invoke a live adapter" in text
    assert "the smoke must stop with HOLD and must not continue" in text


def test_l6u03_preserves_no_live_no_callback_no_production_holds():
    text = normalized(DOC)

    for surface in FORBIDDEN_HELD_SURFACES:
        assert surface in text

    assert "no Runtime Registry consumption" in text
    assert "no service/listener/startup/cron activation" in text
    assert "no package publication" in text
    assert "no provider/prod/canary authority" in text
    assert "no Atlas Gate movement" in text
