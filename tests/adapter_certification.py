from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import quote

from memory_seam import (
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    SourceAdapter,
    StaticIdentityVerifier,
)

ALLOWED_RETRIEVAL_BACKENDS = frozenset(
    {
        "metadata_only",
        "committed_fixture",
        "recursive_markdown_scan",
        "filesystem",
        "supervised-one-read-source-card",
        "supervised-report-safe-source-card-callback",
    }
)

POSTURE_FALSE_FIELDS = (
    "read_backend_called",
    "service_started",
    "runtime_registry_consumed",
    "raw_fallback_used",
    "write_custody_or_reindex",
)


@dataclass(frozen=True)
class AdapterCertificationConfig:
    context_include: tuple[str, ...] = ("memory", "project")
    recall_query: str = "memory seam certification"
    zero_match_query: str = "__memory_seam_adapter_certification_zero_match__"
    recall_scope: str = "wiki"
    recall_n: int = 3
    token_subject: str = "agent:adapter-certification"
    snippet_char_limit: int = 200
    allowed_retrieval_backends: frozenset[str] = ALLOWED_RETRIEVAL_BACKENDS


def assert_source_adapter_certified(
    adapter: SourceAdapter,
    fixture_root: str | Path,
    *,
    config: AdapterCertificationConfig = AdapterCertificationConfig(),
) -> None:
    """Reusable pytest assertion suite for a read-only SourceAdapter."""

    root = Path(fixture_root).expanduser().resolve()

    context_items = adapter.context_items(
        include=config.context_include,
        token_subject=config.token_subject,
    )
    recall_items = adapter.recall_items(
        config.recall_query,
        scope=config.recall_scope,
        token_subject=config.token_subject,
        n=config.recall_n,
    )
    zero_match_items = adapter.recall_items(
        config.zero_match_query,
        scope=config.recall_scope,
        token_subject=config.token_subject,
        n=config.recall_n,
    )

    assert isinstance(context_items, list)
    assert isinstance(recall_items, list)
    assert zero_match_items == []

    _assert_items_safe(
        [*context_items, *recall_items],
        root=root,
        snippet_char_limit=config.snippet_char_limit,
        allowed_retrieval_backends=config.allowed_retrieval_backends,
    )

    provider = AdapterMemorySeamProvider(adapter)
    _assert_posture_flags_fail_closed(provider.health())

    disabled_runtime = LocalReadOnlyRuntime(provider=provider)
    disabled = disabled_runtime.handle(RuntimeRequest("GET", "/recall?query=held&scope=wiki"))
    assert disabled["status_code"] == 503
    _assert_runtime_receipt_fail_closed(disabled["body"]["runtime"])

    enabled_runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(
            subject=config.token_subject,
            allowed_scopes=frozenset({"context", "wiki", "diary"}),
        ),
    )
    target = (
        "/recall?"
        f"query={quote(config.recall_query)}"
        f"&scope={quote(config.recall_scope)}"
        f"&n={int(config.recall_n)}"
    )
    allowed = enabled_runtime.handle(RuntimeRequest("GET", target))
    assert allowed["status_code"] == 200
    _assert_posture_flags_fail_closed(allowed["body"])
    _assert_runtime_receipt_fail_closed(allowed["body"]["runtime"])
    _assert_items_safe(
        allowed["body"]["items"],
        root=root,
        snippet_char_limit=config.snippet_char_limit,
        allowed_retrieval_backends=config.allowed_retrieval_backends,
    )


def _assert_items_safe(
    items: Iterable[Mapping[str, Any]],
    *,
    root: Path,
    snippet_char_limit: int,
    allowed_retrieval_backends: frozenset[str],
) -> None:
    for item in items:
        assert isinstance(item, Mapping)
        assert str(root) not in repr(dict(item))
        retrieval_backend = item.get("retrieval_backend")
        assert isinstance(retrieval_backend, str)
        assert retrieval_backend in allowed_retrieval_backends
        snippet = item.get("snippet")
        if snippet is not None:
            assert len(str(snippet)) <= snippet_char_limit
        for key, value in _walk_values(item):
            if isinstance(value, str):
                assert str(root) not in value
                assert not _looks_like_absolute_path(value), f"{key} contains absolute path: {value}"
                if _is_path_key(key):
                    _assert_relative_path(value, root=root)


def _assert_posture_flags_fail_closed(payload: Mapping[str, Any]) -> None:
    for field in POSTURE_FALSE_FIELDS:
        if field in payload:
            assert payload[field] is False


def _assert_runtime_receipt_fail_closed(receipt: Mapping[str, Any]) -> None:
    assert receipt["service_started"] is False
    assert receipt["runtime_registry_consumed"] is False
    assert receipt["write_custody_or_reindex"] is False
    assert receipt["audit_receipt"]["persisted"] is False
    assert receipt["audit_receipt"]["raw_content_persisted"] is False


def _walk_values(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_key = str(key)
            path = child_key if not prefix else f"{prefix}.{child_key}"
            yield from _walk_values(child, path)
    elif isinstance(value, list | tuple):
        for index, child in enumerate(value):
            yield from _walk_values(child, f"{prefix}[{index}]")
    else:
        yield prefix, value


def _is_path_key(key: str) -> bool:
    leaf = key.rsplit(".", 1)[-1].lower()
    return leaf == "path" or leaf.endswith("_path") or leaf.endswith("path")


def _looks_like_absolute_path(value: str) -> bool:
    if not value:
        return False
    if value.startswith(("http://", "https://", "memory_seam://")):
        return False
    return PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute()


def _assert_relative_path(value: str, *, root: Path) -> None:
    if value == "":
        return
    assert "\\" not in value
    rel = PurePosixPath(value)
    assert not rel.is_absolute()
    assert ".." not in rel.parts
    assert rel.as_posix() == value
    candidate = root.joinpath(*rel.parts)
    if candidate.exists():
        candidate.resolve(strict=True).relative_to(root)
    else:
        candidate.resolve(strict=False).relative_to(root)


__all__ = [
    "ALLOWED_RETRIEVAL_BACKENDS",
    "AdapterCertificationConfig",
    "POSTURE_FALSE_FIELDS",
    "assert_source_adapter_certified",
]
