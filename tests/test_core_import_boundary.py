from __future__ import annotations

import importlib
from pathlib import Path


def test_package_imports_core_modules():
    import memory_seam

    for name in ["contracts", "policy", "descriptors", "receipts", "router", "testing"]:
        assert importlib.import_module(f"memory_seam.{name}")
    assert hasattr(memory_seam, "SubjectPolicy")


def test_core_has_no_atlas_adapter_imports():
    core_dir = Path(__file__).parents[1] / "src" / "memory_seam"
    forbidden = (
        "from backends import memory",
        "from backends import wiki",
        "from backends import memory_seam",
        "from backends.memory_seam_",
        "FastMCP",
        "ATLAS_QUERY_MCP_LOCAL_AUTHORITY",
        "memory_seam_service",
        "memory_seam_mcp_authority",
        "memory_seam_control_plane",
    )
    for path in core_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, f"forbidden Atlas adapter dependency in {path.name}: {needle}"
