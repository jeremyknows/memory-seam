from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS = REPO_ROOT / "src" / "memory_seam" / "agent_packages" / "memory_librarian" / "skills"
PLUGIN_ROOT = REPO_ROOT / "integrations" / "claude-plugin"
PLUGIN_SKILLS = PLUGIN_ROOT / "skills"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_claude_plugin_manifest_matches_official_root_layout():
    plugin_meta_dir = PLUGIN_ROOT / ".claude-plugin"
    manifest = json.loads((plugin_meta_dir / "plugin.json").read_text(encoding="utf-8"))

    assert manifest == {
        "name": "memory-seam",
        "description": "receipt-first memory boundary — recall over your own notes with receipts, via the librarian skills + MCP bridge",
        "version": "0.1.0",
        "author": {"name": "Jeremy Knows"},
        "homepage": "https://github.com/jeremyknows/memory-seam",
        "license": "Apache-2.0",
    }
    assert sorted(path.name for path in plugin_meta_dir.iterdir()) == ["plugin.json"]
    assert (PLUGIN_ROOT / "skills").is_dir()
    assert (PLUGIN_ROOT / ".mcp.json").is_file()


def test_claude_plugin_mcp_config_uses_plain_root_default():
    config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert config == {
        "mcpServers": {
            "memory-seam-mcp": {
                "command": "memory-seam-mcp",
                "args": ["--root", "./notes"],
            }
        }
    }


def test_claude_plugin_skills_match_canonical_packaged_skills():
    canonical = {
        path.parent.name: sha256(path)
        for path in sorted(CANONICAL_SKILLS.glob("*/SKILL.md"))
    }
    plugin = {
        path.parent.name: sha256(path)
        for path in sorted(PLUGIN_SKILLS.glob("*/SKILL.md"))
    }

    assert plugin == canonical
