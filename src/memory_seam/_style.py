"""Tiny ANSI styling helpers for human CLI output."""

from __future__ import annotations

import os
import sys

RESET = "\033[0m"
_CODES = {
    "bold": "1",
    "dim": "2",
    "green": "32",
    "yellow": "33",
    "red": "31",
    "cyan": "36",
}


def enabled() -> bool:
    return bool(sys.stdout.isatty()) and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb"


def _wrap(text: object, code: str) -> str:
    value = str(text)
    if not enabled():
        return value
    return f"\033[{code}m{value}{RESET}"


def bold(text: object) -> str:
    return _wrap(text, _CODES["bold"])


def dim(text: object) -> str:
    return _wrap(text, _CODES["dim"])


def green(text: object) -> str:
    return _wrap(text, _CODES["green"])


def yellow(text: object) -> str:
    return _wrap(text, _CODES["yellow"])


def red(text: object) -> str:
    return _wrap(text, _CODES["red"])


def cyan(text: object) -> str:
    return _wrap(text, _CODES["cyan"])


__all__ = ["bold", "cyan", "dim", "enabled", "green", "red", "yellow"]
