"""Supervised no-live manual pull dogfood harness.

This example is intentionally local and bounded: it builds the committed
synthetic provider in-process, asks one source-card-first context question, then
asks one recall question against the same synthetic fixture deck. It does not
start a service, discover sources, read live/private files, consume Runtime
Registry, grant cron/startup authority, or perform writes/custody/reindex work.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_seam.adapters import synthetic_safe_content_provider  # noqa: E402
from memory_seam.providers import provider_handlers  # noqa: E402
from memory_seam.receipts import build_read_receipt, read_receipt_enabled  # noqa: E402
from memory_seam.router import route_request  # noqa: E402


def _route(target: str) -> dict:
    provider = synthetic_safe_content_provider()
    return route_request(
        "GET",
        target,
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context:project", "context:memory", "wiki"],
    )


def _safe_posture(body: dict) -> dict:
    return {
        "raw_fallback_used": body["raw_fallback_used"],
        "read_backend_called": body["read_backend_called"],
        "runtime_registry_consumed": body["runtime_registry_consumed"],
        "service_started": body["service_started"],
        "write_custody_or_reindex": body["write_custody_or_reindex"],
    }


def build_manual_pull_summary() -> dict:
    """Return a compact report-safe summary for the supervised dogfood run."""

    context_response = _route(
        "/context?include=project,memory&mode=manual_pull_dogfood&agent=sax&read_receipt=metadata_only"
    )
    context_body = context_response["body"]
    context_receipt = build_read_receipt(
        endpoint="context",
        token_subject="agent:example",
        timeout_ms=context_body["timeout_ms"],
        envelope=context_body,
    )

    recall_response = _route(
        "/recall?query=runtime+identity+rollback&scope=wiki&n=2&read_receipt=metadata_only"
    )
    recall_body = recall_response["body"]
    recall_receipt = build_read_receipt(
        endpoint="recall",
        token_subject="agent:example",
        timeout_ms=recall_body["timeout_ms"],
        envelope=recall_body,
    )

    return {
        "status": "manual_pull_dogfood_no_live_pass",
        "context": {
            "status_code": context_response["status_code"],
            "source_card_count": len(context_body["source_cards"]),
            "source_card_ids": [card["card_id"] for card in context_body["source_cards"]],
            "item_titles": [item["title"] for item in context_body["items"]],
            "receipt_verdict": context_receipt["usefulness_shape"]["verdict"],
            "safe_posture": _safe_posture(context_body),
        },
        "recall": {
            "status_code": recall_response["status_code"],
            "item_titles": [item["title"] for item in recall_body["items"]],
            "receipt_verdict": recall_receipt["usefulness_shape"]["verdict"],
            "safe_posture": _safe_posture(recall_body),
        },
        "held_authority": [
            "no_cron_or_startup_injection",
            "no_service_or_listener",
            "no_broad_recall_authority",
            "no_live_or_private_source_reads",
            "no_runtime_registry_consumption",
            "no_write_custody_or_reindex",
        ],
    }


def main() -> None:
    print(json.dumps(build_manual_pull_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
