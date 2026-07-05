"""L5.06 no-live verifier for the supervised one-read receipt.

The verifier consumes an already-produced report-safe receipt artifact and does not
perform source discovery, Runtime Registry reads, backend/provider calls, service
activation, writes, custody, reindexing, or Atlas Gate movement.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

L5_POST_READ_VERIFIER_SCHEMA = "memory_seam_l5_post_read_verifier_v0"
L5_RECEIPT_SCHEMA = "memory_seam_l5_supervised_one_read_receipt_v0"

USEFULNESS_VERDICTS = {
    "useful",
    "too_redacted",
    "denied_before_read",
    "degraded_backend_error",
}

REQUIRED_ZERO_COUNTERS = (
    "source_discovery_calls",
    "raw_content_reads",
    "credential_auth_env_keychain_authfile_reads",
    "file_stat_calls",
    "read_backend_calls",
    "provider_calls",
)

REQUIRED_FALSE_POSTURE = (
    "runtime_registry_consumed",
    "service_listener_cron_startup_activation",
    "global_config_mutation",
    "recurring_runner_activated",
    "provider_prod_canary_authority",
    "write_custody_or_reindex",
    "repository_visibility_or_publication_change",
    "atlas_gate_movement",
)

_PRIVATE_VAR_FOLDERS_PATTERN = "/private" + "/var/folders"
_MAC_USER_PATH_PATTERN = "/" + "Users" + r"/[A-Za-z0-9._-]+"

SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private_absolute_path",
        re.compile(
            r"(?:" + _MAC_USER_PATH_PATTERN + r"|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+|"
            + re.escape(_PRIVATE_VAR_FOLDERS_PATTERN)
            + r")"
        ),
    ),
    (
        "token_like",
        re.compile(
            r"\b(?:ghp|gho|github_pat|sk-[A-Za-z0-9]|xox[baprs]-)[A-Za-z0-9_\-]{12,}\b|\bAKIA[0-9A-Z]{16}\b"
        ),
    ),
    ("platform_identifier", re.compile(r"\b(?:[1-9][0-9]{16,20}|[CDGUTW][0-9][A-Z0-9]{8,})\b")),
    (
        "raw_query_payload",
        re.compile(r"(?:\braw_query\b|\bquery_payload\b|\bq=)[^\n]{8,}", re.IGNORECASE),
    ),
)


@dataclass(frozen=True)
class VerificationResult:
    """Report-safe L5.06 verification result."""

    schema: str = L5_POST_READ_VERIFIER_SCHEMA
    issue: str = "#106"
    receipt_schema: str = L5_RECEIPT_SCHEMA
    verdict: str = "degraded_backend_error"
    reason_code: str = "unverified"
    task_answerable_from_safe_content: bool = False
    hygiene_passed: bool = False
    posture_preserved: bool = False
    no_additional_read_performed: bool = True
    posture_counters: dict[str, Any] = field(default_factory=dict)
    hygiene_findings: tuple[str, ...] = ()
    missing_fields: tuple[str, ...] = ()


def _stringify_public_artifact(artifact: Mapping[str, Any] | str) -> str:
    if isinstance(artifact, str):
        return artifact
    return repr(artifact)


def scan_public_hygiene(artifact: Mapping[str, Any] | str) -> tuple[str, ...]:
    """Return report-safe hygiene finding names for public/private leak patterns."""

    text = _stringify_public_artifact(artifact)
    findings: list[str] = []
    for name, pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            findings.append(name)
    return tuple(findings)


def _posture_preserved(counters: Mapping[str, Any]) -> bool:
    return all(counters.get(name) == 0 for name in REQUIRED_ZERO_COUNTERS) and all(
        counters.get(name) is False for name in REQUIRED_FALSE_POSTURE
    )


def _classify(receipt: Mapping[str, Any]) -> tuple[str, str, bool]:
    if receipt.get("decision") == "DENY_BEFORE_READ" or receipt.get("read_attempted") is False:
        return "denied_before_read", "receipt_denied_before_read", False

    if receipt.get("decision") in {"DEGRADED_BACKEND_ERROR", "BACKEND_FAILED"}:
        return "degraded_backend_error", "receipt_backend_or_adapter_failed", False

    if receipt.get("backend_error") or receipt.get("degraded") is True:
        return "degraded_backend_error", "receipt_backend_or_adapter_failed", False

    usefulness = receipt.get("usefulness_verdict")
    if isinstance(usefulness, Mapping):
        verdict = str(usefulness.get("verdict", "")).strip()
        answerable = usefulness.get("task_answerable_from_safe_content") is True
        reason = str(usefulness.get("reason_code", "receipt_usefulness_verdict"))
        if verdict == "useful" and answerable:
            return "useful", reason, True
        if verdict in {"too_redacted", "hold_too_redacted"} or not answerable:
            return "too_redacted", reason or "safe_content_too_redacted", False

    read_result = receipt.get("read_result")
    if isinstance(read_result, Mapping):
        safe_summary = str(read_result.get("safe_summary", "")).strip()
        if safe_summary and "redacted" not in safe_summary.lower():
            return "useful", "safe_metadata_summary_present", True

    return "too_redacted", "safe_content_missing_or_too_redacted", False


def verify_l5_post_read_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Verify a #105 receipt without performing another source/provider read."""

    missing: list[str] = []
    if receipt.get("schema") != L5_RECEIPT_SCHEMA:
        missing.append("schema")
    if "posture_counters" not in receipt:
        missing.append("posture_counters")

    raw_counters = receipt.get("posture_counters")
    counters: dict[str, Any] = dict(raw_counters) if isinstance(raw_counters, Mapping) else {}
    hygiene_findings = scan_public_hygiene(receipt)
    posture_ok = _posture_preserved(counters)
    verdict, reason_code, answerable = _classify(receipt)

    if missing:
        verdict = "degraded_backend_error"
        reason_code = "receipt_missing_required_fields"
        answerable = False
    elif hygiene_findings:
        verdict = "too_redacted"
        reason_code = "public_private_hygiene_failed"
        answerable = False
    elif not posture_ok:
        verdict = "degraded_backend_error"
        reason_code = "held_posture_counter_nonzero_or_true"
        answerable = False

    result = VerificationResult(
        verdict=verdict,
        reason_code=reason_code,
        task_answerable_from_safe_content=answerable,
        hygiene_passed=not hygiene_findings,
        posture_preserved=posture_ok,
        posture_counters=dict(counters),
        hygiene_findings=hygiene_findings,
        missing_fields=tuple(missing),
    )
    return asdict(result)


