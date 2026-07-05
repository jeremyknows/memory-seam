#!/usr/bin/env python3
"""No-live examples for null and fake Memory Seam providers.

The null provider demonstrates the safe unconfigured shape. The fake provider
uses committed synthetic strings only; it does not discover local sources, call
external providers, start services, consume Runtime Registry, or write custody /
reindex artifacts.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_seam import (  # noqa: E402
    AdapterMemorySeamProvider,
    NullMemorySeamProvider,
    SourceCard,
    SyntheticSourceCardAdapter,
    provider_handlers,
    read_receipt_enabled,
    route_request,
)


FAKE_RUNBOOK_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "id": "fake-runbook-boundary",
        "scope": "context",
        "include_family": "project",
        "source_tier": "fake_fixture",
        "backend": "fake_no_live_provider",
        "retrieval_backend": "committed_fixture",
        "canonicality": "example_fixture",
        "private_class": "reportable_synthetic",
        "title": "Fake provider boundary",
        "snippet": "Fake providers should return committed safe fixtures and never call live backends.",
        "redaction_applied": False,
        "redaction_labels": [],
        "truncated": False,
    },
    {
        "id": "fake-runbook-recall",
        "scope": "wiki",
        "include_family": "memory",
        "source_tier": "fake_fixture",
        "backend": "fake_no_live_provider",
        "retrieval_backend": "committed_fixture",
        "canonicality": "example_fixture",
        "private_class": "reportable_synthetic",
        "title": "Fake recall fixture",
        "snippet": "Recall can be smoke-tested with deterministic fake items before any live adapter exists.",
        "redaction_applied": False,
        "redaction_labels": [],
        "truncated": False,
    },
)


@dataclass(frozen=True)
class FakeRunbookAdapter:
    """Tiny example adapter backed only by in-file report-safe fixtures."""

    adapter_name: str = "fake-runbook-fixture"
    items: tuple[dict[str, Any], ...] = FAKE_RUNBOOK_ITEMS

    def context_items(self, *, include: Iterable[str], token_subject: str | None) -> list[dict[str, Any]]:
        requested = {part for part in include if part} or {"project", "memory"}
        return [dict(item) for item in self.items if item["include_family"] in requested]

    def recall_items(self, query: str, *, scope: str, token_subject: str | None, n: int) -> list[dict[str, Any]]:
        terms = query.lower().split()
        allowed_scopes = {"wiki", "diary", "context"} if scope == "all" else {scope}
        matches = []
        for item in self.items:
            haystack = f"{item['title']} {item['snippet']}".lower()
            if item["scope"] in allowed_scopes and (not terms or any(term in haystack for term in terms)):
                matches.append(dict(item))
        return matches[: max(0, int(n))]


def null_provider_context() -> dict[str, Any]:
    """Route a context request through NullMemorySeamProvider."""

    provider = NullMemorySeamProvider(provider_name="example-null")
    return route_request(
        "GET",
        "/context?include=project&mode=example",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes={"context", "wiki"},
    )


def fake_provider() -> AdapterMemorySeamProvider:
    """Build a deterministic fake provider suitable for no-live smoke tests."""

    cards = (
        SourceCard(
            card_id="fake-source-card-boundary",
            include_family="project",
            source_tier="fake_fixture",
            private_class="reportable_synthetic",
            canonicality="example_fixture",
            retrieval_backend="committed_fixture",
            title="Fake provider boundary card",
            safe_summary="Fake adapter examples are committed fixtures only; no live provider is contacted.",
        ),
    )
    return AdapterMemorySeamProvider(
        FakeRunbookAdapter(),
        SyntheticSourceCardAdapter(adapter_name="fake-source-card-fixture", cards=cards),
        provider_name="example-fake",
    )


def fake_provider_context() -> dict[str, Any]:
    """Route a context request through the fake provider."""

    provider = fake_provider()
    return route_request(
        "GET",
        "/context?include=project&mode=example",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes={"context", "wiki"},
    )


def fake_provider_recall() -> dict[str, Any]:
    """Route a recall request through the fake provider."""

    provider = fake_provider()
    return route_request(
        "GET",
        "/recall?query=smoke+fake&scope=wiki&n=2",
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes={"context", "wiki"},
    )


def compact_summary(response: dict[str, Any]) -> dict[str, Any]:
    body = dict(response.get("body") or {})
    return {
        "status_code": response.get("status_code"),
        "endpoint": body.get("endpoint"),
        "provider": body.get("provider"),
        "items": [item.get("title") for item in body.get("items", [])],
        "degraded_reasons": body.get("degraded_reasons", []),
        "safe_posture": {
            "read_backend_called": body.get("read_backend_called"),
            "service_started": body.get("service_started"),
            "runtime_registry_consumed": body.get("runtime_registry_consumed"),
            "raw_fallback_used": body.get("raw_fallback_used", False),
            "write_custody_or_reindex": body.get("write_custody_or_reindex"),
        },
    }


def main() -> int:
    payload = {
        "null_context": compact_summary(null_provider_context()),
        "fake_context": compact_summary(fake_provider_context()),
        "fake_recall": compact_summary(fake_provider_recall()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
