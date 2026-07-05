from __future__ import annotations

from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"


def test_readme_operator_quickstart_has_copy_pasteable_install_and_smoke_commands():
    text = README.read_text(encoding="utf-8")
    assert "## Operator quickstart" in text
    assert "git clone https://github.com/jeremyknows/memory-seam.git" in text
    assert "cd memory-seam" in text
    assert "python -m pip install -e ." in text
    assert "python examples/quickstart_smoke.py" in text
    assert "pytest -q" in text
    assert "python scripts/public_hygiene_scan.py" in text
    assert "python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py" in text


def test_readme_operator_quickstart_preserves_no_live_boundary_language():
    text = README.read_text(encoding="utf-8")
    quickstart = text.split("## Operator quickstart", 1)[1].split("## Development", 1)[0]
    required_boundary_terms = [
        "fully synthetic",
        "does not start a service",
        "discover local sources",
        "call a network",
        "consume Runtime Registry",
        "read private/live data",
        "fall back to raw reads",
        "publish packages",
        "write/custody/reindex behavior",
        "metadata-only receipts",
        "committed synthetic fixtures",
    ]
    normalized_quickstart = " ".join(quickstart.split())
    for term in required_boundary_terms:
        assert term in normalized_quickstart


def test_readme_operator_quickstart_documents_expected_context_and_recall_shape():
    text = README.read_text(encoding="utf-8")
    quickstart = text.split("## Operator quickstart", 1)[1].split("## Development", 1)[0]
    assert '"context"' in quickstart
    assert '"recall"' in quickstart
    assert '"receipt_verdict": "useful"' in quickstart
    assert '"read_backend_called": false' in quickstart
    assert '"runtime_registry_consumed": false' in quickstart
    assert '"write_custody_or_reindex": false' in quickstart
