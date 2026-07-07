from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, cast

ROOT = Path(__file__).resolve().parents[1]
SMOKE_EXAMPLE = ROOT / "examples" / "l6w_supervised_live_read_approval_no_live_smoke.py"
DOC = ROOT / "docs" / "l6w04-supervised-live-read-approval-no-live-smoke.md"
DOCS_INDEX = ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = ROOT / "docs" / "contract-test-inventory.md"

EXPECTED_COUNTERS = (
    "provider_callbacks",
    "backend_callbacks",
    "source_stat_callbacks",
    "source_read_callbacks",
    "write_callbacks",
    "custody_callbacks",
    "delete_callbacks",
    "reindex_callbacks",
    "rollback_callbacks",
    "cache_purge_callbacks",
    "credential_reads",
    "auth_reads",
    "env_reads",
    "keychain_reads",
    "oauth_reads",
    "auth_file_reads",
    "runtime_registry_consumptions",
    "source_discoveries",
    "workspace_scans",
    "family_scans",
    "broad_recall_queries",
    "index_queries",
    "live_private_reads",
    "source_stat_calls",
    "source_read_calls",
    "persistence_writes",
    "audit_record_writes",
    "custody_record_writes",
    "cache_mutations",
    "service_activations",
    "publication_actions",
    "visibility_changes",
    "provider_prod_canary_actions",
    "atlas_gate_movements",
    "mutation_executions",
)

UNSAFE_MARKERS = (
    "raw-secret-token",
    "credential-material",
    "operator-home-path",
    "platform-raw-id",
    "raw-query-payload",
    "raw-payload-content",
    "private-correlation-ref",
    "source://",
    "I approve Memory Seam",
    "requested_callback_family",
    "allowed=true",
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("l6w_supervised_live_read_approval_no_live_smoke", SMOKE_EXAMPLE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_l6w04_smoke_summary(summary: dict[str, object]) -> None:
    assert summary["smoke"] == "l6w_supervised_live_read_approval_no_live"
    assert summary["issue_ref"] == "#202"
    assert summary["approval_scaffold_issue_ref"] == "#199"
    assert summary["denial_matrix_issue_ref"] == "#200"
    assert summary["receipt_contract_issue_ref"] == "#201"
    assert summary["source_floor"] == "9264533"
    assert summary["upstream_packet"] == "docs/l6v06-supervised-source-card-trust-boundary-review.md"
    assert summary["operation_class"] == "SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ"
    assert summary["status"] == "HELD_FOR_FUTURE_APPROVAL"
    assert summary["approval_status"] == "NO_APPROVAL_PRESENT"
    assert summary["recognition_status"] == "NO_APPROVAL_RECOGNIZED"
    assert summary["stop_condition_status"] == "HELD_PENDING_FUTURE_ISSUE_BOUND_OWNER_APPROVAL"
    assert summary["stop_reason"] == "NO_APPROVAL_PRESENT"
    assert summary["operation_count"] == 0
    assert summary["max_operation_count"] == 1
    assert summary["one_operation_binding"] is True
    assert summary["descriptor_ref"] == "report-safe-descriptor-ref:l6w04-synthetic"
    assert summary["source_card_ref"] == "report-safe-source-card-ref:l6w04-synthetic"
    assert summary["metadata_only"] is True
    assert summary["stdout_only"] is True
    assert summary["non_persistent"] is True
    assert summary["allowed"] is False
    assert summary["allowed_result_count"] == 0
    assert summary["allowed_true_route_present"] is False
    assert summary["callbacks_invoked"] is False
    assert summary["live_read_invoked"] is False
    assert summary["live_adapter_invoked"] is False
    assert summary["source_discovery_attempted"] is False
    assert summary["runtime_registry_consumed"] is False
    assert summary["mutation_attempted"] is False
    assert summary["persistence_attempted"] is False
    assert summary["production_authority_claimed"] is False
    assert summary["guarded_counters_zero"] is True
    assert tuple(cast(Iterable[object], summary["denial_codes"])) == ("NO_APPROVAL_PRESENT",)
    assert summary["validation_errors"] == []

    counters = summary["counters"]
    assert isinstance(counters, dict)
    assert set(counters) == set(EXPECTED_COUNTERS)
    assert all(value == 0 for value in counters.values())


def test_l6w04_smoke_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6w04-supervised-live-read-approval-no-live-smoke.md" in docs_index
    assert "tests/test_l6w04_supervised_live_read_approval_no_live_smoke.py" in inventory
    assert "L6W.04 local no-live supervised live-read approval smoke" in inventory
    assert "LOCAL_SYNTHETIC_NO_LIVE_APPROVAL_SMOKE" in inventory


def test_l6w04_doc_records_no_live_no_callback_no_production_holds():
    text = normalized(DOC)

    for term in (
        "L6W.04 local no-live supervised live-read approval smoke",
        "Status: `LOCAL_SYNTHETIC_NO_LIVE_APPROVAL_SMOKE`",
        "Rail issue: #202",
        "Prerequisite: #201 closed/PASS",
        "Source floor: `9264533` or later on `origin/main`",
        "Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`",
        "examples/l6w_supervised_live_read_approval_no_live_smoke.py",
        "committed synthetic metadata only",
        "does not recognize approval, request approval, consume approval, or execute a live/private read",
        "stdout-only JSON",
        "`NO_APPROVAL_PRESENT`",
        "`NO_APPROVAL_RECOGNIZED`",
        "held before provider/backend/source-stat/source-read callbacks",
        "no source discovery, no Runtime Registry consumption, no persistence, no activation, no production authority, no Atlas Gate movement, no mutation execution, and no `allowed=true` route",
    ):
        assert term in text


def test_l6w04_smoke_summary_builds_one_held_synthetic_no_live_receipt():
    summary = load_smoke_module().build_report_safe_smoke_summary()

    assert_l6w04_smoke_summary(summary)


def test_l6w04_smoke_cli_emits_stdout_only_report_safe_json_with_zero_counters():
    completed = subprocess.run(
        [sys.executable, "examples/l6w_supervised_live_read_approval_no_live_smoke.py"],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    summary = json.loads(completed.stdout)
    assert completed.stderr == ""
    assert_l6w04_smoke_summary(summary)

    report_text = completed.stdout
    for unsafe_marker in UNSAFE_MARKERS:
        assert unsafe_marker not in report_text


def test_l6w04_smoke_counter_inventory_covers_held_live_read_surfaces():
    summary = load_smoke_module().build_report_safe_smoke_summary()
    counters = summary["counters"]

    assert summary["guarded_counters_zero"] is True
    for counter in EXPECTED_COUNTERS:
        assert counter in counters
        assert counters[counter] == 0
