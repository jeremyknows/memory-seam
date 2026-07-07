# L6W.01 supervised live-read approval packet scaffold

Status: `HITL_SCAFFOLD_ONLY_NO_APPROVAL_NO_EXECUTION`

Parent: #6  
Rail issue: #199  
Source floor: `9264533` or later on `origin/main`  
Upstream packet: `docs/l6v06-supervised-source-card-trust-boundary-review.md`

This packet is a docs/tests-only HITL scaffold for asking Jeremy for one future supervised live/private read of one report-safe source-card descriptor. It is not approval, not execution, not implementation, not a merge-triggered grant, and not authority for any current or future agent to perform a live/private read from this file alone.

The scaffold deliberately does not include approval wording that can be treated as already granted. It names required fields, checks, and stop conditions that a separate future issue-bound human comment would have to bind before any implementation may recognize approval. Until that separate fresh human comment exists and a later approved implementation slice recognizes it, all live/private read behavior remains held.

## Non-approval boundary

This packet must be interpreted as `NO_APPROVAL_PRESENT`.

The following events do not create approval:

- this document being merged;
- issue #199 closing;
- labels, milestones, branch names, PR titles, or PR bodies referencing supervised live-read work;
- stale comments from earlier L5/L6/L6U/L6V rails;
- copied approval text from another issue;
- comments by non-owner actors;
- comments that omit any required binding field;
- comments that broaden operation count, scope, source access, discovery, callback, persistence, activation, production, publication, visibility, provider/prod/canary, Atlas Gate, mutation, or `allowed=true` authority.

## Future approval packet requirements

A future approval request may ask Jeremy for exactly one issue-bound human approval comment. The future comment, if Jeremy chooses to grant it, must bind all of the following report-safe fields in one fresh comment on the designated future approval issue:

| Field | Required bound value or constraint |
| --- | --- |
| `approval_issue_ref` | the fresh future approval issue number, not #199 and not any prior issue |
| `approval_author_association` | `OWNER` |
| `approval_owner_ref` | `repo-owner:jeremyknows` |
| `approval_subject_ref` | one report-safe Memory Seam source-card descriptor subject chosen in the future issue |
| `approval_audience` | Memory Seam supervised live-read approval only |
| `approval_scope` | one report-safe source-card descriptor read only |
| `operation_class` | `SUPERVISED_REPORT_SAFE_SOURCE_CARD_LIVE_READ` |
| `max_operation_count` | exactly `1` |
| `approval_created_at` | present in the future comment metadata |
| `approval_expires_at` | no later than 12 hours after `approval_created_at` |
| `report_safe_output_shape` | safe refs, booleans, zero/non-zero counters, status strings, and usefulness classification only |
| `zero_discovery_expectation` | no source discovery, workspace scans, family scans, broad recall, or index queries |
| `denial_before_callback` | stale, variant, copied, broadened, unrelated, missing, unsafe, or expired approval must deny before provider/backend/source-stat/source-read callbacks |
| `stop_conditions` | deny on mismatch, expiry, callback request, raw content request, credential request, discovery request, Runtime Registry request, persistence request, activation request, publication/visibility request, provider/prod/canary request, Atlas Gate request, mutation request, or `allowed=true` request |
| `rollback_behavior` | no rollback callback; stop, emit report-safe denial/held receipt metadata only, and require a new human issue review before any retry |

The exact future approval issue may add tighter limits, but it must not broaden these requirements.

## Explicit held surfaces

This scaffold preserves the following holds:

- live/private reads until a separate future issue-bound owner approval and later approved implementation recognition exist;
- raw source content and raw private text;
- source discovery, workspace scans, family scans, broad recall, and index queries;
- source-stat/source-read/provider/backend callbacks;
- credentials, auth files, environment secrets, keychain entries, OAuth material, and auth-file reads;
- Runtime Registry consumption;
- write/custody/delete/reindex/rollback/cache-purge callbacks and all mutation execution;
- persistence, audit/custody record writes, and cache mutation;
- service/listener/startup/cron activation and global Hermes/MCP/client/runtime configuration mutation;
- package publication, repository visibility changes, provider/prod/canary or production authority, and Atlas Gate movement;
- any `allowed=true` route, allowed-result implementation, or claim that this scaffold is approval.

## Report-safe output contract for the future packet

Any future report for this lane may include only:

- public issue/PR numbers and repository file names;
- operation-class names and schema/status strings;
- report-safe descriptor/source-card references chosen for the future issue;
- booleans and numeric counters;
- expiry and stop-condition status;
- usefulness classification labels such as `useful`, `too_redacted`, `unsafe`, `ambiguous`, or `held`.

It must not include raw private source text, credentials, auth/env/keychain material, OAuth material, auth-file material, raw platform IDs, private absolute paths, raw prompt/query payloads, raw payload content, raw backend responses, private correlation refs, source URIs, or raw approval text.

## Acceptance checklist

This scaffold is acceptable only if tests prove that it:

1. is discoverable in the docs index and contract-test inventory;
2. records `HITL_SCAFFOLD_ONLY_NO_APPROVAL_NO_EXECUTION` and `NO_APPROVAL_PRESENT`;
3. binds issue, actor association, owner, subject, audience, scope, operation class, expiry, max-one-operation, report-safe output shape, zero-discovery expectations, rollback/stop behavior, and denial-before-callback requirements;
4. rejects merge/closure/label/stale/copied/non-owner/broadened interpretations as approval;
5. preserves no-live/no-callback/no-production/no-`allowed=true` boundaries.
