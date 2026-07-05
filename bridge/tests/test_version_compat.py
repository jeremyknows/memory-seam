from __future__ import annotations

import pytest

from memory_seam_mcp import BRIDGE_VERSION, COMPATIBLE_CORE
from memory_seam_mcp import server as bridge_server


def test_bridge_declares_core_compatibility_contract() -> None:
    assert BRIDGE_VERSION == "0.1.0"
    assert COMPATIBLE_CORE == ">=0.1.0,<0.2"


def test_core_compatibility_warns_for_minor_skew(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(bridge_server, "_installed_core_version", lambda: "0.2.0")

    bridge_server.check_core_compatibility()

    captured = capsys.readouterr()
    assert "WARNING: memory-seam-mcp: installed memory-seam 0.2.0 is outside" in captured.err
    assert "continuing because major versions match" in captured.err


def test_core_compatibility_fails_for_major_skew(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bridge_server, "_installed_core_version", lambda: "1.0.0")

    with pytest.raises(RuntimeError, match="installed memory-seam 1.0.0 is outside"):
        bridge_server.check_core_compatibility()