def verify_l5_receipt_document(path: str | Path) -> dict[str, Any]:
    """Verify the committed Markdown receipt artifact without source discovery."""

    receipt_path = Path(path)
    text = receipt_path.read_text(encoding="utf-8")
    counters: dict[str, Any] = {}
    for name in REQUIRED_ZERO_COUNTERS:
        counters[name] = 0 if f"`{name}` | `0`" in text else "missing"
    for name in REQUIRED_FALSE_POSTURE:
        counters[name] = False if f"`{name}` | `false`" in text else "missing"
    counters["supervised_source_card_reads"] = 1 if "`supervised_source_card_reads` | `1`" in text else "missing"

    receipt = {
        "schema": L5_RECEIPT_SCHEMA if L5_RECEIPT_SCHEMA in text else "missing",
        "decision": "PASS_ONE_SUPERVISED_METADATA_READ" if "PASS_ONE_SUPERVISED_METADATA_READ" in text else "missing",
        "usefulness_verdict": {
            "verdict": "useful" if "Verdict: `useful`" in text else "too_redacted",
            "task_answerable_from_safe_content": "Task answerable from safe content: `true`" in text,
            "reason_code": "committed_receipt_safe_usefulness_verdict",
        },
        "posture_counters": counters,
    }
    result = verify_l5_post_read_receipt(receipt)
    doc_findings = scan_public_hygiene(text)
    if doc_findings:
        result["verdict"] = "too_redacted"
        result["reason_code"] = "public_private_hygiene_failed"
        result["task_answerable_from_safe_content"] = False
        result["hygiene_passed"] = False
        result["hygiene_findings"] = tuple(sorted(set(result["hygiene_findings"]) | set(doc_findings)))
    return result
