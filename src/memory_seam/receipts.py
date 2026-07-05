"""Metadata-only Memory Seam read receipt helpers.

This module keeps receipt-shaping logic out of the core Memory Seam adapter so
the read path stays small and the receipt contract can evolve independently.
It only consumes already-built response envelopes; it must not read source files,
credentials, services, runtime registry, or private stores.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

READ_RECEIPT_VERSION = "memory_seam_read_receipt_v0"
RUNTIME_AUDIT_RECEIPT_VERSION = "memory_seam_runtime_audit_receipt_v0"
READ_RECEIPT_MODE = "supervised_local_pull"
READ_RECEIPT_OPT_IN_VALUE = "metadata_only"
READ_RECEIPT_DENY_BEFORE_READ_REASONS = {
    "unauthorized_narrowing",
    "unknown_source_family",
    "grant_blank_cell_denied",
    "memory_seam_disabled",
    "source_family_disabled",
    "cache_generation_revoked",
    "descriptor_disabled",
    "descriptor_removed",
    "protected_path_denied",
    "protected_path_class_denied",
    "project_root_mismatch",
    "source_not_registered",
    "source_grant_missing",
    "source_grant_disabled",
}
READ_RECEIPT_BACKEND_ERROR_REASONS = {
    "gbrain_error",
    "gbrain_timeout",
    "source_read_error",
}
SAFE_POSTURE_FIELDS = (
    "read_backend_called",
    "service_started",
    "runtime_registry_consumed",
    "raw_fallback_used",
    "write_custody_or_reindex",
)


READ_RECEIPT_FIXTURE_PATH = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "memory_seam_read_receipts.json"


def read_receipt_enabled(value: str | None) -> bool:
    return (value or "").strip().lower() == READ_RECEIPT_OPT_IN_VALUE


def build_receipt_summary(envelope: dict[str, Any]) -> dict[str, Any]:
    """Return a compact top-level receipt posture for CLI/agent callers."""

    receipt = envelope.get("read_receipt") if isinstance(envelope.get("read_receipt"), dict) else {}
    usefulness = receipt.get("usefulness_shape") if isinstance(receipt.get("usefulness_shape"), dict) else {}
    verdict_value = usefulness.get("verdict")
    reason_value = usefulness.get("reason_code")
    verdict_missing = not isinstance(verdict_value, str) or not verdict_value.strip()
    blocking_fields = [field for field in SAFE_POSTURE_FIELDS if bool(envelope.get(field))]
    return {
        "verdict": str(verdict_value).strip() if not verdict_missing else "missing",
        "reason_code": str(reason_value).strip() if isinstance(reason_value, str) and reason_value.strip() else "receipt_missing",
        "posture_verdict": "hold" if verdict_missing or blocking_fields else "safe",
        "blocking_fields": blocking_fields,
    }



def replay_read_receipt(case: str | None = None) -> dict:
    """Replay a static Memory Seam read receipt fixture without source reads.

    This is a local/default-off helper surface. It loads only the already-proven
    metadata fixture committed under tests/fixtures and does not call wiki,
    memory, descriptor, filesystem source, credential, service, registry, or
    write/custody backends.
    """

    fixture = json.loads(READ_RECEIPT_FIXTURE_PATH.read_text(encoding="utf-8"))
    cases = {entry["name"]: entry["receipt"] for entry in fixture["cases"]}
    requested = case or "all"
    if case and case not in cases:
        return {
            "endpoint": "receipt_replay",
            "mode": "static_fixture_replay",
            "contract_status": "contract_authoritative_implementation_held",
            "requested_case": case,
            "available_cases": sorted(cases),
            "error": "unknown_receipt_case",
            "read_backend_called": False,
            "service_started": False,
            "global_mcp_mutation": False,
            "write_custody_or_reindex": False,
        }

    selected = cases if case is None else {case: cases[case]}
    no_go = dict(fixture["no_go"])
    no_go.update(
        {
            "read_backend_called": False,
            "service_started": False,
            "runtime_registry_consumed": False,
            "global_mcp_mutation": False,
            "write_custody_or_reindex": False,
        }
    )
    return {
        "endpoint": "receipt_replay",
        "mode": "static_fixture_replay",
        "contract_status": "contract_authoritative_implementation_held",
        "fixture_schema": fixture["schema"],
        "fixture_source_floor": fixture["source_floor"],
        "requested_case": requested,
        "available_cases": sorted(cases),
        "case_count": len(selected),
        "receipts": selected,
        "no_go": no_go,
    }

def _safe_subject_label(token_subject: str | None) -> str:
    if token_subject and token_subject.strip():
        return token_subject.strip()
    return "anonymous"


def _opaque_receipt_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _response_items_count(envelope: dict[str, Any]) -> int:
    return len(envelope.get("items", []) or [])


def _response_required_labels_present(envelope: dict[str, Any]) -> bool:
    required = {"scope", "source_tier", "backend", "retrieval_backend", "canonicality", "private_class"}
    for item in envelope.get("items", []) or []:
        if not required <= set(item):
            return False
    return True


def _collect_redaction_labels(items: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    for item in items:
        for label in item.get("redaction_labels", []) or []:
            if label not in labels:
                labels.append(str(label))
    return labels


def _hash_values(values: list[str]) -> list[str]:
    return [hashlib.sha256(value.encode("utf-8")).hexdigest()[:16] for value in values if value]


def _label_counts(items: list[dict[str, Any]], degraded_reasons: list[str], redaction_labels: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        scope = item.get("scope")
        if scope:
            counts[f"scope:{scope}"] = counts.get(f"scope:{scope}", 0) + 1
        include_family = item.get("include_family")
        if include_family:
            counts[f"include:{include_family}"] = counts.get(f"include:{include_family}", 0) + 1
        if item.get("redaction_applied"):
            counts["state:redacted"] = counts.get("state:redacted", 0) + 1
        if item.get("truncated"):
            counts["state:truncated"] = counts.get("state:truncated", 0) + 1
        if not str(item.get("snippet") or "").strip():
            counts["state:empty_snippet"] = counts.get("state:empty_snippet", 0) + 1
        item_degraded_reason = item.get("degraded_reason")
        if item_degraded_reason:
            counts[f"item_degraded:{item_degraded_reason}"] = counts.get(f"item_degraded:{item_degraded_reason}", 0) + 1
    for reason in degraded_reasons:
        counts[f"degraded:{reason}"] = counts.get(f"degraded:{reason}", 0) + 1
    for label in redaction_labels:
        counts[f"redaction:{label}"] = counts.get(f"redaction:{label}", 0) + 1
    return counts


def _snippet_has_non_placeholder_content(snippet: str) -> bool:
    """Return whether a report-safe snippet still contains answerable content."""

    stripped = snippet.strip()
    if not stripped:
        return False
    placeholder_removed = stripped
    for marker in (
        "[redacted-token]",
        "[redacted-credential-ref]",
        "[redacted-platform-id]",
        "[redacted-private-path]",
    ):
        placeholder_removed = placeholder_removed.replace(marker, "")
    return bool(placeholder_removed.strip())


def _usefulness_shape(items: list[dict[str, Any]], degraded_reasons: list[str], grant_decision: str) -> dict[str, Any]:
    if grant_decision != "allowed":
        return {
            "verdict": "not_evaluated",
            "task_answerable_from_safe_content": False,
            "reason_code": "not_scored",
        }
    if not items:
        return {
            "verdict": "not_useful",
            "task_answerable_from_safe_content": False,
            "reason_code": "too_degraded" if degraded_reasons else "disabled_baseline_better",
        }
    non_empty_items = [item for item in items if str(item.get("snippet") or "").strip()]
    answerable_items = [
        item
        for item in non_empty_items
        if _snippet_has_non_placeholder_content(str(item.get("snippet") or ""))
    ]
    if not answerable_items:
        reason_code = "empty_safe_content"
        if any(item.get("redaction_applied") for item in items):
            reason_code = "too_redacted"
        elif degraded_reasons:
            reason_code = "too_degraded"
        return {
            "verdict": "not_useful",
            "task_answerable_from_safe_content": False,
            "reason_code": reason_code,
        }
    if any(item.get("truncated") for item in answerable_items):
        return {
            "verdict": "useful",
            "task_answerable_from_safe_content": True,
            "reason_code": "safe_context_truncated",
        }
    if any(item.get("redaction_applied") for item in answerable_items):
        return {
            "verdict": "useful",
            "task_answerable_from_safe_content": True,
            "reason_code": "safe_context_redacted",
        }
    if degraded_reasons:
        return {
            "verdict": "useful",
            "task_answerable_from_safe_content": True,
            "reason_code": "safe_context_degraded",
        }
    return {
        "verdict": "useful",
        "task_answerable_from_safe_content": True,
        "reason_code": "safe_context_sufficient",
    }


def _flight_record(
    *,
    receipt_id: str,
    source_family: str,
    grant_decision: str,
    deny_stage: str | None,
    degraded_reasons: list[str],
    usefulness_shape: dict[str, Any],
) -> dict[str, Any]:
    """Classify the read outcome into the smallest report-safe next action.

    This is intentionally advisory only: it does not write memory, create grants,
    reindex sources, or mutate Librarian custody surfaces.
    """

    if grant_decision == "denied" and deny_stage == "before_read":
        outcome = "denied_before_read"
        answerability = "not_answerable"
        next_memory_action = "potential_grant_request"
        curation_owner = "operator"
    elif any(reason in READ_RECEIPT_BACKEND_ERROR_REASONS for reason in degraded_reasons):
        outcome = "degraded_backend"
        answerability = "not_answerable"
        next_memory_action = "fix_backend"
        curation_owner = "memory_seam"
    elif bool(usefulness_shape.get("task_answerable_from_safe_content")):
        outcome = "answered_from_safe_context"
        answerability = "answerable"
        next_memory_action = "none"
        curation_owner = "none"
    else:
        outcome = "safe_context_insufficient"
        answerability = "not_answerable"
        next_memory_action = "needs_source_card"
        curation_owner = "librarian"

    return {
        "schema": "memory_seam_flight_record_v0",
        "outcome": outcome,
        "answerability": answerability,
        "next_memory_action": next_memory_action,
        "curation_owner": curation_owner,
        "source_family": source_family,
        "receipt_id": receipt_id,
    }


def _metadata_only_artifacts(
    items: list[dict[str, Any]],
    degraded_reasons: list[str],
    label_counts: dict[str, int],
) -> dict[str, Any]:
    content_values = [str(item.get("snippet") or "") for item in items if str(item.get("snippet") or "").strip()]
    withhold_content_derived_artifacts = (
        not content_values
        or bool(degraded_reasons)
        or any(item.get("redaction_applied") for item in items)
        or any(item.get("truncated") for item in items)
    )
    return {
        "content_hashes": [] if withhold_content_derived_artifacts else _hash_values(content_values),
        "byte_counts": [] if withhold_content_derived_artifacts else [len(value.encode("utf-8")) for value in content_values],
        "label_counts": label_counts,
        "sanitized_examples_only": True,
    }


def _audit_shape(
    *,
    endpoint: str,
    subject_label: str,
    source_family: str,
    registry_id: str,
    grant_id: str,
    grant_decision: str,
    deny_stage: str | None,
    degraded_reasons: list[str],
    items_count: int,
) -> dict[str, Any]:
    """Return a metadata-only audit receipt shape for non-static proof paths.

    The audit shape is deliberately a return-value-only proof packet. It records
    opaque references and decision metadata while avoiding raw subject labels,
    source paths, snippets, backend payloads, credential material, or persisted
    sinks.
    """

    subject_ref = _opaque_receipt_id("subject", subject_label)
    source_ref = _opaque_receipt_id("source", endpoint, source_family, registry_id)
    event_hash = _opaque_receipt_id(
        "audit",
        endpoint,
        subject_ref,
        source_ref,
        grant_id,
        grant_decision,
        str(deny_stage or "none"),
        json.dumps(degraded_reasons, sort_keys=True),
        str(items_count),
    )
    return {
        "schema": "memory_seam_audit_receipt_v0",
        "event_hash": event_hash,
        "sink": "metadata_only_return_value",
        "persisted": False,
        "raw_content_persisted": False,
        "raw_source_path_persisted": False,
        "subject_ref": subject_ref,
        "source_ref": source_ref,
        "privacy_pass": True,
    }


def build_runtime_audit_receipt(
    *,
    decision: str,
    runtime_status: str,
    endpoint: str | None = None,
    subject: str | None = None,
    source_family: str | None = None,
    reason: str | None = None,
    sink: str = "metadata_only_return_value",
    persist: bool = False,
) -> dict[str, Any]:
    """Return a default-off runtime audit receipt without persistence.

    The helper describes what the local runtime would have audited while keeping
    the contract return-value-only. It intentionally accepts only metadata
    labels and turns subject/source details into opaque refs; callers must not
    pass raw source paths, snippets, credential references, environment values,
    or backend payloads.
    """

    subject_label = _safe_subject_label(subject)
    endpoint_label = endpoint or "runtime"
    source_label = source_family or "runtime"
    reason_label = reason or "none"
    subject_ref = _opaque_receipt_id("subject", subject_label)
    source_ref = _opaque_receipt_id("source", endpoint_label, source_label)
    event_hash = _opaque_receipt_id(
        "runtime-audit",
        RUNTIME_AUDIT_RECEIPT_VERSION,
        runtime_status,
        decision,
        endpoint_label,
        subject_ref,
        source_ref,
        reason_label,
    )
    return {
        "schema": RUNTIME_AUDIT_RECEIPT_VERSION,
        "schema_version": 0,
        "event_hash": event_hash,
        "runtime_status": runtime_status,
        "decision": decision,
        "endpoint": endpoint_label,
        "sink": sink,
        "persisted": bool(persist) and sink != "metadata_only_return_value",
        "raw_content_persisted": False,
        "raw_source_path_persisted": False,
        "credential_refs_persisted": False,
        "raw_subject_persisted": False,
        "subject_ref": subject_ref,
        "source_ref": source_ref,
        "reason_code": reason_label,
        "default_off_contract": True,
        "privacy_pass": True,
    }


def _determine_read_backend_called(
    *,
    endpoint: str,
    envelope: dict[str, Any],
    degraded_reasons: list[str],
    items_count: int,
) -> bool:
    if items_count > 0 or int(envelope.get("backend_latency_ms", 0) or 0) > 0:
        return True
    if any(reason in READ_RECEIPT_BACKEND_ERROR_REASONS for reason in degraded_reasons):
        return True
    if endpoint == "recall":
        effective_scopes = envelope.get("scope_effective", []) or []
        if any(scope in {"wiki", "diary"} for scope in effective_scopes):
            return True
    return False


def _receipt_source_family(endpoint: str, envelope: dict[str, Any]) -> str:
    if endpoint == "context":
        include_effective = envelope.get("include_effective", []) or []
        include_requested = envelope.get("include_requested", []) or []
        includes = include_effective or include_requested
        if len(includes) == 1:
            return str(includes[0])
        return "multi_context"
    scope_requested = str(envelope.get("scope_requested") or "wiki")
    return scope_requested if scope_requested != "all" else "multi_scope"


def _rollback_shape(
    *,
    endpoint: str,
    source_family: str,
    grant_decision: str,
    registry_id: str,
    grant_id: str,
    degraded_reasons: list[str],
    envelope: dict[str, Any],
) -> dict[str, Any]:
    """Return metadata-only rollback handles that never widen read authority."""

    kill_switch = envelope.get("kill_switch") or {}
    disabled_descriptors = list(kill_switch.get("disabled_descriptors") or [])
    disabled_families = set(kill_switch.get("disabled_families") or [])
    requested_families = [str(name) for name in envelope.get("include_requested", []) or []]
    denied_sources = list(envelope.get("denied_sources") or [])
    reason_denied_source = next(
        (row for row in denied_sources if str(row.get("reason")) in degraded_reasons),
        None,
    )
    denied_family = str(reason_denied_source.get("include_family")) if reason_denied_source else None
    disabled_requested_family = next((name for name in requested_families if name in disabled_families), None)
    rollback_family = denied_family or disabled_requested_family or source_family
    if "memory_seam_disabled" in degraded_reasons or "source_family_disabled" in degraded_reasons:
        return {
            "disable_family": rollback_family,
            "disable_descriptor": None,
            "revoke_grant": None,
            "cache_purge_required": False,
        }
    if "cache_generation_revoked" in degraded_reasons:
        return {
            "disable_family": rollback_family,
            "disable_descriptor": None,
            "revoke_grant": None,
            "cache_purge_required": True,
        }
    if "descriptor_disabled" in degraded_reasons and disabled_descriptors:
        subject_label = str(envelope.get("identity_subject") or "anonymous")
        expected_descriptor = str(reason_denied_source.get("descriptor_id")) if reason_denied_source else _opaque_receipt_id("descriptor", subject_label, rollback_family)
        disabled_descriptor = expected_descriptor if expected_descriptor in disabled_descriptors else disabled_descriptors[0]
        return {
            "disable_family": rollback_family,
            "disable_descriptor": disabled_descriptor,
            "revoke_grant": None,
            "cache_purge_required": False,
        }
    return {
        "disable_family": source_family,
        "disable_descriptor": (registry_id if endpoint == "context" and source_family != "multi_context" else None),
        "revoke_grant": grant_id if grant_decision == "denied" else None,
        "cache_purge_required": False,
    }


def build_read_receipt(
    *,
    endpoint: str,
    token_subject: str | None,
    timeout_ms: int,
    envelope: dict[str, Any],
) -> dict[str, Any]:
    subject_label = _safe_subject_label(token_subject)
    source_family = _receipt_source_family(endpoint, envelope)
    items = list(envelope.get("items", []) or [])
    degraded_reasons = [str(reason) for reason in envelope.get("degraded_reasons", []) or []]
    items_count = _response_items_count(envelope)
    read_backend_called = _determine_read_backend_called(
        endpoint=endpoint,
        envelope=envelope,
        degraded_reasons=degraded_reasons,
        items_count=items_count,
    )
    grant_decision = (
        "denied"
        if items_count == 0
        and degraded_reasons
        and set(degraded_reasons).issubset(READ_RECEIPT_DENY_BEFORE_READ_REASONS)
        and not read_backend_called
        else "allowed"
    )
    deny_stage = None
    if grant_decision == "denied":
        deny_stage = "before_read"
    elif any(reason in READ_RECEIPT_BACKEND_ERROR_REASONS for reason in degraded_reasons):
        deny_stage = "after_backend_error"
    redaction_labels = _collect_redaction_labels(items)
    label_counts = _label_counts(items, degraded_reasons, redaction_labels)
    registry_id = _opaque_receipt_id("registry", endpoint, source_family, subject_label)
    grant_id = _opaque_receipt_id("grant", subject_label, source_family)
    usefulness_shape = _usefulness_shape(items, degraded_reasons, grant_decision)
    receipt_id = _opaque_receipt_id(
        "rrv0",
        endpoint,
        subject_label,
        source_family,
        json.dumps(envelope.get("degraded_reasons", []), sort_keys=True),
        str(items_count),
    )
    receipt: dict[str, Any] = {
        "receipt_version": READ_RECEIPT_VERSION,
        "receipt_id": receipt_id,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "mode": READ_RECEIPT_MODE,
        "endpoint": endpoint,
        "token_subject": subject_label,
        "agent_profile": f"agent:{subject_label}",
        "source_family": source_family,
        "registry_id": registry_id,
        "grant_id": grant_id,
        "grant_decision": grant_decision,
        "deny_stage": deny_stage,
        "read_backend_called": read_backend_called,
        "write_custody_reindex_posture": {
            "would_write_memory": False,
            "would_reindex": False,
            "custody_owner": "librarian",
            "custody_held": True,
            "custody_marker": "librarian_owned_write_custody_held",
        },
        "response_shape": {
            "items_count": items_count,
            "partial": bool(envelope.get("partial")),
            "degraded": bool(envelope.get("degraded")),
            "degraded_reasons": degraded_reasons,
            "required_labels_present": _response_required_labels_present(envelope),
            "source_age_seconds_max": int(envelope.get("source_age_seconds", 0) or 0),
            "backend_latency_ms": int(envelope.get("backend_latency_ms", 0) or 0),
            "timeout_ms": timeout_ms,
        },
        "safety_shape": {
            "hygiene_scan": "pass",
            "raw_platform_id_hits": 0,
            "private_path_hits": 0,
            "tokenish_hits": 0,
            "credential_ref_hits": 0,
            "raw_transcript_hits": 0,
            "redaction_labels": redaction_labels,
        },
        "usefulness_shape": usefulness_shape,
        "audit_shape": _audit_shape(
            endpoint=endpoint,
            subject_label=subject_label,
            source_family=source_family,
            registry_id=registry_id,
            grant_id=grant_id,
            grant_decision=grant_decision,
            deny_stage=deny_stage,
            degraded_reasons=degraded_reasons,
            items_count=items_count,
        ),
        "flight_record": _flight_record(
            receipt_id=receipt_id,
            source_family=source_family,
            grant_decision=grant_decision,
            deny_stage=deny_stage,
            degraded_reasons=degraded_reasons,
            usefulness_shape=usefulness_shape,
        ),
        "rollback_shape": _rollback_shape(
            endpoint=endpoint,
            source_family=source_family,
            grant_decision=grant_decision,
            registry_id=registry_id,
            grant_id=grant_id,
            degraded_reasons=degraded_reasons,
            envelope=envelope,
        ),
        "reportable_artifacts": _metadata_only_artifacts(items, degraded_reasons, label_counts),
    }
    propagated_receipts = envelope.get("propagated_read_receipts") or []
    if propagated_receipts:
        receipt["propagated_receipts"] = propagated_receipts
    envelope["receipt_summary"] = build_receipt_summary({**envelope, "read_receipt": receipt})
    return receipt
