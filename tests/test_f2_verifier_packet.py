from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "docs" / "f2-verifier-packet.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
README = REPO_ROOT / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_f2_verifier_packet_is_discoverable_from_indexes():
    packet_name = "f2-verifier-packet.md"

    assert PACKET.exists()
    assert packet_name in DOCS_INDEX.read_text(encoding="utf-8")
    assert packet_name in README.read_text(encoding="utf-8")
    assert "tests/test_f2_verifier_packet.py" in CONTRACT_TEST_INVENTORY.read_text(
        encoding="utf-8"
    )


def test_f2_verifier_packet_records_issue_pr_and_ci_evidence():
    text = _normalized(PACKET)

    required_terms = [
        "F2 PASS",
        "8e23e9f Add final L4 closure review packet (#70)",
        "6e9b05a Add F2 policy semantics decision note (#90)",
        "`#71` F2.01 schema contract consolidation",
        "`#86` Add portable schema contract consolidation",
        "9072d9514fc177cfa8b0cf9932a191573ea0b970",
        "`#72` F2.02 denial fixture matrix",
        "`#87` Add denial fixture matrix",
        "c7c34448afeef8fb9933cb9d891a3656952dd3a1",
        "`#73` F2.03 router parser and redaction edge cases",
        "`#88` Add router redaction edge-case tests",
        "58a2b88966a9d95f46cbfcd2e01bc81cc46b94d9",
        "`#74` F2.04 adapter import-boundary compatibility",
        "`#89` Add adapter import-boundary compatibility proof",
        "eed1c4389a7a418e49d5395b13656d29d127dda6",
        "`#75` F2.05 policy semantics decision note",
        "`#90` Add F2 policy semantics decision note",
        "6e9b05a281b048648a30f6a34b16b17d5d98db21",
        "pytest (3.10)",
        "pytest (3.11)",
        "pytest (3.12)",
    ]
    for term in required_terms:
        assert term in text


def test_f2_verifier_packet_records_full_verifier_and_issue_state():
    text = _normalized(PACKET)

    required_terms = [
        "pytest -q",
        "python scripts/public_hygiene_scan.py",
        "python -m py_compile src/memory_seam/*.py tests/*.py scripts/*.py examples/*.py",
        "git diff --check",
        "pytest -q tests/test_f2_verifier_packet.py",
        "`#76` F2.06: in progress by this packet",
        "`#77` F3.01: next eligible target only after `#76` closes/PASS",
        "`#80` F4.01 through `#82` F4.03: locked behind `#79` closing/PASS",
        "`#83` F10.01 through `#85` F10.03: locked behind `#82` closing/PASS",
        "`#6` L5/L6: HOLD unless Jeremy explicitly unholds it",
    ]
    for term in required_terms:
        assert term in text


def test_f2_verifier_packet_preserves_trust_boundary_and_holds():
    text = _normalized(PACKET)

    required_terms = [
        "denies blank/missing grants and unknown families before source stat/backend/provider reads",
        "zero source-read, stat, backend, and provider counters",
        "before handler/provider/source/backend reads",
        "descriptor registration and grant authority as an intersection, not a union",
        "raw private source text",
        "credentials, auth/env/keychain material",
        "raw platform IDs",
        "private absolute paths",
        "raw query payloads",
        "private correlation references",
        "Service/listener activation or installation",
        "Credential/auth/env/keychain/OAuth/auth-file reads",
        "Runtime Registry runtime consumption",
        "Live/private source reads or source discovery",
        "Unsupervised reads, cron/startup activation, canaries, provider/prod authority",
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


def test_f2_verifier_packet_unlocks_only_supervised_f3_design_lane():
    text = _normalized(PACKET)

    required_terms = [
        "Proceed to **`#77` F3.01: manual pull dogfood harness/runbook**",
        "after this packet lands, local verification passes, GitHub CI passes, and issue `#76` closes/PASS",
        "manual, read-only, source-card-first",
        "no startup injection",
        "no cron",
        "no broader recall authority",
        "no writes/custody/reindex",
        "no service/listener",
        "no Runtime Registry runtime consumption",
        "no provider/prod/canary",
        "no Atlas Gate movement",
        "no repository visibility or package-publication decision",
    ]
    for term in required_terms:
        assert term in text
