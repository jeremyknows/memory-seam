from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "public-private-hygiene-inventory.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized_doc() -> str:
    return " ".join(DOC.read_text(encoding="utf-8").split())


def test_public_private_hygiene_inventory_names_target_surfaces_and_risk_classes():
    text = normalized_doc()

    required_terms = [
        "# Public/private hygiene inventory",
        "Inventory PASS",
        "Root/package docs",
        "Documentation index and hygiene docs",
        "Runtime/contracts notes",
        "Tests/scripts/examples",
        "Omitted internal material",
        "Private absolute paths",
        "raw private source text",
        "credentials",
        "auth/env/keychain material",
        "token-shaped strings",
        "raw platform IDs",
        "raw query payloads",
        "private correlation refs",
    ]
    for term in required_terms:
        assert term in text


def test_public_private_hygiene_inventory_documents_scanner_targets_and_safe_exceptions():
    text = normalized_doc()

    required_terms = [
        "python scripts/public_hygiene_scan.py",
        "Host-private paths",
        "Raw platform identifiers",
        "Token-like strings",
        "Adapter/source-floor provenance labels and removed-doc references",
        "GitHub issue-comment URLs",
        "Internal operator/provenance terms",
        "listed in `scripts/public_hygiene_scan.py`",
        "Private provenance has no public-tree quarantine",
        "internal planning and provenance documents are maintained privately and omitted from this repository",
        "Generated caches and dependency/build artifacts are skipped",
        "scripts/public_hygiene_scan.py may include its own pattern examples",
    ]
    for term in required_terms:
        assert term in text


def test_public_private_hygiene_inventory_preserves_held_authority():
    text = normalized_doc()

    required_terms = [
        "does not authorize package publication automation",
        "service/listener activation",
        "credential/auth/env/keychain reads",
        "Runtime Registry consumption",
        "live/private source reads",
        "source discovery",
        "unsupervised reads",
        "writes/custody/reindex behavior",
        "provider/prod/canary authority",
        "production authority changes",
        "runtime/write authority remains held unless explicitly approved by a maintainer",
    ]
    for term in required_terms:
        assert term in text

    forbidden_terms = [
        "twine upload",
        "gh repo edit --visibility public",
        "crontab -e",
        "Runtime Registry endpoint",
    ]
    for term in forbidden_terms:
        assert term not in text


def test_public_private_hygiene_inventory_records_trust_boundary_without_new_reads():
    text = normalized_doc()

    required_terms = [
        "inventory/scanner documentation only",
        "does not add a denial path that can materialize source/provider/file/stat/backend reads",
        "zero provider/backend/read/stat calls",
        "Public artifacts for this inventory contain only issue/PR numbers, command names, file names, booleans, safe class names, and aggregate policy statements",
        "pytest -q tests/test_public_private_hygiene_inventory.py tests/test_public_hygiene_scan.py",
    ]
    for term in required_terms:
        assert term in text


def test_public_private_hygiene_inventory_is_discoverable_from_docs():
    docs_index = DOCS_INDEX.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    inventory = CONTRACT_TEST_INVENTORY.read_text(encoding="utf-8")

    assert "public-private-hygiene-inventory.md" in docs_index
    assert "public/private hygiene inventory" in readme
    assert "tests/test_public_private_hygiene_inventory.py" in inventory
    assert "Public/private hygiene inventory" in inventory
