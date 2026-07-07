# L6X.03 report-safe one-read receipt verifier

Status: `RECEIPT_VERIFIER_NO_ADDITIONAL_READS`
Rail issue: #213
Parent issue: #6
Depends on: L6X.02 HOLD proof
Source floor entering slice: `1348a4b55fc52ca065a54ad8b3d57e0ccc333a9d` or later

## Scope

This slice adds a small metadata-only verifier for the supervised one-read attempt receipt shape. For the current rail, L6X.02 produced a no-live absent-approval HOLD proof, so the verifier accepts that HOLD receipt and preserves deny-before-read/callback posture.

The verifier verifies an already supplied receipt mapping only. It does not perform source discovery, live/private reads, callbacks, credential/auth reads, Runtime Registry consumption, persistence, activation, mutation, rollback, cache purge, publication, provider/prod/canary authority, repository visibility changes, Atlas Gate movement, or `allowed=true` routing.

## Required safe receipt fields

The verifier allows only safe metadata fields:

- `schema_version`
- `receipt_status`
- `approval_result`
- `live_read_invoked`
- `allowed`
- `allowed_result_count`
- `operation_class`
- `operation_count_attempted`
- `descriptor_ref`
- `source_card_ref`
- `stop_status`
- `rollback_status`
- `guarded_counters`
- `report_safe`
- `metadata_only`
- `unsafe_raw_fields_rejected_before_report`

For the L6X.02 HOLD receipt, `live_read_invoked=false`, `operation_count_attempted=0`, `allowed=false`, `allowed_result_count=0`, and all guarded counters remain zero.

## Unsafe echo regressions

The verifier rejects unsafe echo markers for these classes before a receipt can be treated as report safe:

- raw source text
- private paths
- source URIs
- platform IDs
- prompts/queries
- backend responses
- credentials/auth material
- private correlation refs
- raw approval text

It also rejects unknown receipt fields and nonzero guarded counters, including provider/backend/source-stat/source-read/credential/Runtime-Registry/persistence/mutation/rollback/cache-purge counters.

## Preserved HOLD posture

Because #212 had no exact owner approval comment, #213 does not broaden the attempt. It verifies the no-live HOLD artifact only and leaves future live/private reads held behind a separate exact owner approval and bounded rail. No additional read, callback, persistence, activation, production, mutation, rollback, cache-purge, Gate, or `allowed=true` authority is created here.
