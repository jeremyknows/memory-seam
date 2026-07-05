"""Memory Seam CLI front door.

The rootless commands remain the original synthetic no-live smoke checks. When
``recall`` or ``context`` receives a local root positional argument, the CLI
uses a packaged local adapter through the default-off runtime.
"""

from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlencode

from . import _style
from .adapters import AdapterMemorySeamProvider
from .adapters import synthetic_safe_content_provider
from .local_adapters.factory import build_local_adapter, valid_local_adapter_names
from .providers import provider_handlers
from .receipts import read_receipt_enabled
from .router import route_request
from .runtime import LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest, StaticIdentityVerifier

CLI_STATUS = "minimal_no_live_synthetic_smoke_cli"
LOCAL_MARKDOWN_PROVIDER_NAME = "local-markdown-cli"
LOCAL_PROVIDER_NAME_PREFIX = "local"
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
TAGLINE = "receipt-first memory boundary for AI agents"
GATE_WORDMARK = """\
███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗
████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝
██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝ ╚████╔╝
██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝
██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║
╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝

          ███████╗███████╗ █████╗ ███╗   ███╗
          ██╔════╝██╔════╝██╔══██╗████╗ ████║
          ███████╗█████╗  ███████║██╔████╔██║
          ╚════██║██╔══╝  ██╔══██║██║╚██╔╝██║
          ███████║███████╗██║  ██║██║ ╚═╝ ██║
          ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═╝ ╚═╝"""
RECEIPT_GATE = "+───────────────────[ receipt gate ]───────────────────+"


def _version() -> str:
    try:
        return version("memory-seam")
    except PackageNotFoundError:
        return "0.1.0"


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


def _local_provider_name(adapter: str) -> str:
    return LOCAL_MARKDOWN_PROVIDER_NAME if adapter == "markdown" else f"{LOCAL_PROVIDER_NAME_PREFIX}-{adapter}-cli"


def build_local_runtime(adapter: str, root: str | Path, **config: Any) -> LocalReadOnlyRuntime:
    """Build the local adapter runtime used by the CLI front door."""

    provider_name = _local_provider_name(adapter)
    return LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name=provider_name),
        provider=AdapterMemorySeamProvider(
            build_local_adapter(adapter, root, **config),
            provider_name=provider_name,
        ),
        identity_verifier=StaticIdentityVerifier(
            subject=LOCAL_MARKDOWN_AGENT,
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )


def build_local_markdown_runtime(root: str | Path) -> LocalReadOnlyRuntime:
    """Build the local markdown runtime used by the CLI front door."""

    return build_local_runtime("markdown", root)


