from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from memory_seam.l5_post_read_verifier import (
    L5_POST_READ_VERIFIER_SCHEMA,
    L5_RECEIPT_SCHEMA,
    scan_public_hygiene,
    verify_l5_post_read_receipt,
    verify_l5_receipt_document,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = ROOT / "docs" / "l5-supervised-one-read-receipt.md"
SCRIPT_PATH = ROOT / "scripts" / "l5_post_read_verifier.py"
DOCS_INDEX_PATH = ROOT / "docs" / "README.md"
INVENTORY_PATH = ROOT / "docs" / "contract-test-inventory.md"


def _base_counters() -> dict[str, object]:
    return {
        "source_discovery_calls": 0,
        "raw_content_reads": 0,
        "credential_auth_env_keychain_authfile_reads": 0,
        "file_stat_calls": 0,
        "read_backend_calls": 0,
        "provider_calls": 0,
        "runtime_registry_consumed": False,
        "service_listener_cron_startup_activation": False,
        "global_config_mutation": False,
        "recurring_runner_activated": False,
        "provider_prod_canary_authority": False,
        "write_custody_or_reindex": False,
        "repository_visibility_or_publication_change": False,
        "atlas_gate_movement": False,
    }


def _receipt(**overrides: object) -> dict[str, object]:
    receipt: dict[str, object] = {
        "schema": L5_RECEIPT_SCHEMA,
        "decision": "PASS_ONE_SUPERVISED_METADATA_READ",
        "read_result": {
            "title": "L5 supervised source-grant decision packet",
            "document_kind": "decision_packet",
            "section_label": "one bounded supervised read target",
            "safe_summary": "Defines exactly one metadata-only project-document source-card read.",
            "freshness_label": "current_source_floor_after_20bb521",
            "redacted_source_card_id": "source-card-redacted-l5-105",
        },
        "usefulness_verdict": {
            "verdict": "useful",
            "task_answerable_from_safe_content": True,
            "reason_code": "safe_metadata_card_confirms_reachability_and_hold_posture",
        },
        "posture_counters": _base_counters(),
    }
    receipt.update(overrides)
    return receipt


def test_l5_06_verifier_reports_useful_without_additional_read():
    result = verify_l5_post_read_receipt(_receipt())

    assert result["schema"] == L5_POST_READ_VERIFIER_SCHEMA
    assert result["issue"] == "#106"
    assert result["verdict"] == "useful"
    assert result["task_answerable_from_safe_content"] is True
    assert result["reason_code"] == "safe_metadata_card_confirms_reachability_and_hold_posture"
    assert result["hygiene_passed"] is True
    assert result["posture_preserved"] is True
    assert result["no_additional_read_performed"] is True
    counters = result["posture_counters"]
    assert counters["source_discovery_calls"] == 0
    assert counters["file_stat_calls"] == 0
    assert counters["read_backend_calls"] == 0
    assert counters["provider_calls"] == 0
    assert counters["write_custody_or_reindex"] is False
    assert counters["atlas_gate_movement"] is False


def test_l5_06_verifier_classifies_too_redacted_fixture():
    result = verify_l5_post_read_receipt(
        _receipt(
            usefulness_verdict={
                "verdict": "too_redacted",
                "task_answerable_from_safe_content": False,
                "reason_code": "safe_content_too_redacted",
            },
            read_result={"safe_summary": "redacted"},
        )
    )

    assert result["verdict"] == "too_redacted"
    assert result["task_answerable_from_safe_content"] is False
    assert result["reason_code"] == "safe_content_too_redacted"
    assert result["hygiene_passed"] is True
    assert result["posture_preserved"] is True


def test_l5_06_verifier_classifies_denied_before_read_fixture():
    counters = _base_counters()
    counters["supervised_source_card_reads"] = 0

    result = verify_l5_post_read_receipt(
        _receipt(
            decision="DENY_BEFORE_READ",
            read_attempted=False,
            posture_counters=counters,
            usefulness_verdict={
                "verdict": "denied_before_read",
                "task_answerable_from_safe_content": False,
                "reason_code": "exact_approval_phrase_required",
            },
        )
    )

    assert result["verdict"] == "denied_before_read"
    assert result["reason_code"] == "receipt_denied_before_read"
    assert result["task_answerable_from_safe_content"] is False
    assert result["posture_preserved"] is True


def test_l5_06_verifier_classifies_degraded_backend_error_fixture():
    result = verify_l5_post_read_receipt(
        _receipt(
            decision="DEGRADED_BACKEND_ERROR",
            backend_error=True,
            usefulness_verdict={
                "verdict": "degraded_backend_error",
                "task_answerable_from_safe_content": False,
                "reason_code": "backend_failed",
            },
        )
    )

    assert result["verdict"] == "degraded_backend_error"
    assert result["reason_code"] == "receipt_backend_or_adapter_failed"
    assert result["task_answerable_from_safe_content"] is False
    assert result["hygiene_passed"] is True
    assert result["posture_preserved"] is True


def test_l5_06_verifier_fails_closed_on_public_private_hygiene_leak():
    private_path_shape = "/" + "Users" + "/" + "operator/private"
    result = verify_l5_post_read_receipt(_receipt(read_result={"safe_summary": f"see {private_path_shape}"}))

    assert result["verdict"] == "too_redacted"
    assert result["reason_code"] == "public_private_hygiene_failed"
    assert result["task_answerable_from_safe_content"] is False
    assert result["hygiene_passed"] is False
    assert "private_absolute_path" in result["hygiene_findings"]
    token_shape = "ghp_" + ("A" * 13)
    assert scan_public_hygiene({"token": token_shape}) == ("token_like",)


def test_l5_06_verifier_fails_closed_on_held_posture_movement():
    counters = _base_counters()
    counters["provider_calls"] = 1

    result = verify_l5_post_read_receipt(_receipt(posture_counters=counters))

    assert result["verdict"] == "degraded_backend_error"
    assert result["reason_code"] == "held_posture_counter_nonzero_or_true"
    assert result["task_answerable_from_safe_content"] is False
    assert result["posture_preserved"] is False


def test_l5_06_committed_receipt_doc_and_cli_are_report_safe():
    result = verify_l5_receipt_document(RECEIPT_PATH)

    assert result["verdict"] == "useful"
    assert result["hygiene_passed"] is True
    assert result["posture_preserved"] is True
    assert result["no_additional_read_performed"] is True

    cli = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--receipt", str(RECEIPT_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert '"verdict": "useful"' in cli.stdout
    assert '"no_additional_read_performed": true' in cli.stdout
    assert '"provider_calls": 0' in cli.stdout
    assert cli.stderr == ""


def test_l5_06_docs_and_inventory_are_discoverable():
    docs_index = DOCS_INDEX_PATH.read_text(encoding="utf-8")
    inventory = INVENTORY_PATH.read_text(encoding="utf-8")

    assert "l5-post-read-verifier.md" in docs_index
    assert "test_l5_post_read_verifier.py" in inventory
    assert "no additional reads" in inventory
