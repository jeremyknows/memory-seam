"""First-party local adapter implementations for Memory Seam."""

from .markdown import (
    LOCAL_MARKDOWN_ADAPTER_NAME,
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    MAX_SNIPPET_CHARS,
    LocalMarkdownAdapter,
)

__all__ = [
    "LOCAL_MARKDOWN_ADAPTER_NAME",
    "LocalMarkdownAdapter",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
