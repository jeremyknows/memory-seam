#!/usr/bin/env python3
"""Sync canonical memory-librarian skills into the Claude Code plugin shell."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / "src" / "memory_seam" / "agent_packages" / "memory_librarian" / "skills"
PLUGIN_SKILLS = ROOT / "integrations" / "claude-plugin" / "skills"


def sync() -> list[Path]:
    """Copy canonical skill SKILL.md files into the plugin skills directory."""
    if not SOURCE_SKILLS.is_dir():
        raise FileNotFoundError(f"canonical skills directory not found: {SOURCE_SKILLS}")

    PLUGIN_SKILLS.mkdir(parents=True, exist_ok=True)
    source_names = {path.name for path in SOURCE_SKILLS.iterdir() if path.is_dir()}

    for stale in sorted(path for path in PLUGIN_SKILLS.iterdir() if path.is_dir() and path.name not in source_names):
        shutil.rmtree(stale)

    copied: list[Path] = []
    for source_dir in sorted(path for path in SOURCE_SKILLS.iterdir() if path.is_dir()):
        source_file = source_dir / "SKILL.md"
        if not source_file.is_file():
            raise FileNotFoundError(f"canonical skill missing SKILL.md: {source_dir}")
        target_dir = PLUGIN_SKILLS / source_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "SKILL.md"
        shutil.copyfile(source_file, target_file)
        copied.append(target_file)

    return copied


def main() -> int:
    copied = sync()
    for path in copied:
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
