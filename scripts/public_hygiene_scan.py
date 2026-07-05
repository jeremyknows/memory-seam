#!/usr/bin/env python3
"""Conservative public-readiness hygiene scan for the standalone repo.

This is intentionally stricter than normal development habits. It fails on
host-private paths, raw platform IDs, obvious token-like strings, private
issue-comment URLs, and deployment-specific provenance references.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED_CACHE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "site-packages",
}
TEXT_SUFFIXES = {".md", ".py", ".toml", ".yml", ".yaml", ".txt", ".json"}
L6V_SUPERVISED_PROOF_ARTIFACT_SUFFIXES = {".json", ".yml", ".yaml", ".txt"}
MAC_USER_PATH_PATTERN = "/" + "Users" + r"/[A-Za-z0-9._-]+"
INTERNAL_OPERATOR_TERMS = (
    "Example agent label",
    "Example operator poke",
    "Example harvest label",
    "operator directive",
    "stewardship-transition",
    "Example-stewardship",
)
PATTERNS = {
    "host_private_path": re.compile(
        r"(?:" + MAC_USER_PATH_PATTERN + r"|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+|/private/var/folders)"
    ),
    "platform_identifier": re.compile(r"\b(?:[1-9][0-9]{16,20}|[CDGUTW][0-9][A-Z0-9]{8,})\b"),
    "token_like": re.compile(
        r"\b(?:ghp|gho|github_pat|sk-[A-Za-z0-9]|xox[baprs]-)[A-Za-z0-9_\-]{12,}\b|\bAKIA[0-9A-Z]{16}\b"
    ),
    "atlas_source_floor": re.compile(r"example-source@[0-9a-f]{7,40}|example-source `origin/main`"),
    "docs_atlas_source_reference": re.compile(r"docs/atlas-source|atlas-source"),
    "internal_baton_reference": re.compile(r"\b(?:master-baton|OSS pivot baton|atlas-source)\b", re.IGNORECASE),
    "github_issue_comment_url": re.compile(
        r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/[0-9]+#issuecomment-[0-9]+"
    ),
    "internal_operator_term": re.compile("|".join(re.escape(term) for term in INTERNAL_OPERATOR_TERMS)),
}

L6V_SUPERVISED_PROOF_SAFE_REFS = {
    "descriptor_ref": re.compile(r"^synthetic_descriptor:l6v-report-safe-[a-z0-9-]+$"),
    "source_card_ref": re.compile(r"^synthetic_source_card:l6v-report-safe-[a-z0-9-]+$"),
}
L6V_SUPERVISED_PROOF_FALSE_ONLY_FIELDS = {
    "allowed",
    "allowed_true_route_present",
    "callbacks_invoked",
    "live_adapter_invoked",
    "mutation_attempted",
    "persistence_attempted",
    "raw_approval_text_included",
    "raw_actor_id_included",
    "raw_source_content_included",
    "private_raw_content_included",
    "credentials_or_auth_material_included",
    "private_paths_included",
    "source_uris_included",
    "raw_platform_ids_included",
    "raw_prompts_or_queries_included",
    "raw_payload_content_included",
    "raw_backend_responses_included",
    "private_correlation_refs_included",
}
L6V_SUPERVISED_PROOF_ZERO_ONLY_FIELDS = {"allowed_result_count"}
L6V_SUPERVISED_PROOF_UNSAFE_VALUE_FIELDS = {
    "raw_source_content",
    "private_path",
    "source_uri",
    "source_identifier",
    "credential_material",
    "auth_material",
    "token",
    "raw_query_text",
    "raw_prompt_text",
    "raw_payload_content",
    "raw_backend_response",
    "raw_platform_id",
    "private_correlation_ref",
}
L6V_SUPERVISED_PROOF_KV = re.compile(
    r"(?P<quote>[\"'`]?)(?P<key>[A-Za-z_][A-Za-z0-9_]*)"
    r"(?P=quote)\s*(?::|=)\s*"
    r"(?P<value>\"[^\"]*\"|'[^']*'|`[^`]*`|true|false|null|None|[0-9]+)",
    re.IGNORECASE,
)


class HygieneHit(str):
    """Formatted hygiene hit."""


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'", "`"}:
        return value[1:-1]
    return value


def _line_for(text: str, index: int) -> int:
    return text[:index].count("\n") + 1


def scan_l6v_supervised_proof_artifact_text(text: str, rel: str) -> list[HygieneHit]:
    """Ratchet reportable supervised-proof artifacts without reading live sources.

    The scanner is syntax-light on purpose: it catches JSON/YAML/text
    fixture-style key/value artifacts that would make a source-card proof unsafe
    to report, while preserving committed synthetic metadata refs.
    """

    hits: list[HygieneHit] = []
    for match in L6V_SUPERVISED_PROOF_KV.finditer(text):
        key = match.group("key")
        value = match.group("value")
        normalized_value = _strip_quotes(value)
        line = _line_for(text, match.start())
        if key in L6V_SUPERVISED_PROOF_FALSE_ONLY_FIELDS and value.lower() == "true":
            hits.append(HygieneHit(f"{rel}:{line}: l6v_supervised_proof_true_flag: {key}"))
        elif key in L6V_SUPERVISED_PROOF_ZERO_ONLY_FIELDS and normalized_value != "0":
            hits.append(HygieneHit(f"{rel}:{line}: l6v_supervised_proof_nonzero_count: {key}"))
        elif key in L6V_SUPERVISED_PROOF_UNSAFE_VALUE_FIELDS and normalized_value not in {"", "false", "null", "None"}:
            hits.append(HygieneHit(f"{rel}:{line}: l6v_supervised_proof_unsafe_value: {key}"))
        elif key in L6V_SUPERVISED_PROOF_SAFE_REFS:
            if not L6V_SUPERVISED_PROOF_SAFE_REFS[key].match(normalized_value):
                hits.append(HygieneHit(f"{rel}:{line}: l6v_supervised_proof_unsafe_ref: {key}"))
    return hits


def is_generated_cache_path(path: Path) -> bool:
    """Return True when a path belongs to generated or dependency cache output."""
    return any(part in GENERATED_CACHE_DIRS for part in path.parts) or any(
        part.endswith(('.egg-info', '.dist-info')) for part in path.parts
    )


def iter_files(root: Path = ROOT) -> Iterable[tuple[Path, str]]:
    for path in root.rglob("*"):
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if is_generated_cache_path(rel_path):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path, rel


def allowed(rel: str, kind: str) -> bool:
    if rel in {"scripts/public_hygiene_scan.py", "docs/public-hygiene.md"} and kind in {
        "host_private_path",
        "platform_identifier",
        "token_like",
        "atlas_source_floor",
        "docs_atlas_source_reference",
        "internal_baton_reference",
        "github_issue_comment_url",
        "internal_operator_term",
        "l6v_supervised_proof_true_flag",
        "l6v_supervised_proof_nonzero_count",
        "l6v_supervised_proof_unsafe_value",
        "l6v_supervised_proof_unsafe_ref",
    }:
        return True
    return False


def scan(root: Path = ROOT) -> list[HygieneHit]:
    hits: list[HygieneHit] = []
    for path, rel in iter_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                if not allowed(rel, kind):
                    line = _line_for(text, match.start())
                    hits.append(HygieneHit(f"{rel}:{line}: {kind}: {match.group(0)[:80]}"))
        if path.suffix in L6V_SUPERVISED_PROOF_ARTIFACT_SUFFIXES:
            for hit in scan_l6v_supervised_proof_artifact_text(text, rel):
                kind = hit.split(": ", 2)[1].rstrip(":")
                if not allowed(rel, kind):
                    hits.append(hit)
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan repository text files for public-readiness hygiene risks.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to scan; defaults to this checkout.")
    args = parser.parse_args(argv)

    hits = scan(args.root.resolve())
    if hits:
        print("public hygiene scan failed:")
        print("\n".join(hits))
        return 1
    print("public hygiene scan passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
