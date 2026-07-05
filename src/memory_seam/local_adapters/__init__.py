"""First-party local adapter implementations for Memory Seam."""

from .factory import LOCAL_ADAPTERS, build_local_adapter, valid_local_adapter_list, valid_local_adapter_names
from .git_tree import LOCAL_GIT_TREE_ADAPTER_NAME, LocalGitTreeAdapter
from .jsonl_export import LOCAL_JSONL_EXPORT_ADAPTER_NAME, LocalJsonlExportAdapter
from .markdown import (
    LOCAL_MARKDOWN_ADAPTER_NAME,
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    MAX_SNIPPET_CHARS,
    LocalMarkdownAdapter,
)
from .plaintext import LOCAL_PLAINTEXT_ADAPTER_NAME, LocalPlainTextAdapter
from .sqlite_notes import LOCAL_SQLITE_ADAPTER_NAME, LocalSqliteAdapter

__all__ = [
    "LOCAL_ADAPTERS",
    "LOCAL_GIT_TREE_ADAPTER_NAME",
    "LOCAL_JSONL_EXPORT_ADAPTER_NAME",
    "LOCAL_MARKDOWN_ADAPTER_NAME",
    "LOCAL_PLAINTEXT_ADAPTER_NAME",
    "LOCAL_SQLITE_ADAPTER_NAME",
    "LocalGitTreeAdapter",
    "LocalJsonlExportAdapter",
    "LocalMarkdownAdapter",
    "LocalPlainTextAdapter",
    "LocalSqliteAdapter",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
    "build_local_adapter",
    "valid_local_adapter_list",
    "valid_local_adapter_names",
]
