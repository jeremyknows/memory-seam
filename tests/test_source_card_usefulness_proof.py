from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from memory_seam.adapters import SAFE_DOGFOOD_ITEMS, score_synthetic_usefulness

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "f3-source-card-usefulness-proof.md"

_spec = importlib.util.spec_from_file_location("manual_pull_dogfood", ROOT / "examples" / "manual_pull_dogfood.py")
assert _spec and _spec.loader
manual_pull_dogfood = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(manual_pull_dogfood)
build_manual_pull_summary = manual_pull_dogfood.build_manual_pull_summary

SAFE_POSTURE_FALSE = {
    "raw_fallback_used": False,
    "read_backend_called": False,
    "runtime_registry_consumed": False,
    "service_started": False,
    "write_custody_or_reindex": False,
}


def test_source_card_usefulness_pass_packet_records_safe_ids_and_no_fallback():
    summary = build_manual_pull_summary()

    assert summary["status"] == "manual_pull_dogfood_no_live_pass"
    assert summary["context"]["status_code"] == 200
    assert summary["recall"]["status_code"] == 200
    assert summary["context"]["receipt_verdict"] == "useful"
    assert summary["recall"]["receipt_verdict"] == "useful"
    assert summary["context"]["source_card_count"] == 2
    assert summary["context"]["source_card_ids"] == [
        "source-card-project-boundary",
        "source-card-runtime-answer",
    ]
    assert summary["context"]["safe_posture"] == SAFE_POSTURE_FALSE
    assert summary["recall"]["safe_posture"] == SAFE_POSTURE_FALSE

    rendered = json.dumps(summary, sort_keys=True)
    assert "/" + "Users" + "/" not in rendered
    assert "gho_" not in rendered
    assert "ghp_" not in rendered
    assert "raw query" not in rendered.lower()


def test_source_card_usefulness_matrix_has_pass_hold_fail_without_private_reads():
    passed = score_synthetic_usefulness(SAFE_DOGFOOD_ITEMS)
    held = score_synthetic_usefulness(
        [
            {
                **SAFE_DOGFOOD_ITEMS[0],
                "snippet": "[redacted-token] Synthetic no-live/read-only boundary remains reportable.",
                "redaction_applied": True,
                "redaction_labels": ["token"],
                "truncated": True,
            }
        ]
    )
    failed = score_synthetic_usefulness([], degraded_reasons=["synthetic_fixture_empty"])

    assert passed["verdict"] == "PASS"
    assert passed["answerable"] is True
    assert passed["safe"] is True
    assert passed["reason_codes"] == ["safe_context_sufficient"]

    assert held["verdict"] == "HOLD"
    assert held["answerable"] is True
    assert held["safe"] is True
    assert "redaction_survived" in held["reason_codes"]
    assert "safe_content_truncated" in held["reason_codes"]

    assert failed["verdict"] == "FAIL"
    assert failed["answerable"] is False
    assert failed["too_degraded"] is True
    assert "too_degraded" in failed["reason_codes"]

    for score in (passed, held, failed):
        assert "/" + "Users" + "/" not in repr(score)
        assert "gho_" not in repr(score)
        assert "ghp_" not in repr(score)


def test_source_card_usefulness_packet_is_discoverable_and_names_acceptance_fields():
    packet = PACKET.read_text()
    readme = (ROOT / "README.md").read_text()
    docs_index = (ROOT / "docs" / "README.md").read_text()
    inventory = (ROOT / "docs" / "contract-test-inventory.md").read_text()

    assert "docs/f3-source-card-usefulness-proof.md" in readme
    assert "f3-source-card-usefulness-proof.md" in docs_index
    assert "tests/test_source_card_usefulness_proof.py" in inventory

    for text in [
        '"outcome": "PASS"',
        '"outcome": "HOLD"',
        '"outcome": "FAIL"',
        '"raw_fallback_used": false',
        '"service_started": false',
        '"runtime_registry_consumed": false',
        '"write_custody_or_reindex": false',
        '"read_backend_called": false',
        "source-card-project-boundary",
        "source-card-runtime-answer",
        "pytest -q tests/test_source_card_usefulness_proof.py",
    ]:
        assert text in packet

    assert "raw private source text" in packet
    assert "private absolute paths" in packet
    assert "raw query payloads" in packet
    assert "zero counters or monkeypatch/spy assertions" in packet


def test_source_card_usefulness_focused_command_emits_report_safe_json():
    result = subprocess.run(
        [sys.executable, "examples/manual_pull_dogfood.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert payload["context"]["safe_posture"] == SAFE_POSTURE_FALSE
    assert payload["recall"]["safe_posture"] == SAFE_POSTURE_FALSE
    assert payload["context"]["source_card_ids"] == [
        "source-card-project-boundary",
        "source-card-runtime-answer",
    ]
    assert "/" + "Users" + "/" not in result.stdout
    assert "raw query" not in result.stdout.lower()
