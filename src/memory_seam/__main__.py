"""Module entrypoint for ``python -m memory_seam``."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
