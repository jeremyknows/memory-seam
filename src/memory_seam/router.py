"""Portable no-live Memory Seam router helpers."""

from __future__ import annotations

from typing import Any, Callable, Iterable
from urllib.parse import parse_qs, urlsplit

from .contracts import CONTRACT_STATUS, MAX_TIMEOUT_MS, MIN_TIMEOUT_MS, WRITE_LIKE_ROUTES, payload_has_write_like_shape


def first(params: dict[str, list[str]], key: str, default: str | None = None) -> str | None:
    values = params.get(key)
    if not values:
        return default
    return values[0]


def csv_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def int_param(
    params: dict[str, list[str]],
    key: str,
    default: int,
    *,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    value = first(params, key)
    parsed = default if value is None or value == "" else int(value)
    if min_value is not None:
        parsed = max(min_value, parsed)
    if max_value is not None:
        parsed = min(max_value, parsed)
    return parsed


def response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "status_code": status_code,
        "headers": {"content-type": "application/json"},
        "body": body,
    }


def error(status_code: int, error_code: str) -> dict[str, Any]:
    return response(
        status_code,
        {
            "error": error_code,
            "contract_status": CONTRACT_STATUS,
            "write_like_routes": "absent_or_404_405",
            "read_backend_called": False,
            "source_stat_called": False,
            "write_custody_or_reindex": False,
        },
    )


def route_request(
    method: str,
    target: str,
    *,
    health_handler: Callable[[], dict[str, Any]],
    context_handler: Callable[..., dict[str, Any]],
    recall_handler: Callable[..., dict[str, Any]],
    read_receipt_enabled: Callable[[str | None], bool],
    token_subject: str | None = None,
    allowed_scopes: Iterable[str] | None = None,
    acting_for: str | None = None,
    context_sources=None,
    context_source_allowlist=None,
    request_body: dict[str, Any] | None = None,
    diary_read_ceiling: str | None = None,
) -> dict[str, Any]:
    normalized_method = method.upper()
    parsed = urlsplit(target)
    path = parsed.path or "/"
    params = parse_qs(parsed.query, keep_blank_values=True)

    route = f"{normalized_method} {path}"
    if route in WRITE_LIKE_ROUTES:
        return error(405, "write_like_route_unavailable")
    if path not in {"/health", "/context", "/recall"}:
        return error(404, "route_not_found")
    if normalized_method != "GET":
        return error(405, "method_not_allowed")
    if payload_has_write_like_shape({key: values for key, values in params.items()}) or payload_has_write_like_shape(
        request_body
    ):
        return error(405, "write_like_payload_unavailable")

    try:
        if path == "/health":
            body = {"endpoint": "health", **health_handler()}
        elif path == "/context":
            body = context_handler(
                include=csv_list(first(params, "include")),
                mode=first(params, "mode", "startup") or "startup",
                agent=first(params, "agent"),
                token_subject=token_subject,
                allowed_scopes=allowed_scopes,
                acting_for=acting_for,
                timeout_ms=int_param(params, "timeout_ms", 1500, min_value=MIN_TIMEOUT_MS, max_value=MAX_TIMEOUT_MS),
                context_sources=context_sources,
                context_source_allowlist=context_source_allowlist,
                include_read_receipt=read_receipt_enabled(first(params, "read_receipt")),
            )
        else:
            query = first(params, "query", "") or ""
            # diary_read_ceiling is omitted entirely when unset so the recall
            # handler's default (self-ceiling, fail-closed) is preserved and
            # pre-W2b handlers that don't accept the kwarg keep working.
            ceiling_kwargs: dict[str, Any] = (
                {"diary_read_ceiling": diary_read_ceiling} if diary_read_ceiling is not None else {}
            )
            body = recall_handler(
                query,
                scope=first(params, "scope", "wiki") or "wiki",
                agent=first(params, "agent"),
                token_subject=token_subject,
                allowed_scopes=allowed_scopes,
                acting_for=acting_for,
                n=int_param(params, "n", 5),
                timeout_ms=int_param(params, "timeout_ms", 1500, min_value=MIN_TIMEOUT_MS, max_value=MAX_TIMEOUT_MS),
                context_sources=context_sources,
                context_source_allowlist=context_source_allowlist,
                include_read_receipt=read_receipt_enabled(first(params, "read_receipt")),
                **ceiling_kwargs,
            )
    except (TypeError, ValueError) as exc:
        return response(400, {"error": "bad_request", "message": str(exc), "contract_status": CONTRACT_STATUS})

    return response(200, body)
