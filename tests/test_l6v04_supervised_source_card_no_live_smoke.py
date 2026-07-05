from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from memory_seam.supervised_source_card_preflight import (
    L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS,
    L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS,
    L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS,
)

ROOT = Path(__file__).resolve().parents[1]
SMOKE_EXAMPLE = ROOT / "examples" / "l6v_supervised_source_card_no_live_smoke.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("l6v_supervised_source_card_no_live_smoke", SMOKE_EXAMPLE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_l6v04_smoke_summary(summary: dict[str, object]) -> None:
    assert summary["smoke"] == "l6v_supervised_source_card_no_live"
    assert summary["issue_ref"] == "#190"
    assert summary["preflight_issue_ref"] == "#187"
    assert summary["source_floor"] == "876375b"
    assert summary["upstream_packet"] == "docs/l6u05-supervised-live-use-trust-boundary-review.md"
    assert summary["operation_class"] == L6V_SUPERVISED_SOURCE_CARD_OPERATION_CLASS
    assert summary["status"] == L6V_SUPERVISED_SOURCE_CARD_PREFLIGHT_STATUS
    assert summary["status_detail"] == "ready_metadata_only_preflight"
    assert summary["recognized_operation"] is True
    assert summary["preflight_ready"] is True
    assert summary["operation_count"] == 1
    assert summary["max_operation_count"] == 1
    assert summary["descriptor_ref"] == "synthetic_descriptor:l6v-report-safe-project-doc-v1"
    assert summary["source_card_ref"] == "synthetic_source_card:l6v-report-safe-project-doc-v1"
    assert summary["metadata_only"] is True
    assert summary["non_persistent"] is True
    assert summary["allowed"] is False
    assert summary["allowed_result_count"] == 0
    assert summary["allowed_true_route_present"] is False
    assert summary["callbacks_invoked"] is False
    assert summary["live_adapter_invoked"] is False
    assert summary["mutation_attempted"] is False
    assert summary["persistence_attempted"] is False
    assert summary["guarded_counters_zero"] is True
    approval_denial_codes = summary["approval_denial_codes"]
    assert isinstance(approval_denial_codes, tuple | list)
    assert tuple(approval_denial_codes) == ()
    assert summary["validation_errors"] == []

    counters = summary["counters"]
    assert isinstance(counters, dict)
    assert set(counters) == set(L6V_SUPERVISED_SOURCE_CARD_GUARDED_COUNTERS)
    assert all(value == 0 for value in counters.values())


def test_l6v04_smoke_summary_runs_one_recognized_synthetic_no_live_preflight():
    summary = load_smoke_module().build_report_safe_smoke_summary()

    assert_l6v04_smoke_summary(summary)


def test_l6v04_smoke_cli_emits_stdout_only_report_safe_json_with_zero_counters():
    completed = subprocess.run(
        [sys.executable, "examples/l6v_supervised_source_card_no_live_smoke.py"],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    summary = json.loads(completed.stdout)
    assert completed.stderr == ""
    assert_l6v04_smoke_summary(summary)

    report_text = completed.stdout
    for unsafe_marker in (
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
    ):
        assert unsafe_marker not in report_text


def test_l6v04_smoke_counter_inventory_covers_held_source_callback_persistence_surfaces():
    summary = load_smoke_module().build_report_safe_smoke_summary()
    counters = summary["counters"]

    assert summary["guarded_counters_zero"] is True
    for counter in (
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
        "persistence_writes",
        "audit_record_writes",
        "custody_record_writes",
        "cache_mutations",
        "service_activations",
        "publication_actions",
        "visibility_changes",
        "atlas_gate_movements",
    ):
        assert counter in counters
        assert counters[counter] == 0
