# L6AB.01 report-safe source-card value comparison matrix

Status: `REPORT_SAFE_VALUE_COMPARISON_MATRIX_NO_LIVE_READS`
Rail issue: #251
Parent issue: #6
Depends on: L6AA rail closed at source floor `91761ed55889f4c5432b55c445e396e727a6be93`
Frontier source: `docs/l6aa05-source-floor-parent-status-frontier-reconciliation.md`

This packet compares existing public/report-safe L6X through L6AA evidence only. It performs no live/private read, no callback, no source discovery, no credential/auth/env/keychain/OAuth/auth-file read, no Runtime Registry consumption, no persistence or mutation, no service/listener/startup/global runtime activation, no publication/visibility/provider/prod/canary/Gate movement, and no broad `allowed=true` route.

## Matrix

| Case | Existing rail evidence | Approval state | Target-ref state | Outcome | Value signal |
| --- | --- | --- | --- | --- | --- |
| Absent approval | L6X #212/#214/#215 | `ABSENT_OWNER_APPROVAL` | `NOT_REACHED_NO_APPROVAL` | `DENIED_BEFORE_READ`; `live_read_invoked=false`; `allowed=false`; counts zero | No source-card value proof; approval absence proved denial posture. |
| Missing target refs | L6Y #222/#225 | `OWNER_APPROVAL_PRESENT_FRESH` | `MISSING_EXECUTABLE_DESCRIPTOR_AND_SOURCE_CARD_REFS` | `DENIED_BEFORE_READ`; `live_read_invoked=false`; `allowed=false`; counts zero | Control-plane value only; fresh approval still could not identify executable refs. |
| Mismatched target refs | L6Z #232/#235 | `OWNER_APPROVAL_PRESENT_FRESH` | `MISMATCHED_EXECUTABLE_DESCRIPTOR_OR_SOURCE_CARD_REFS` | `DENIED_BEFORE_READ`; `live_read_invoked=false`; `allowed=false`; counts zero | Useful denial evidence; exact refs matter before any source-card callback. |
| Exact owner-approved target refs | L6AA #242/#245 | `APPROVED_EXACT_OWNER_ISSUE_BOUND_FRESH_TARGET_REF_MATCH` | `EXACT_DESCRIPTOR_AND_SOURCE_CARD_REF_MATCH` | Historical PASS: `PASS_EXECUTION_ONE_REPORT_SAFE_SOURCE_CARD_READ`; `live_read_invoked=true`; `allowed=EXACT_ONE_REPORT_SAFE_SOURCE_CARD_READ_ONLY`; counts one | Report-safe metadata proved the target card existed, was reportable, and carried redaction labels. |

The L6AA PASS row is historical evidence for the already-consumed #242 one-read allowance. It is not reusable approval and cannot authorize another read.

## Report-safe evidence fields

The executable comparison helper in `memory_seam.l6ab_value_comparison` emits only:

- public issue anchors and rail names;
- approval state labels without raw approval text;
- target-ref match/missing/mismatch labels without private content;
- receipt/status labels, booleans, and integer counts;
- high-level value-signal summaries;
- explicit `cannot_authorize_another_read=true` flags.

It does not accept a reader callback, provider/backend/source callback, Runtime Registry handle, file path, credential material, or raw source/approval content.

## Preserved holds

- additional live/private reads remain held
- raw private content remains held
- source discovery, workspace scans, family scans, broad recall, and index queries remain held
- credential/auth/env/keychain/OAuth/auth-file reads remain held
- provider/backend/source-stat/source-read callbacks remain held
- Runtime Registry consumption remains held
- persistence, audit/custody writes, and cache mutation remain held
- service/listener/startup/cron activation and global runtime config mutation remain held
- publication, repository visibility, provider/prod/canary authority, and Atlas Gate movement remain held
- mutation, rollback, and cache-purge execution remain held
- any broad `allowed=true` route remains held

## Verification intent

Tests prove the comparison distinguishes absent approval, missing target refs, mismatched target refs, and the successful exact-owner-approved #242 report-safe evidence; emits only report-safe metadata; and cannot authorize another read.
