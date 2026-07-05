from __future__ import annotations

from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"


def test_readme_has_copy_pasteable_install_and_smoke_commands():
    text = README.read_text(encoding="utf-8")
    assert "## Install (Verified E2E)" in text
    assert 'pip install "git+https://github.com/jeremyknows/memory-seam.git"' in text
    assert "## 60-Second Quickstart" in text
    assert "git clone https://github.com/jeremyknows/memory-seam.git" in text
    assert "cd memory-seam" in text
    assert "python3 -m pip install -e ." in text
    assert "python examples/quickstart_smoke.py" in text
    assert "python3 -m pytest -q" in text
    assert "python3 scripts/public_hygiene_scan.py" in text


def test_readme_quickstart_preserves_no_live_boundary_language():
    text = README.read_text(encoding="utf-8")
    quickstart = text.split("## 60-Second Quickstart", 1)[1].split("## Build Your Own Provider", 1)[0]
    required_boundary_terms = [
        "committed synthetic fixtures",
        "metadata-only",
        "no live reads",
        "raw fallbacks",
        "fail-closed",
        "service startup",
        "Runtime Registry consumption",
        "backend reads",
        "write/custody/reindex behavior",
    ]
    normalized_quickstart = " ".join(quickstart.split())
    for term in required_boundary_terms:
        assert term in normalized_quickstart


def test_readme_quickstart_documents_expected_context_and_recall_shape():
    text = README.read_text(encoding="utf-8")
    quickstart = text.split("## 60-Second Quickstart", 1)[1].split("## Build Your Own Provider", 1)[0]
    assert '"context"' in quickstart
    assert '"recall"' in quickstart
    assert '"receipt_verdict": "useful"' in quickstart
    assert '"read_backend_called": false' in quickstart
    assert '"runtime_registry_consumed": false' in quickstart
    assert '"write_custody_or_reindex": false' in quickstart


def test_readme_links_to_deep_docs_and_boundary_docs():
    text = README.read_text(encoding="utf-8")
    assert "[docs/README.md](docs/README.md)" in text
    assert "[adapter import boundary](docs/adapter-import-boundary.md)" in text
    assert "[package boundary](docs/package-boundary.md)" in text
