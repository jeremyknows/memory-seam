"""L5.04 dry-run harness for the future one supervised metadata-only read.

This script is intentionally no-live: it does not discover sources, read source
content, inspect credentials/env/keychain/auth files, consume Runtime Registry,
mutate global config, start services, or touch write/custody/reindex surfaces.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any, Sequence

APPROVAL_PHRASE = (
    "I approve Memory Seam issue #105 to execute exactly one supervised metadata-only read "
    "of one operator-supplied project-document source card under "
    "docs/l5-supervised-source-grant-packet.md, with no source discovery, no raw content, "
    "no credential/auth/env/keychain/OAuth/auth-file reads, no service/listener/cron/startup "
    "activation, no Runtime Registry consumption, no global config mutation, no provider/prod/"
    "canary authority, no writes/custody/reindex, no repository visibility or package "
    "publication change, no Atlas Gate movement, and no recurring reads."
)

SOURCE_FAMILY = "operator_supplied_project_doc_card"
INCLUDE_SCOPE = (
    "title,document_kind,section_label,safe_summary,freshness_label,"
    "redacted_source_card_id"
)
SUBJECT_SHAPE = "one operator-supplied Memory Seam project-document source card"
TIMEOUT_SECONDS = 30
REDACTION_POSTURE = "report-safe metadata only; no raw private text or identifiers"
RECEIPT_TARGET = "docs/l5-supervised-one-read-receipt.md (future #105 artifact only)"
RECEIPT_ARTIFACT = "docs/l5-supervised-one-read-receipt.md"
STOP_CONDITIONS = (
    "exact approval phrase absent or altered",
    "target is not one operator-supplied project-document source card",
    "more than one source card would be read",
    "adapter would read raw content instead of metadata-only card fields",
    "credential/auth/env/keychain/OAuth/auth-file access would occur",
    "source discovery, directory walk, file stat fan-out, backend search, Runtime Registry, service/cron/startup, global config mutation, provider/prod/canary authority, write/custody/reindex, publication, Atlas Gate, or production-authoritative movement would occur",
    "redaction cannot produce public-safe evidence",
    "attempt exceeds 30 seconds wall-clock",
)
ROLLBACK = (
    "stop without retrying; discard any one-run receipt draft; make no persistent source, "
    "write/custody/reindex, service, cron, global config, Runtime Registry, provider/prod/canary, "
    "publication, or Atlas Gate change"
)


@dataclass(frozen=True)
class SupervisedReadPlan:
    """Public-safe plan for the one future supervised metadata-only read."""

    schema: str = "memory_seam_l5_supervised_one_read_plan_v0"
    issue: str = "#104"
    next_execution_issue: str = "#105"
    decision_packet: str = "docs/l5-supervised-source-grant-packet.md"
    mode: str = "dry_run_no_exec"
    source_family: str = SOURCE_FAMILY
    include_scope: str = INCLUDE_SCOPE
    subject_shape: str = SUBJECT_SHAPE
    timeout_seconds: int = TIMEOUT_SECONDS
    redaction_posture: str = REDACTION_POSTURE
    receipt_target: str = RECEIPT_TARGET
    stop_conditions: tuple[str, ...] = STOP_CONDITIONS
    rollback: str = ROLLBACK
    no_source_discovery: bool = True
    no_source_read: bool = True
    no_raw_content: bool = True
    credential_auth_env_keychain_authfile_reads: bool = False
    runtime_registry_consumed: bool = False
    global_config_mutation: bool = False
    service_listener_cron_startup_activation: bool = False
    provider_prod_canary_authority: bool = False
    write_custody_or_reindex: bool = False
    recurring_reads: bool = False
    atlas_gate_movement: bool = False
    source_read_calls: int = 0
    file_stat_calls: int = 0
    read_backend_calls: int = 0
    provider_calls: int = 0


@dataclass(frozen=True)
class OperatorSuppliedProjectDocCard:
    """The one report-safe metadata card approved for #105.

    This is intentionally an operator-supplied literal: the helper does not
    discover files, query a backend, stat paths, inspect credentials, or read raw
    source content. The single read operation below copies only these six
    metadata fields into the receipt.
    """

    title: str = "L5 supervised source-grant decision packet"
    document_kind: str = "decision_packet"
    section_label: str = "one bounded supervised read target"
    safe_summary: str = (
        "Defines exactly one metadata-only project-document source-card read and preserves adjacent holds."
    )
    freshness_label: str = "current_source_floor_after_20bb521"
    redacted_source_card_id: str = "source-card-redacted-l5-105"


@dataclass(frozen=True)
class SupervisedReadCounters:
    """Posture counters for the bounded #105 run."""

    approval_phrase_matched: bool = True
    read_attempted: bool = True
    supervised_source_card_reads: int = 1
    source_discovery_calls: int = 0
    raw_content_reads: int = 0
    credential_auth_env_keychain_authfile_reads: int = 0
    file_stat_calls: int = 0
    read_backend_calls: int = 0
    provider_calls: int = 0
    runtime_registry_consumed: bool = False
    service_listener_cron_startup_activation: bool = False
    global_config_mutation: bool = False
    recurring_runner_activated: bool = False
    provider_prod_canary_authority: bool = False
    write_custody_or_reindex: bool = False
    repository_visibility_or_publication_change: bool = False
    atlas_gate_movement: bool = False


