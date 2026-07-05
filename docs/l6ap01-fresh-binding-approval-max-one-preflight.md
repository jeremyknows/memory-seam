# L6AP.01 fresh binding approval receipt and max-one retry preflight

Issue: #390  
Parent: #6  
Starting source floor: `35046efe4880145d929bbe0ddb00196b83c9cc04`

This artifact records a report-safe, issue-bound preflight for the L6AP max-one supervised metadata retry rail. It does **not** perform the live retry; execution remains scoped to #391 only.

## Fresh approval binding

Report-safe approval anchor:

- source: fresh Discord source-deck message, represented by the report-safe anchor `fresh-discord-source-deck-message-report-safe-anchor`
- issue receipt: `issue-390-comment-4659796366`
- parent rail-created receipt: `issue-6-comment-4659797054`
- custody: one-run only

The preflight refuses stale, copied, broadened, expired, revoked, or missing issue-bound authority before any read.

## Exact retry target for #391 only

- endpoint: `memory_seam_recall`
- route audience: `memory-seam:read:recall`
- acting_for / agent: `sax`
- scope: `wiki`
- n: `3`
- query label: `supervised_metadata_readiness`
- evidence class: `SUPERVISED_METADATA_READ_RETRY_REPORT_SAFE`
- max operation count: `1`
- report-safe metadata only: `true`
- denial before read required: `true`

The query text is bound in code as exact metadata for the subsequent issue. This document intentionally does not include any raw/private/source content, source paths or URIs, auth payloads, provider payloads, secrets, env/keychain/OAuth/auth-file material, or credential data.

## Refusal surfaces

The preflight denies before read if any candidate asks for or implies:

- raw/private/source/auth/provider payload output;
- source paths/URIs;
- secret/env/keychain/OAuth/auth-file/credential reads;
- Runtime Registry access, provider callbacks, or service activation;
- source discovery, broad recall, broad `allowed=true`;
- provider/prod/canary/Gate/Atlas Gate/write/mutation movement;
- `max_operation_count` other than `1` or a second operation;
- non-report-safe output;
- removal of denial-before-read.

## Report-safe retry metadata fields for #391

If #391 executes or safely denies the single retry, only these fields are eligible for persistence:

- status
- endpoint
- route audience
- agent
- scope
- n
- query label
- evidence class
- items count
- safe item labels
- denial reason / auth status code when denied
- guarded counters

No live retry was performed by this issue.
