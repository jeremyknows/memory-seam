from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
L4_CLOSURE = REPO_ROOT / "docs" / "l4-closure-review.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"


def test_l4_closure_packet_cites_issue_pr_evidence_and_verifier_gate():
    text = L4_CLOSURE.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    required_terms = [
        "# L4 closure review packet",
        "L4 CLOSED",
        "ready for the next bounded design/planning tranche only",
        "Issue",
        "Primary PR evidence",
        "#21",
        "#44",
        "#46",
        "#69",
        "pytest -q",
        "python scripts/public_hygiene_scan.py",
        "python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py",
        "git diff --check",
        "Source cards and reportable artifacts reject unsafe raw/private fragments",
        "Synthetic usefulness/ranking fixtures simulate retrieval quality without live indexes",
        "Downstream migration/smoke docs preserve adapter-local, no-mutation boundaries",
    ]
    for term in required_terms:
        assert term in normalized


def test_l4_closure_packet_preserves_l5_l6_and_runtime_holds():
    normalized = " ".join(L4_CLOSURE.read_text(encoding="utf-8").split())

    required_holds = [
        "#6 L5/L6 unsupervised read ladder and write-custody companion",
        "service/listener activation",
        "credential/auth/env/keychain/OAuth/auth-file reads",
        "global Hermes/MCP/client/runtime configuration mutation",
        "Runtime Registry runtime consumption",
        "live/private source reads or source discovery",
        "unsupervised reads, cron/startup activation, canaries, provider/prod authority",
        "writes, custody, reindex",
        "repository visibility changes and package publication",
        "Atlas Gate movement",
    ]
    for term in required_holds:
        assert term in normalized

    forbidden_terms = [
        "twine upload",
        "gh repo edit --visibility public",
        "launchctl load",
        "crontab -e",
    ]
    for term in forbidden_terms:
        assert term not in normalized


def test_l4_closure_packet_is_discoverable_from_docs_index():
    index = DOCS_INDEX.read_text(encoding="utf-8")

    assert "l4-closure-review.md" in index
    assert "L4 closure packet" in index
