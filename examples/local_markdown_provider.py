#!/usr/bin/env python3
"""Compatibility shim for the packaged local markdown adapter."""

from __future__ import annotations

from memory_seam.local_adapters.markdown import (
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    MAX_SNIPPET_CHARS,
    LocalMarkdownAdapter,
)

LocalMarkdownProvider = LocalMarkdownAdapter

__all__ = [
    "LocalMarkdownAdapter",
    "LocalMarkdownProvider",
    "MAX_FILE_BYTES",
    "MAX_SCAN_FILES",
    "MAX_SNIPPET_CHARS",
]