def local_adapter_response(
    endpoint: str,
    *,
    root: str | Path,
    adapter: str = "markdown",
    query: str = "",
    n: int = 5,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Route a local adapter request through the default-off runtime."""

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
        raise ValueError(f"unsupported local adapter CLI endpoint: {endpoint}")
    return build_local_runtime(adapter, root, **(config or {})).handle(RuntimeRequest("GET", target))


def local_markdown_response(
    endpoint: str,
    *,
    root: str | Path,
    query: str = "",
    n: int = 5,
) -> dict[str, Any]:
    """Route a local markdown request through the default-off runtime."""

    return local_adapter_response(endpoint, root=root, adapter="markdown", query=query, n=n)


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


def _scan_count(body: dict[str, Any]) -> int:
    summary = body.get("adapter_scan_summary") or {}
    if isinstance(summary, dict):
        try:
            return int(summary.get("files_scanned") or 0)
        except (TypeError, ValueError):
            return 0
    return 0


def _receipt_line(verdict: str, reason: str) -> str:
    base = f"Receipt: verdict={verdict}; reason={reason};"
    if verdict == "useful":
        return _style.green(f"✓ {base}")
    if verdict in {"degraded", "empty", "not_evaluated"}:
        return _style.yellow(base)
    if verdict == "error":
        return _style.red(base)
    return _style.yellow(base)


def _banner() -> str:
    return "\n".join(
        (
            _style.cyan(GATE_WORDMARK),
            _style.dim(RECEIPT_GATE),
            f"v{_version()} · {TAGLINE}",
            "usage: memory-seam recall <root> \"query\"",
            "       memory-seam context <root> [--json]",
        )
    )


def _scan_status_line(root: str | Path, files_scanned: int = 0) -> str:
    root_label = str(Path(root).expanduser().absolute())
    return f"memory-seam: scanning {root_label} … {files_scanned} files"


def _print_scan_status(root: str | Path) -> None:
    if not _style.enabled():
        return
    sys.stdout.write("\r" + _scan_status_line(root))
    sys.stdout.flush()


def _print_human_local_response(
    response: dict[str, Any],
    *,
    root: str | Path,
    adapter: str,
    overwrite_scan_line: bool = False,
) -> None:
    body = dict(response.get("body") or {})
    items = list(body.get("items") or [])
    root_label = str(Path(root).expanduser().absolute())
    ready = f"memory-seam v{_version()} · adapter={adapter} · root={root_label} · {_scan_count(body)} files scanned"
    if overwrite_scan_line:
        sys.stdout.write("\r" + _style.cyan(ready) + "\033[K\n")
    else:
        print(_style.cyan(ready))
    if not items:
        print("No matches.")
    for index, item in enumerate(items, start=1):
        title = str(item.get("title") or "(untitled)")
        path = str(item.get("path") or ".")
        snippet = " ".join(str(item.get("snippet") or "").split())
        print(f"{index}. {_style.bold(title)}")
        print(f"   {_style.dim(_style.cyan(path))}")
        if snippet:
            print(f"   {snippet}")
    verdict, reason, posture = _receipt_summary(body)
    print(_receipt_line(verdict, reason), _style.dim(f"safe_posture={_format_posture(posture)}"))


def _fatal_adapter_message(root: str | Path, response: dict[str, Any], *, adapter: str) -> str | None:
    body = response.get("body") or {}
    reason = body.get("reason")
    if not isinstance(reason, str) or reason not in FATAL_ADAPTER_REASONS:
        return None
    return f"memory-seam: cannot read {adapter} root {str(root)!r}: {FATAL_ADAPTER_REASONS[reason]} ({reason})"


def _add_local_adapter_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--adapter", default="markdown", choices=valid_local_adapter_names())
    parser.add_argument("--db-table", help="sqlite table name for --adapter sqlite")
    parser.add_argument("--title-column", help="sqlite title column for --adapter sqlite")
    parser.add_argument("--body-column", help="sqlite body column for --adapter sqlite")


def _adapter_config_from_args(args: argparse.Namespace) -> dict[str, Any]:
    config: dict[str, Any] = {}
    if getattr(args, "adapter", None) == "sqlite":
        config = {
            "table": args.db_table,
            "title_column": args.title_column,
            "body_column": args.body_column,
        }
    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memory-seam",
        description="Read local notes through Memory Seam or run no-live synthetic smoke checks.",
    )
    parser.add_argument("--version", action="store_true", help="show version and usage")
    subparsers = parser.add_subparsers(dest="endpoint")

    health = subparsers.add_parser("health", help="emit synthetic provider health JSON")
    health.set_defaults(include="project", mode="startup", agent=None, query="", scope="wiki", n=5)

    context = subparsers.add_parser("context", help="read local adapter context, or emit synthetic context JSON")
    context.add_argument("root", nargs="?", help="local notes root/database; omit for synthetic smoke JSON")
    _add_local_adapter_options(context)
    context.add_argument("--json", action="store_true", help="print the full local adapter envelope as JSON")
    context.add_argument("--include", default="project", choices=("project", "memory", "project,memory"))
    context.add_argument("--mode", default="startup")
    context.add_argument("--agent", default="agent:memory-seam-cli")
    context.set_defaults(query="", scope="wiki", n=5)

    recall = subparsers.add_parser("recall", help="read local adapter recall, or emit synthetic recall JSON")
    recall.add_argument("root", nargs="?", help="local notes root/database; omit for synthetic smoke JSON")
    recall.add_argument("query_text", nargs="?", help="local recall query")
    _add_local_adapter_options(recall)
    recall.add_argument("--json", action="store_true", help="print the full local adapter envelope as JSON")
    recall.add_argument("--query", default="runtime boundary")
    recall.add_argument("--scope", default="wiki", choices=("wiki", "diary", "context", "all"))
    recall.add_argument("--n", default=5, type=int)
    recall.add_argument("--agent", default="agent:memory-seam-cli")
    recall.set_defaults(include="project", mode="startup")

    librarian = subparsers.add_parser("librarian", help="initialize or inspect a memory librarian template package")
    librarian_subparsers = librarian.add_subparsers(dest="librarian_command")

    librarian_init = librarian_subparsers.add_parser("init", help="create a memory librarian workspace")
    librarian_init.add_argument("dest", help="empty destination directory for the librarian workspace")
    librarian_init.add_argument("--notes", help="configured notes root; defaults to <dest>/memory")
    librarian_init.add_argument("--client", default="none", choices=("claude-code", "claude-desktop", "none"))
    librarian_init.add_argument("--adapter", default="markdown", choices=valid_local_adapter_names(), help="source adapter")
    librarian_init.add_argument("--mode", default="supervised-request", choices=("supervised-request", "draft-only"))
    librarian_init.add_argument("--agent-name", default="Memory Librarian")
    librarian_init.add_argument("--operator-name", default="Operator")
    librarian_init.add_argument("--timezone")

    librarian_doctor = librarian_subparsers.add_parser("doctor", help="check a memory librarian workspace posture")
    librarian_doctor.add_argument("dest", help="librarian workspace directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version or args.endpoint is None:
        print(_banner())
        return 0
    if args.endpoint == "librarian":
        from .librarian import doctor_librarian, init_librarian, make_init_options

        if args.librarian_command == "init":
            return init_librarian(make_init_options(args))
        if args.librarian_command == "doctor":
            return doctor_librarian(Path(args.dest))
        parser.error("missing librarian command")
    if args.endpoint in {"context", "recall"} and getattr(args, "root", None):
        if args.endpoint == "recall" and not args.query_text:
            parser.error('recall with a local root requires a query, e.g. memory-seam recall ./notes "launch plan"')
        show_scan_status = not args.json and _style.enabled()
        if show_scan_status:
            _print_scan_status(args.root)
        try:
            response = local_adapter_response(
                args.endpoint,
                root=args.root,
                adapter=args.adapter,
                query=getattr(args, "query_text", "") or "",
                n=args.n,
                config=_adapter_config_from_args(args),
            )
        except ValueError as exc:
            if show_scan_status:
                sys.stdout.write("\r\033[K")
                sys.stdout.flush()
            print(_style.red(f"memory-seam: {exc}"), file=sys.stderr)
            return 2
        fatal = _fatal_adapter_message(args.root, response, adapter=args.adapter)
        if fatal is not None:
            if show_scan_status:
                sys.stdout.write("\r\033[K")
                sys.stdout.flush()
            print(_style.red(fatal), file=sys.stderr)
            return 2
        if args.json:
            print(json.dumps(_json_safe(response), indent=2, sort_keys=True))
        else:
            _print_human_local_response(
                response,
                root=args.root,
                adapter=args.adapter,
                overwrite_scan_line=show_scan_status,
            )
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
    "build_local_runtime",
    "build_parser",
    "local_adapter_response",
    "local_markdown_response",
    "main",
    "no_live_response",
]
