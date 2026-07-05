"""OSS sanitization guard for the portable package surface.

Protective intent: the standalone package (and everything shipped with it to
wheel/sdist consumers) must never carry machine-specific residue from a
developer host — user-specific home paths or machine-bound HMAC key
labels. The repository-wide ``scripts/public_hygiene_scan.py`` already covers
broader release hygiene; this guard is the narrower, always-on pytest gate for
the portable surface specifically, so a regression fails the suite on every PR
rather than only during an ad hoc release check.

Scope: ``src/`` (the wheel package), ``examples/`` and ``scripts/`` (shipped in
the sdist and runnable as-is), and ``tests/fixtures/`` (the fixture JSON/data
the sdist ships). Private provenance docs are not part of the portable surface
and must stay outside public release artifacts.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PORTABLE_SURFACE_DIRS = (
    REPO_ROOT / "src",
    REPO_ROOT / "examples",
    REPO_ROOT / "scripts",
    REPO_ROOT / "tests" / "fixtures",
)
TEXT_SUFFIXES = {".py", ".md", ".toml", ".json", ".yml", ".yaml", ".txt", ".typed"}
GENERATED_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", "build", "dist"}

# Assembled from fragments so this guard file itself never contains the
# forbidden literal (and never trips the public hygiene scanner).
FORBIDDEN_HOME_PATH = "/" + "Users" + "/" + "watson"

# Any hmac_key_label value on the portable surface must read as synthetic
# fixture material, never as a binding to a specific operator machine.
HMAC_KEY_LABEL_VALUE = re.compile(
    r"hmac_key_label[\"'`]?\s*[:=]\s*[\"'`]([^\"'`]*)[\"'`]",
    re.IGNORECASE,
)
SAFE_HMAC_LABEL_MARKERS = ("synthetic", "fixture", "test", "example", "demo")
MACHINE_SPECIFIC_HMAC_MARKERS = ("watson", "macmini", "mac-mini", "mini-m4", "prod")


def iter_portable_text_files() -> Iterator[Path]:
    for base in PORTABLE_SURFACE_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if any(part in GENERATED_DIR_NAMES for part in path.parts):
                continue
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                yield path


def test_portable_surface_scan_covers_package_and_shipped_fixtures() -> None:
    """The guard must actually be scanning a real surface, not an empty set."""
    files = list(iter_portable_text_files())
    assert len(files) >= 40
    assert any(path.suffix == ".py" and path.is_relative_to(REPO_ROOT / "src") for path in files)
    assert any(path.suffix == ".json" for path in files)


def test_portable_surface_contains_no_user_specific_home_path() -> None:
    offenders: list[str] = []
    for path in iter_portable_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        if FORBIDDEN_HOME_PATH in text:
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert offenders == []


def test_portable_surface_hmac_key_labels_are_synthetic_not_machine_specific() -> None:
    offenders: list[str] = []
    for path in iter_portable_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in HMAC_KEY_LABEL_VALUE.finditer(text):
            value = match.group(1).lower()
            machine_specific = any(marker in value for marker in MACHINE_SPECIFIC_HMAC_MARKERS)
            recognizably_synthetic = any(marker in value for marker in SAFE_HMAC_LABEL_MARKERS)
            if machine_specific or not recognizably_synthetic:
                offenders.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {value}")
    assert offenders == []
