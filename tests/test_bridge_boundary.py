from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_bridge_package_boundary_exists() -> None:
    bridge = REPO_ROOT / "bridge"

    assert bridge.is_dir()
    assert (bridge / "pyproject.toml").is_file()
    assert (bridge / "src" / "memory_seam_mcp" / "__init__.py").is_file()
    assert (bridge / "src" / "memory_seam_mcp" / "server.py").is_file()
    assert (bridge / "tests").is_dir()


def test_core_package_keeps_empty_dependency_boundary() -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "\ndependencies = []\n" in text


def test_bridge_declares_own_dependencies_and_core_dependency() -> None:
    text = (REPO_ROOT / "bridge" / "pyproject.toml").read_text(encoding="utf-8")

    assert 'name = "memory-seam-mcp"' in text
    assert '"memory-seam @ git+https://github.com/jeremyknows/memory-seam.git",' in text
    assert '"mcp",' in text
