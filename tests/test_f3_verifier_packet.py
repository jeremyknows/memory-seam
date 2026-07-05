from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "f3-verifier-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_f3_verifier_packet_is_discoverable_from_indexes():
    packet_name = "f3-verifier-packet.md"

    assert PACKET.exists()
    assert packet_name in DOCS_INDEX.read_text(encoding="utf-8")
    assert packet_name in README.read_text(encoding="utf-8")
    assert "tests/test_f3_verifier_packet.py" in CONTRACT_TEST_INVENTORY.read_text(
        encoding="utf-8"
    )


def test_f3_verifier_packet_records_issue_pr_and_ci_evidence():
    text = _normalized(PACKET)

    required_terms = [
        "F3 PASS",
        "8e23e9f Add final L4 closure review packet (#70)",
        "86cf112 Add F2 verifier packet (#91)",
        "2394853 Add source-card usefulness proof packet (#93)",
        "`#77` F3.01 manual pull dogfood harness/runbook",
        "`#92` Add F3 manual pull dogfood runbook",
        "2eb0310f50a585915698de7d9c7a4cc448280386",
        "`#78` F3.02 source-card usefulness proof packet",
        "`#93` Add source-card usefulness proof packet",
        "23948532e73e9f4850ffb65766700b5afc4a7468",
        "`#79` F3.03 verifier packet",
        "pytest (3.10)",
        "pytest (3.11)",
        "pytest (3.12)",
    ]
    for term in required_terms:
        assert term in text


def test_f3_verifier_packet_records_full_verifier_and_issue_state():
    text = _normalized(PACKET)

    required_terms = [
        "pytest -q",
        "python scripts/public_hygiene_scan.py",
        "python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py",
        "git diff --check",
        "pytest -q tests/test_f3_verifier_packet.py",
        "`#79` F3.03: in progress by this packet",
        "`#80` F4.01: next eligible target only after `#79` closes/PASS",
        "`#81` F4.02 and `#82` F4.03: locked behind the preceding F4 issue order",
        "`#83` F10.01 through `#85` F10.03: locked behind `#82` closing/PASS",
        "`#6` L5/L6: HOLD unless Jeremy explicitly unholds it",
    ]
    for term in required_terms:
        assert term in text


def test_f3_verifier_packet_preserves_trust_boundary_and_holds():
    text = _normalized(PACKET)

    required_terms = [
        "synthetic_safe_content_provider()",
        "committed synthetic fixtures only",
        "source_card_count",
        "report-safe source-card IDs",
        "no raw fallback",
        "raw_fallback_used=false",
        "read_backend_called=false",
        "service_started=false",
        "runtime_registry_consumed=false",
        "write_custody_or_reindex=false",
        "denial before source/provider/file/stat/backend reads",
        "zero counters or equivalent monkeypatch/spy assertions",
        "raw private source text",
        "credentials, auth/env/keychain material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "private correlation references",
        "Startup injection and cron",
        "Broad recall authority",
        "Service/listener activation or installation",
        "Credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry runtime consumption",
        "Live/private source reads or source discovery",
        "Unsupervised reads, canaries, provider/prod authority",
        "Writes, custody, reindex, thread-retirement behavior",
        "Repository visibility changes and package publication",
        "Atlas Gate movement or production-authoritative claims",
    ]
    for term in required_terms:
        assert term in text

    forbidden_terms = [
        "/" + "Users" + "/",
        "twine upload",
        "gh repo edit --visibility public",
        "launchctl load",
        "crontab -e",
    ]
    for term in forbidden_terms:
        assert term not in text


def test_f3_verifier_packet_unlocks_only_no_service_identity_lane():
    text = _normalized(PACKET)

    required_terms = [
        "Proceed to **`#80` F4.01: no-service identity negative matrix**",
        "after this packet lands, local verification passes, GitHub CI passes, and issue `#79` closes/PASS",
        "in-process verifier semantics",
        "forged-subject/wrong-audience/expired-token/query-body-mismatch/confused-deputy negatives",
        "denial before provider/source/file/stat/backend reads",
        "no persistent listener",
        "no credential store reads",
        "no live/private source reads",
        "no Runtime Registry runtime consumption",
        "no writes/custody/reindex",
        "no provider/prod/canary authority",
        "no Atlas Gate movement",
        "no repository visibility or package-publication decision",
    ]
    for term in required_terms:
        assert term in text
