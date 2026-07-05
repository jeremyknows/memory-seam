"""Memory Seam CLI front door.

The rootless commands remain the original synthetic no-live smoke checks. When
``recall`` or ``context`` receives a local root positional argument, the CLI
uses the packaged local markdown adapter through the default-off runtime.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlencode

from .adapters import AdapterMemorySeamProvider
from .adapters import synthetic_safe_content_provider
from .local_adapters.markdown import LocalMarkdownAdapter
from .providers import provider_handlers
from .receipts import read_receipt_enabled
from .router import route_request
from .runtime import LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest, StaticIdentityVerifier

CLI_STATUS = "minimal_no_live_synthetic_smoke_cli"
LOCAL_MARKDOWN_PROVIDER_NAME = "local-markdown-cli"
LOCAL_MARKDOWN_AGENT = "agent:memory-seam-cli"
READ_RECEIPT_QUERY_VALUE = "metadata_only"
CLI_HELD_SURFACES = (
    "daemon_or_listener",
    "live_source_reads",
    "runtime_registry_consumption",
    "global_config_mutation",
    "write_like_routes",
    "custody_or_reindex",
)
FATAL_ADAPTER_REASONS = {
    "missing_root": "missing root",
    "not_a_directory": "root is not a directory",
    "root_is_symlink": "root is a symlink",
    "permission_denied": "permission denied",
    "root_unavailable": "root is unavailable",
}


def no_live_response(endpoint: str, *, include: str, mode: str, agent: str | None, query: str, scope: str, n: int) -> dict[str, Any]:
    """Route one health/context/recall smoke request through committed fixtures only."""

    provider = synthetic_safe_content_provider()
    if endpoint == "health":
        target = "/health"
    elif endpoint == "context":
        target = f"/context?include={include}&mode={mode}"
        if agent:
            target += f"&agent={agent}"
    elif endpoint == "recall":
        target = f"/recall?query={query}&scope={scope}&n={n}"
        if agent:
            target += f"&agent={agent}"
    else:  # Defensive: argparse prevents this branch for CLI calls.
        raise ValueError(f"unsupported no-live CLI endpoint: {endpoint}")

    response = route_request(
        "GET",
        target,
        **provider_handlers(provider),
        read_receipt_enabled=read_receipt_enabled,
        token_subject=agent,
        allowed_scopes=["context", "wiki", "diary"],
    )
    body = dict(response.get("body") or {})
    body["cli"] = {
        "status": CLI_STATUS,
        "synthetic_fixtures_only": True,
        "service_started": False,
        "live_source_reads": False,
        "runtime_registry_consumed": False,
        "write_like_routes_available": False,
        "write_custody_or_reindex": False,
        "held_surfaces": list(CLI_HELD_SURFACES),
    }
    return {**response, "body": body}


def build_local_markdown_runtime(root: str | Path) -> LocalReadOnlyRuntime:
    """Build the local markdown runtime used by the CLI front door."""

    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name=LOCAL_MARKDOWN_PROVIDER_NAME),
        provider=AdapterMemorySeamProvider(
            LocalMarkdownAdapter(root),
            provider_name=LOCAL_MARKDOWN_PROVIDER_NAME,
        ),
        identity_verifier=StaticIdentityVerifier(
            subject=LOCAL_MARKDOWN_AGENT,
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def local_markdown_response(
    endpoint: str,
    *,
    root: str | Path,
    query: str = "",
    n: int = 5,
) -> dict[str, Any]:
    """Route a local markdown request through the default-off runtime."""

    if endpoint == "context":
        target = "/context?" + urlencode(
            {
                "include": "memory",
                "mode": "startup",
                "agent": LOCAL_MARKDOWN_AGENT,
                "read_receipt": READ_RECEIPT_QUERY_VALUE,
            }
        )
    elif endpoint == "recall":
        target = "/recall?" + urlencode(
            {
                "query": query,
                "scope": "wiki",
                "n": n,
                "agent": LOCAL_MARKDOWN_AGENT,
                "read_receipt": READ_RECEIPT_QUERY_VALUE,
            }
        )
    else:
        raise ValueError(f"unsupported local markdown CLI endpoint: {endpoint}")
    return build_local_markdown_runtime(root).handle(RuntimeRequest("GET", target))


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(child) for child in value]
    if isinstance(value, (set, frozenset)):
        return sorted(str(child) for child in value)
    return value


def _safe_posture(body: dict[str, Any]) -> dict[str, bool]:
    return {
        "read_backend_called": bool(body.get("read_backend_called")),
        "service_started": bool(body.get("service_started")),
        "runtime_registry_consumed": bool(body.get("runtime_registry_consumed")),
        "raw_fallback_used": bool(body.get("raw_fallback_used")),
        "write_custody_or_reindex": bool(body.get("write_custody_or_reindex")),
    }


def _receipt_summary(body: dict[str, Any]) -> tuple[str, str, dict[str, bool]]:
    receipt = body.get("read_receipt") or {}
    usefulness = receipt.get("usefulness_shape") or {}
    verdict = str(usefulness.get("verdict") or "not_evaluated")
    reason = str(usefulness.get("reason_code") or "not_scored")
    return verdict, reason, _safe_posture(body)


def _format_posture(posture: dict[str, bool]) -> str:
    return ", ".join(f"{key}={str(value).lower()}" for key, value in posture.items())


def _print_human_local_markdown(response: dict[str, Any]) -> None:
    body = dict(response.get("body") or {})
    items = list(body.get("items") or [])
    if not items:
        print("No matches.")
    for index, item in enumerate(items, start=1):
        title = str(item.get("title") or "(untitled)")
        path = str(item.get("path") or ".")
        snippet = " ".join(str(item.get("snippet") or "").split())
        print(f"{index}. {title}")
        print(f"   {path}")
        if snippet:
            print(f"   {snippet}")
    verdict, reason, posture = _receipt_summary(body)
    print(f"Receipt: verdict={verdict}; reason={reason}; safe_posture={_format_posture(posture)}")


def _fatal_adapter_message(root: str | Path, response: dict[str, Any]) -> str | None:
    body = response.get("body") or {}
    reason = body.get("reason")
    if not isinstance(reason, str) or reason not in FATAL_ADAPTER_REASONS:
        return None
    return f"memory-seam: cannot read markdown root {str(root)!r}: {FATAL_ADAPTER_REASONS[reason]} ({reason})"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memory-seam",
        description="Read local markdown through Memory Seam or run no-live synthetic smoke checks.",
    )
    subparsers = parser.add_subparsers(dest="endpoint", required=True)

    health = subparsers.add_parser("health", help="emit synthetic provider health JSON")
    health.set_defaults(include="project", mode="startup", agent=None, query="", scope="wiki", n=5)

    context = subparsers.add_parser("context", help="read local markdown context, or emit synthetic context JSON")
    context.add_argument("root", nargs="?", help="local markdown root; omit for synthetic smoke JSON")
    context.add_argument("--adapter", default="markdown", choices=("markdown",))
    context.add_argument("--json", action="store_true", help="print the full local markdown envelope as JSON")
    context.add_argument("--include", default="project", choices=("project", "memory", "project,memory"))
    context.add_argument("--mode", default="startup")
    context.add_argument("--agent", default="agent:memory-seam-cli")
    context.set_defaults(query="", scope="wiki", n=5)

    recall = subparsers.add_parser("recall", help="read local markdown recall, or emit synthetic recall JSON")
    recall.add_argument("root", nargs="?", help="local markdown root; omit for synthetic smoke JSON")
    recall.add_argument("query_text", nargs="?", help="local markdown recall query")
    recall.add_argument("--adapter", default="markdown", choices=("markdown",))
    recall.add_argument("--json", action="store_true", help="print the full local markdown envelope as JSON")
    recall.add_argument("--query", default="runtime boundary")
    recall.add_argument("--scope", default="wiki", choices=("wiki", "diary", "context", "all"))
    recall.add_argument("--n", default=5, type=int)
    recall.add_argument("--agent", default="agent:memory-seam-cli")
    recall.set_defaults(include="project", mode="startup")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.endpoint in {"context", "recall"} and getattr(args, "root", None):
        if args.endpoint == "recall" and not args.query_text:
            parser.error('recall with a local root requires a query, e.g. memory-seam recall ./notes "launch plan"')
        response = local_markdown_response(
            args.endpoint,
            root=args.root,
            query=getattr(args, "query_text", "") or "",
            n=args.n,
        )
        fatal = _fatal_adapter_message(args.root, response)
        if fatal is not None:
            print(fatal, file=sys.stderr)
            return 2
        if args.json:
            print(json.dumps(_json_safe(response), indent=2, sort_keys=True))
        else:
            _print_human_local_markdown(response)
        return 0 if int(response.get("status_code", 1)) < 400 else 1

    payload = no_live_response(
        args.endpoint,
        include=args.include,
        mode=args.mode,
        agent=args.agent,
        query=args.query,
        scope=args.scope,
        n=args.n,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if int(payload.get("status_code", 1)) < 400 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


__all__ = [
    "CLI_HELD_SURFACES",
    "CLI_STATUS",
    "LOCAL_MARKDOWN_PROVIDER_NAME",
    "build_local_markdown_runtime",
    "build_parser",
    "local_markdown_response",
    "main",
    "no_live_response",
]
