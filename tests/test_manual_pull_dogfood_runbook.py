from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "f3-manual-pull-dogfood.md"

_spec = importlib.util.spec_from_file_location("manual_pull_dogfood", ROOT / "examples" / "manual_pull_dogfood.py")
assert _spec and _spec.loader
manual_pull_dogfood = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(manual_pull_dogfood)
build_manual_pull_summary = manual_pull_dogfood.build_manual_pull_summary


def test_manual_pull_dogfood_summary_is_source_card_first_and_no_live():
    summary = build_manual_pull_summary()

    assert summary["status"] == "manual_pull_dogfood_no_live_pass"
    assert summary["context"]["status_code"] == 200
    assert summary["context"]["source_card_count"] == 2
    assert summary["context"]["source_card_ids"] == [
        "source-card-project-boundary",
        "source-card-runtime-answer",
    ]
    assert summary["context"]["item_titles"] == [
        "Memory Seam project boundary",
        "Default-off runtime answer",
    ]
    assert summary["recall"]["status_code"] == 200
    assert summary["recall"]["item_titles"] == ["Default-off runtime answer"]
    assert summary["context"]["receipt_verdict"] == "useful"
    assert summary["recall"]["receipt_verdict"] == "useful"

    for endpoint in ("context", "recall"):
        assert summary[endpoint]["safe_posture"] == {
            "raw_fallback_used": False,
            "read_backend_called": False,
            "runtime_registry_consumed": False,
            "service_started": False,
            "write_custody_or_reindex": False,
        }

    assert "no_cron_or_startup_injection" in summary["held_authority"]
    assert "no_broad_recall_authority" in summary["held_authority"]
    assert "no_write_custody_or_reindex" in summary["held_authority"]


def test_manual_pull_dogfood_command_emits_report_safe_json():
    result = subprocess.run(
        [sys.executable, "examples/manual_pull_dogfood.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)
    rendered = result.stdout

    assert payload["status"] == "manual_pull_dogfood_no_live_pass"
    assert payload["context"]["source_card_count"] == 2
    assert payload["recall"]["receipt_verdict"] == "useful"
    assert "/" + "Users" + "/" not in rendered
    assert "gho_" not in rendered
    assert "ghp_" not in rendered
    assert ".env" not in rendered
    assert "raw query" not in rendered.lower()


def test_manual_pull_dogfood_runbook_is_discoverable_and_names_boundaries():
    runbook = RUNBOOK.read_text()
    readme = (ROOT / "README.md").read_text()
    docs_index = (ROOT / "docs" / "README.md").read_text()
    inventory = (ROOT / "docs" / "contract-test-inventory.md").read_text()

    assert "docs/f3-manual-pull-dogfood.md" in readme
    assert "f3-manual-pull-dogfood.md" in docs_index
    assert "examples/manual_pull_dogfood.py" in docs_index
    assert "tests/test_manual_pull_dogfood_runbook.py" in inventory

    assert "PYTHONPATH=src python examples/manual_pull_dogfood.py" in runbook
    assert "pytest -q tests/test_manual_pull_dogfood_runbook.py" in runbook
    assert '"source_card_count": 2' in runbook
    assert '"receipt_verdict": "useful"' in runbook
    assert '"raw_fallback_used": false' in runbook
    assert "does **not** grant cron/startup injection" in runbook
    for held in [
        "service/listener",
        "broad recall authority",
        "live or private source reads",
        "Runtime Registry consumption",
        "writes, custody, reindexing",
    ]:
        assert held in runbook
