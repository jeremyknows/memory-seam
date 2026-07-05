"""Display sanitizers for terminal-facing Memory Seam output."""

from __future__ import annotations

import re

_OSC_RE = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
_CSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_ESC_RE = re.compile(r"\x1b[@-_][0-?]*[ -/]*[@-~]?")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
_BIDI_RE = re.compile("[\u202a-\u202e\u2066-\u2069]")
_NEWLINE_RE = re.compile(r"[\r\n\t]+")
_SPACE_RE = re.compile(r" {2,}")


def sanitize_display(text: object) -> str:
    """Return a single-line string safe for human terminal display."""

    value = str(text)
    value = _OSC_RE.sub("", value)
    value = _CSI_RE.sub("", value)
    value = _ESC_RE.sub("", value)
    value = _NEWLINE_RE.sub(" ", value)
    value = _CONTROL_RE.sub("", value)
    value = _BIDI_RE.sub("", value)
    return _SPACE_RE.sub(" ", value).strip()


__all__ = ["sanitize_display"]
