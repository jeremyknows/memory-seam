from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
PACKAGING = REPO_ROOT / "docs" / "packaging.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
DELETED_PUBLIC_PROCESS_DOCS = (
    REPO_ROOT / "docs" / ("release-decision-" + "hold-packet.md"),
    REPO_ROOT / "docs" / ("release-" + "readiness.md"),
)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_pre_release_process_docs_are_omitted_from_public_tree() -> None:
    for path in DELETED_PUBLIC_PROCESS_DOCS:
        assert not path.exists()

    docs_index = normalized(DOCS_INDEX)
    readme = normalized(README)
    changelog = normalized(CHANGELOG)
    for stale_ref in ("release-decision-" + "hold-packet.md", "release-" + "readiness.md"):
        assert stale_ref not in docs_index
        assert stale_ref not in readme
        assert stale_ref not in changelog


def test_public_release_posture_is_explicit() -> None:
    readme = normalized(README)
    changelog = normalized(CHANGELOG)
    packaging = normalized(PACKAGING)

    assert "Public v0.1.0 source package under Apache-2.0" in readme
    assert "## v0.1.0" in changelog
    assert "Initial public release baseline" in changelog
    assert "Memory Seam v0.1.0 is packaged" in packaging
    assert "License: Apache-2.0" in packaging


def test_public_release_docs_preserve_no_live_and_write_custody_holds() -> None:
    combined = " ".join(
        normalized(path)
        for path in (
            README,
            CHANGELOG,
            PACKAGING,
            DOCS_INDEX,
        )
    )

    required_terms = [
        "no-live/read-only core",
        "live adapter implementation",
        "service/listener activation",
        "credentials",
        "runtime registry consumption",
        "unsupervised reads",
        "writes/custody/reindex",
        "Runtime Registry consumption",
        "provider/prod/canary authority",
    ]
    for term in required_terms:
        assert term in combined


def test_public_release_docs_do_not_claim_private_staging_or_release_hold() -> None:
    docs = [README, CHANGELOG, PACKAGING, DOCS_INDEX]
    forbidden_claims = [
        "private " + "staging",
        "private-" + "staging",
        "release " + "held",
        "Release is **" + "HELD**",
        "repository remains private",
        "license posture is unresolved",
        "do not publish to PyPI",
        "visibility remains private",
    ]
    for path in docs:
        text = normalized(path)
        for claim in forbidden_claims:
            assert claim not in text
