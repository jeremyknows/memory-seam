from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "scripts" / "l5_supervised_one_read.py"
RECEIPT_PATH = ROOT / "docs" / "l5-supervised-one-read-receipt.md"
DOCS_INDEX_PATH = ROOT / "docs" / "README.md"
INVENTORY_PATH = ROOT / "docs" / "contract-test-inventory.md"


def _load_helper():
    spec = importlib.util.spec_from_file_location("l5_supervised_one_read", HELPER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_l5_05_denies_without_exact_approval_before_read():
    helper = _load_helper()

    exit_code, payload = helper.execute_issue_105_once(approval_phrase="Approved!")

    assert exit_code == 2
    assert payload["decision"] == "DENY_BEFORE_READ"
    assert payload["read_attempted"] is False
    counters = payload["posture_counters"]
    assert counters["supervised_source_card_reads"] == 0
    assert counters["source_discovery_calls"] == 0
    assert counters["raw_content_reads"] == 0
    assert counters["credential_auth_env_keychain_authfile_reads"] == 0
    assert counters["file_stat_calls"] == 0
    assert counters["read_backend_calls"] == 0
    assert counters["provider_calls"] == 0
    assert counters["write_custody_or_reindex"] is False
    assert counters["atlas_gate_movement"] is False


def test_l5_05_executes_exactly_one_metadata_card_read_with_zero_held_counters():
    helper = _load_helper()

    exit_code, payload = helper.execute_issue_105_once(approval_phrase=helper.APPROVAL_PHRASE)

    assert exit_code == 0
    assert payload["schema"] == "memory_seam_l5_supervised_one_read_receipt_v0"
    assert payload["decision"] == "PASS_ONE_SUPERVISED_METADATA_READ"
    assert payload["approval_provenance"] == "issue_105_comment_contains_exact_packet_phrase"
    assert payload["source_family"] == "operator_supplied_project_doc_card"
    assert payload["include_scope"] == (
        "title,document_kind,section_label,safe_summary,freshness_label,redacted_source_card_id"
    )
    assert set(payload["read_result"]) == {
        "title",
        "document_kind",
        "section_label",
        "safe_summary",
        "freshness_label",
        "redacted_source_card_id",
    }
    counters = payload["posture_counters"]
    assert counters["approval_phrase_matched"] is True
    assert counters["read_attempted"] is True
    assert counters["supervised_source_card_reads"] == 1
    assert counters["source_discovery_calls"] == 0
    assert counters["raw_content_reads"] == 0
    assert counters["credential_auth_env_keychain_authfile_reads"] == 0
    assert counters["file_stat_calls"] == 0
    assert counters["read_backend_calls"] == 0
    assert counters["provider_calls"] == 0
    assert counters["runtime_registry_consumed"] is False
    assert counters["service_listener_cron_startup_activation"] is False
    assert counters["global_config_mutation"] is False
    assert counters["recurring_runner_activated"] is False
    assert counters["provider_prod_canary_authority"] is False
    assert counters["write_custody_or_reindex"] is False
    assert counters["repository_visibility_or_publication_change"] is False
    assert counters["atlas_gate_movement"] is False
    assert payload["usefulness_verdict"]["verdict"] == "useful"
    assert payload["public_artifact_redaction_assertion"] == {
        "raw_private_source_text": False,
        "credentials_or_auth_material": False,
        "auth_env_keychain_material": False,
        "raw_platform_ids": False,
        "private_absolute_paths": False,
        "raw_query_payloads": False,
        "private_correlation_refs": False,
    }


def test_l5_05_cli_exec_receipt_outputs_public_safe_pass():
    helper = _load_helper()

    result = subprocess.run(
        [
            sys.executable,
            str(HELPER_PATH),
            "--issue-105-execute-approved-once",
            "--approval-phrase",
            helper.APPROVAL_PHRASE,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert '"decision": "PASS_ONE_SUPERVISED_METADATA_READ"' in result.stdout
    assert '"supervised_source_card_reads": 1' in result.stdout
    assert '"source_discovery_calls": 0' in result.stdout
    assert '"write_custody_or_reindex": false' in result.stdout
    assert "raw private source text" not in result.stdout.lower()
    assert result.stderr == ""


def test_l5_05_receipt_doc_and_inventory_preserve_public_boundaries():
    receipt = RECEIPT_PATH.read_text(encoding="utf-8")
    docs_index = DOCS_INDEX_PATH.read_text(encoding="utf-8")
    inventory = INVENTORY_PATH.read_text(encoding="utf-8")

    assert "PASS_ONE_SUPERVISED_METADATA_READ" in receipt
    assert "`supervised_source_card_reads` | `1`" in receipt
    for phrase in (
        "`source_discovery_calls` | `0`",
        "`raw_content_reads` | `0`",
        "`credential_auth_env_keychain_authfile_reads` | `0`",
        "`file_stat_calls` | `0`",
        "`read_backend_calls` | `0`",
        "`provider_calls` | `0`",
        "`write_custody_or_reindex` | `false`",
        "`atlas_gate_movement` | `false`",
        "no raw private source text, credentials, auth/env/keychain material, raw platform IDs",
    ):
        assert phrase in receipt
    assert "l5-supervised-one-read-receipt.md" in docs_index
    assert "test_l5_supervised_one_read_receipt.py" in inventory
