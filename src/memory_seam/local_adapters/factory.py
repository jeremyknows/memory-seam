"""Factory for first-party local adapter implementations."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable

from memory_seam.adapters import SourceAdapter
from memory_seam.local_adapters.git_tree import LocalGitTreeAdapter
from memory_seam.local_adapters.jsonl_export import LocalJsonlExportAdapter
from memory_seam.local_adapters.markdown import LocalMarkdownAdapter
from memory_seam.local_adapters.plaintext import LocalPlainTextAdapter
from memory_seam.local_adapters.sqlite_notes import LocalSqliteAdapter

AdapterBuilder = Callable[[str | Path, Mapping[str, Any]], SourceAdapter]

SQLITE_REQUIRED_KWARGS = ("table", "title_column", "body_column")


def _markdown(root: str | Path, config: Mapping[str, Any]) -> SourceAdapter:
    return LocalMarkdownAdapter(root)


def _plaintext(root: str | Path, config: Mapping[str, Any]) -> SourceAdapter:
    extension_allowlist = config.get("extension_allowlist")
    if extension_allowlist is None:
        return LocalPlainTextAdapter(root)
    return LocalPlainTextAdapter(root, extension_allowlist=extension_allowlist)


def _jsonl(root: str | Path, config: Mapping[str, Any]) -> SourceAdapter:
    return LocalJsonlExportAdapter(
        root,
        title_field=_optional_str(config.get("title_field")),
        body_field=_optional_str(config.get("body_field")),
    )


def _git_tree(root: str | Path, config: Mapping[str, Any]) -> SourceAdapter:
    extension_allowlist = config.get("extension_allowlist")
    if extension_allowlist is None:
        return LocalGitTreeAdapter(root)
    return LocalGitTreeAdapter(root, extension_allowlist=extension_allowlist)


def _sqlite(root: str | Path, config: Mapping[str, Any]) -> SourceAdapter:
    table = _required_str(config, "table")
    title_column = _required_str(config, "title_column")
    body_column = _required_str(config, "body_column")
    kwargs: dict[str, Any] = {
        "db_path": root,
        "table": table,
        "title_column": title_column,
        "body_column": body_column,
    }
    for key in ("id_column", "row_cap", "statement_op_limit"):
        if key in config and config[key] is not None:
            kwargs[key] = config[key]
    return LocalSqliteAdapter(**kwargs)


LOCAL_ADAPTERS: dict[str, AdapterBuilder] = {
    "markdown": _markdown,
    "plaintext": _plaintext,
    "jsonl": _jsonl,
    "git-tree": _git_tree,
    "sqlite": _sqlite,
}


def valid_local_adapter_names() -> tuple[str, ...]:
    """Return supported local adapter names in CLI display order."""

    return tuple(LOCAL_ADAPTERS)


def valid_local_adapter_list() -> str:
    """Return a human-readable supported local adapter list."""

    return ", ".join(valid_local_adapter_names())


def build_local_adapter(adapter: str, root: str | Path, **config: Any) -> SourceAdapter:
    """Build a first-party local SourceAdapter by public adapter name."""

    try:
        builder = LOCAL_ADAPTERS[adapter]
    except KeyError as exc:
        raise ValueError(f"unknown local adapter {adapter!r}; valid adapters: {valid_local_adapter_list()}") from exc
    return builder(root, config)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _required_str(config: Mapping[str, Any], key: str) -> str:
    value = config.get(key)
    if value is None or str(value).strip() == "":
        raise ValueError(
            "sqlite adapter requires explicit kwargs: "
            + ", ".join(SQLITE_REQUIRED_KWARGS)
            + f"; missing {key}"
        )
    return str(value)


__all__ = [
    "LOCAL_ADAPTERS",
    "SQLITE_REQUIRED_KWARGS",
    "build_local_adapter",
    "valid_local_adapter_list",
    "valid_local_adapter_names",
]
