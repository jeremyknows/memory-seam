from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from memory_seam.positive_authorization_receipt import (
    L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS,
    L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS,
)

ROOT = Path(__file__).resolve().parents[1]
SMOKE_EXAMPLE = ROOT / "examples" / "l6_positive_authorization_no_production_smoke.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("l6_positive_authorization_no_production_smoke", SMOKE_EXAMPLE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_l6p04_smoke_summary(summary: dict[str, object]) -> None:
    assert summary["smoke"] == "l6_positive_authorization_no_production"
    assert summary["synthetic_no_production_only"] is True
    assert summary["status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
    assert summary["recognized_positive_authorization"] is True
    assert summary["operation_count"] == 1
    assert summary["max_operation_count"] == 1
    assert summary["allowed"] is False
    assert summary["mutation_attempted"] is False
    assert summary["mutation_supported"] is False
    assert summary["allowed_result_count"] == 0
    assert summary["persistent_counts_zero"] is True
    assert summary["guarded_counters_zero"] is True
    assert summary["callbacks_invoked"] is False
    assert summary["fixture_is_persistent"] is False
    assert summary["receipt_metadata_status"] == L6_POSITIVE_AUTHORIZATION_RECEIPT_STATUS
    assert summary["validation_errors"] == []


def test_l6p04_smoke_summary_reports_one_held_positive_authorization_without_callbacks():
    summary = load_smoke_module().build_report_safe_smoke_summary()

    assert_l6p04_smoke_summary(summary)



def test_l6p04_smoke_cli_emits_report_safe_stdout_only_summary():
    completed = subprocess.run(
        [sys.executable, "examples/l6_positive_authorization_no_production_smoke.py"],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    summary = json.loads(completed.stdout)
    assert completed.stderr == ""
    assert_l6p04_smoke_summary(summary)

    report_text = completed.stdout
    assert "I approve Memory Seam" not in report_text
    assert "This approval expires 24 hours after this comment" not in report_text
    assert "raw_payload" not in report_text
    assert "private_path" not in report_text
    assert "token_shaped_string" not in report_text



def test_l6p04_guarded_counter_inventory_includes_persistence_and_callback_holds():
    summary = load_smoke_module().build_report_safe_smoke_summary()

    assert summary["guarded_counters_zero"] is True
    assert summary["persistent_counts_zero"] is True
    assert "allowed_result_count" in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS
    for counter in (
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
        "persistent_receipt_count",
        "durable_write_record_count",
        "audit_persistence_count",
        "cache_mutation_count",
    ):
        assert counter in L6_POSITIVE_AUTHORIZATION_GUARDED_COUNTERS
