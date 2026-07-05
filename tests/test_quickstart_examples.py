from __future__ import annotations

import importlib.util
from pathlib import Path

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "quickstart_smoke.py"
SPEC = importlib.util.spec_from_file_location("quickstart_smoke", EXAMPLE_PATH)
assert SPEC and SPEC.loader
quickstart_smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quickstart_smoke)

compact_summary = quickstart_smoke.compact_summary
quickstart_context = quickstart_smoke.quickstart_context
quickstart_recall = quickstart_smoke.quickstart_recall


def test_quickstart_context_answers_from_synthetic_safe_content():
    response = quickstart_context()
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["token_subject"] == "agent:quickstart"
    assert any(item["title"] == "Memory Seam project boundary" for item in body["items"])
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["raw_fallback_used"] is False
    assert body["write_custody_or_reindex"] is False
    assert body["read_receipt"]["usefulness_shape"]["task_answerable_from_safe_content"] is True


def test_quickstart_recall_answers_runtime_boundary():
    response = quickstart_recall()
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "recall"
    assert body["scope_effective"] == ["wiki"]
    assert any("identity verification is explicit" in item["snippet"] for item in body["items"])
    assert body["read_receipt"]["flight_record"]["outcome"] == "answered_from_safe_context"
    assert body["runtime"]["service_started"] is False
    assert body["runtime"]["write_custody_or_reindex"] is False


def test_compact_summary_is_readme_safe_and_stable():
    summary = compact_summary(quickstart_context())
    assert summary == {
        "status_code": 200,
        "endpoint": "context",
        "items": ["Memory Seam project boundary", "Default-off runtime answer"],
        "safe_posture": {
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "raw_fallback_used": False,
            "write_custody_or_reindex": False,
        },
        "receipt_verdict": "useful",
    }
