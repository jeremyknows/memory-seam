from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "scripts" / "l5_supervised_one_read.py"
RUNBOOK_PATH = ROOT / "docs" / "l5-supervised-one-read-runbook.md"
PACKET_PATH = ROOT / "docs" / "l5-supervised-source-grant-packet.md"


def _load_helper():
    spec = importlib.util.spec_from_file_location("l5_supervised_one_read", HELPER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_l5_04_dry_run_plan_is_default_no_exec_and_names_one_supervised_path():
    helper = _load_helper()

    exit_code, payload = helper.evaluate_request(execute=False, approval_phrase=None)

    assert exit_code == 0
    assert payload["decision"] == "DRY_RUN_NO_EXEC"
    assert payload["execution_requested"] is False
    plan = payload["plan"]
    assert plan["source_family"] == "operator_supplied_project_doc_card"
    assert plan["subject_shape"] == "one operator-supplied Memory Seam project-document source card"
    assert plan["include_scope"] == (
        "title,document_kind,section_label,safe_summary,freshness_label,redacted_source_card_id"
    )
    assert plan["timeout_seconds"] == 30
    assert plan["redaction_posture"] == "report-safe metadata only; no raw private text or identifiers"
    assert plan["receipt_target"] == "docs/l5-supervised-one-read-receipt.md (future #105 artifact only)"
    assert "exact approval phrase absent or altered" in plan["stop_conditions"]
    assert "stop without retrying" in plan["rollback"]


def test_l5_04_helper_denies_execute_without_exact_packet_phrase_before_read():
    helper = _load_helper()

    exit_code, payload = helper.evaluate_request(execute=True, approval_phrase="almost approved")

    assert exit_code == 2
    assert payload["decision"] == "DENY_BEFORE_READ"
    assert payload["reason"] == "exact_approval_phrase_required"
    assert payload["approval_phrase_matched"] is False
    plan = payload["plan"]
    assert plan["provider_calls"] == 0
    assert plan["source_read_calls"] == 0
    assert plan["file_stat_calls"] == 0
    assert plan["read_backend_calls"] == 0
    assert plan["credential_auth_env_keychain_authfile_reads"] is False
    assert plan["runtime_registry_consumed"] is False
    assert plan["global_config_mutation"] is False
    assert plan["service_listener_cron_startup_activation"] is False
    assert plan["write_custody_or_reindex"] is False


def test_l5_04_exact_phrase_preflight_remains_no_read_until_105_executes():
    helper = _load_helper()

    exit_code, payload = helper.evaluate_request(execute=True, approval_phrase=helper.APPROVAL_PHRASE)

    assert exit_code == 2
    assert payload["decision"] == "APPROVAL_MATCHED_BUT_EXECUTION_HELD_FOR_105"
    assert payload["approval_phrase_matched"] is True
    assert payload["read_attempted"] is False
    plan = payload["plan"]
    assert plan["next_execution_issue"] == "#105"
    assert plan["no_source_discovery"] is True
    assert plan["no_source_read"] is True
    assert plan["source_read_calls"] == 0
    assert plan["file_stat_calls"] == 0
    assert plan["read_backend_calls"] == 0


def test_l5_04_cli_dry_run_outputs_public_safe_no_live_plan():
    result = subprocess.run(
        [sys.executable, str(HELPER_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert '"decision": "DRY_RUN_NO_EXEC"' in result.stdout
    assert '"source_family": "operator_supplied_project_doc_card"' in result.stdout
    assert '"source_read_calls": 0' in result.stdout
    assert "raw private" not in result.stderr


def test_l5_04_runbook_and_packet_preserve_held_surfaces_and_copy_paste_shape():
    helper = _load_helper()
    runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
    packet = PACKET_PATH.read_text(encoding="utf-8")

    assert "DRY-RUN / NO-EXECUTION / NO-READ" in runbook
    assert "python scripts/l5_supervised_one_read.py" in runbook
    assert "--execute" in runbook
    assert "--approval-phrase" in runbook
    assert helper.APPROVAL_PHRASE in runbook
    assert helper.APPROVAL_PHRASE in packet
    for phrase in (
        "no source discovery",
        "no source reads",
        "no credential/auth/env/keychain/OAuth/auth-file reads",
        "no Runtime Registry consumption",
        "no global config mutation",
        "no service/listener/cron/startup activation",
        "no provider/prod/canary authority",
        "no writes/custody/reindex",
        "no repository visibility or package publication change",
        "no Atlas Gate movement",
    ):
        assert phrase in runbook