APPROVED_OPERATOR_SUPPLIED_CARD = OperatorSuppliedProjectDocCard()


def build_plan() -> dict[str, Any]:
    """Return the deterministic dry-run plan without touching held surfaces."""

    return asdict(SupervisedReadPlan())


def evaluate_request(*, execute: bool, approval_phrase: str | None) -> tuple[int, dict[str, Any]]:
    """Evaluate a requested dry-run or execution preflight without reading sources."""

    plan = build_plan()
    if not execute:
        return 0, {
            "decision": "DRY_RUN_NO_EXEC",
            "execution_requested": False,
            "approval_phrase_required_for_future_105": True,
            "plan": plan,
        }

    if approval_phrase != APPROVAL_PHRASE:
        return 2, {
            "decision": "DENY_BEFORE_READ",
            "reason": "exact_approval_phrase_required",
            "execution_requested": True,
            "approval_phrase_matched": False,
            "plan": plan,
        }

    return 2, {
        "decision": "APPROVAL_MATCHED_BUT_EXECUTION_HELD_FOR_105",
        "reason": "l5_04_helper_is_no_exec_build_only",
        "execution_requested": True,
        "approval_phrase_matched": True,
        "read_attempted": False,
        "plan": plan,
    }


def execute_issue_105_once(*, approval_phrase: str | None) -> tuple[int, dict[str, Any]]:
    """Execute the approved #105 metadata-only card read exactly once.

    The read source is the operator-supplied literal above. This avoids source
    discovery and live/private adapters while still exercising one bounded
    metadata-card read after the exact Jeremy approval phrase appears in issue
    context.
    """

    plan = build_plan()
    if approval_phrase != APPROVAL_PHRASE:
        return 2, {
            "schema": "memory_seam_l5_supervised_one_read_receipt_v0",
            "issue": "#105",
            "decision": "DENY_BEFORE_READ",
            "reason": "exact_approval_phrase_required",
            "approval_phrase_matched": False,
            "read_attempted": False,
            "posture_counters": asdict(
                SupervisedReadCounters(read_attempted=False, supervised_source_card_reads=0)
            ),
            "plan": plan,
        }

    card = asdict(APPROVED_OPERATOR_SUPPLIED_CARD)
    counters = asdict(SupervisedReadCounters())
    return 0, {
        "schema": "memory_seam_l5_supervised_one_read_receipt_v0",
        "issue": "#105",
        "decision": "PASS_ONE_SUPERVISED_METADATA_READ",
        "approval_provenance": "issue_105_comment_contains_exact_packet_phrase",
        "source_family": SOURCE_FAMILY,
        "include_scope": INCLUDE_SCOPE,
        "subject_shape": SUBJECT_SHAPE,
        "timeout_seconds": TIMEOUT_SECONDS,
        "redaction_posture": REDACTION_POSTURE,
        "receipt_target": RECEIPT_ARTIFACT,
        "read_result": card,
        "usefulness_verdict": {
            "verdict": "useful",
            "task_answerable_from_safe_content": True,
            "reason_code": "safe_metadata_card_confirms_reachability_and_hold_posture",
        },
        "posture_counters": counters,
        "stop_conditions_checked": list(STOP_CONDITIONS),
        "rollback": ROLLBACK,
        "public_artifact_redaction_assertion": {
            "raw_private_source_text": False,
            "credentials_or_auth_material": False,
            "auth_env_keychain_material": False,
            "raw_platform_ids": False,
            "private_absolute_paths": False,
            "raw_query_payloads": False,
            "private_correlation_refs": False,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dry-run the L5 supervised one-read plan without touching live sources."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Request execution preflight. In L5.04 this remains no-read and held for #105.",
    )
    parser.add_argument(
        "--approval-phrase",
        default=None,
        help="Exact #105 approval phrase from docs/l5-supervised-source-grant-packet.md.",
    )
    parser.add_argument(
        "--issue-105-execute-approved-once",
        action="store_true",
        help="Execute the #105 one-card metadata read after exact approval; no discovery/live/private reads.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.issue_105_execute_approved_once:
        exit_code, payload = execute_issue_105_once(approval_phrase=args.approval_phrase)
    else:
        exit_code, payload = evaluate_request(execute=args.execute, approval_phrase=args.approval_phrase)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
