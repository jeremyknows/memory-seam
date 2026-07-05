from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "null_and_fake_providers.py"
SPEC = importlib.util.spec_from_file_location("null_and_fake_providers", EXAMPLE_PATH)
assert SPEC and SPEC.loader
null_and_fake_providers = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = null_and_fake_providers
SPEC.loader.exec_module(null_and_fake_providers)

compact_summary = null_and_fake_providers.compact_summary
fake_provider_context = null_and_fake_providers.fake_provider_context
fake_provider_recall = null_and_fake_providers.fake_provider_recall
null_provider_context = null_and_fake_providers.null_provider_context


def test_null_provider_example_returns_safe_unconfigured_context():
    response = null_provider_context()
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["provider"] == "example-null"
    assert body["items"] == []
    assert body["degraded_reasons"] == ["provider_unconfigured"]
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["write_custody_or_reindex"] is False


def test_fake_provider_example_context_uses_committed_fixture_only():
    response = fake_provider_context()
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "context"
    assert body["provider"] == "example-fake"
    assert body["adapter"] == "fake-runbook-fixture"
    assert [item["title"] for item in body["items"]] == ["Fake provider boundary"]
    assert body["source_cards"][0]["safe_summary"].startswith("Fake adapter examples")
    assert body["read_backend_called"] is False
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False
    assert body["raw_fallback_used"] is False
    assert body["write_custody_or_reindex"] is False


def test_fake_provider_example_recall_is_deterministic_no_live():
    response = fake_provider_recall()
    assert response["status_code"] == 200
    body = response["body"]
    assert body["endpoint"] == "recall"
    assert body["scope_effective"] == ["wiki"]
    assert [item["title"] for item in body["items"]] == ["Fake recall fixture"]
    assert "smoke-tested" in body["items"][0]["snippet"]
    assert body["read_backend_called"] is False
    assert body["runtime_registry_consumed"] is False


def test_null_and_fake_provider_compact_summary_is_doc_safe():
    assert compact_summary(null_provider_context()) == {
        "status_code": 200,
        "endpoint": "context",
        "provider": "example-null",
        "items": [],
        "degraded_reasons": ["provider_unconfigured"],
        "safe_posture": {
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "raw_fallback_used": False,
            "write_custody_or_reindex": False,
        },
    }
