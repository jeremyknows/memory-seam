# L6U.02 supervised live-read approval packet

Status: `HITL_ONLY_FUTURE_APPROVAL_PACKET_NOT_APPROVAL`
Parent: #6
Rail issue: #178
Source floor: `1299f4f` or later
Upstream packet: `docs/l6-supervised-live-use-next-rail-decision-packet.md`
Prerequisite: L6U.01 closed/PASS adapter wiring map

This packet drafts the future human-in-the-loop approval requirements for one bounded supervised read-side proof. The packet itself is not approval, does not recognize approval, and does not implement or execute any live/private read. It is documentation and contract-test evidence only.

## Future-only approval purpose

Future operation class: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.

The future proof is limited to exactly one supervised read-side operation class and a max-one-operation limit: `max_operation_count=1`. The operation may only produce report-safe source-card/descriptor proof metadata in a later issue after explicit HITL approval. It must not read raw content, discover sources, query indexes, perform broad recall, call source-stat/source-read APIs, consume Runtime Registry data, or treat approval-like signals as approval. A future preflight must not treat this packet, a merge event, label, issue closure, stale comment, unrelated approval, or copied text as approval.

## Required future HITL approval fields

A later approval request must bind all of these fields before any callback-capable path is considered:

- `approval_packet_ref`: `l6u02.future.hitl.approval.packet.v1`
- `issue_ref`: the exact future issue number authorized for the proof
- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`
- `max_operation_count`: `1`
- `actor_ref`: report-safe operator actor reference
- `subject_ref`: report-safe caller subject reference
- `owner_ref`: report-safe source owner / acting-for reference
- `audience`: `memory-seam-supervised-live-use`
- `scope`: `source-card-read-proof`
- `approval_ref`: report-safe future HITL approval reference
- `approval_timestamp_ref`: report-safe timestamp reference supplied by the human approval record
- `expires_at_ref`: report-safe expiry reference
- `stop_conditions_ref`: `l6u02.stop.conditions.v1`
- `rollback_expectation_ref`: `l6u02.rollback.expectations.v1`
- `audit_expectation_ref`: `l6u02.audit.expectations.v1`
- `public_hygiene_ref`: `l6u02.public.hygiene.v1`

Approval must be exact, fresh, issue-bound, actor/subject/owner-bound, unexpired, max-one-operation, and scoped to the single operation class above. Any missing, mismatched, broadened, copied, stale, variant, callback-requesting, activation-requesting, publication-requesting, provider/prod/canary, or Atlas Gate-moving approval text is denied before callbacks.

## Packet text is never approval

The following signals are explicitly non-authoritative and must never be recognized as approval:

- this packet text or tests;
- PR merge events;
- issue labels or project fields;
- stale comments;
- issue closure;
- unrelated approvals;
- copied approval language from another issue;
- variant approval wording;
- broad approval wording that increases scope, operation count, source classes, callback families, production authority, provider/prod/canary authority, publication authority, visibility authority, or Atlas Gate authority.

## Denial-before-callback cases

A future preflight must deny before provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks for each case below:

| Case | Required result before callbacks |
| --- | --- |
| `stale_approval` | `DENIED_BEFORE_CALLBACK` because the approval is expired or predates the bound future issue window. |
| `variant_approval` | `DENIED_BEFORE_CALLBACK` because the approval text, class, actor, subject, owner, issue, count, expiry, or scope differs. |
| `copied_approval` | `DENIED_BEFORE_CALLBACK` because approval from another issue or tranche is not portable. |
| `mismatched_approval` | `DENIED_BEFORE_CALLBACK` because actor/subject/owner/audience/scope/issue binding failed. |
| `broadened_approval` | `DENIED_BEFORE_CALLBACK` because more than one operation, more than one class, more sources, or broader recall/source-discovery was requested. |
| `callback_requesting_approval` | `DENIED_BEFORE_CALLBACK` because provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks were requested rather than narrowly approved by a later implementation issue. |
| `activation_requesting_approval` | `DENIED_BEFORE_CALLBACK` because service/listener/startup/cron activation or global Hermes/MCP/client/runtime config mutation was requested. |
| `publication_requesting_approval` | `DENIED_BEFORE_CALLBACK` because package publication or repository visibility change was requested. |
| `provider_prod_canary_approval` | `DENIED_BEFORE_CALLBACK` because provider/prod/canary authority or production authority was requested. |
| `atlas_gate_approval` | `DENIED_BEFORE_CALLBACK` because Atlas Gate movement was requested. |

## Stop conditions and reporting requirements

A later approved proof must stop immediately on expiry, any mismatch, any callback request outside the exact future issue, more than one attempted operation, source discovery pressure, raw content pressure, credential/auth/env/keychain/OAuth/auth-file pressure, Runtime Registry pressure, publication/visibility pressure, provider/prod/canary pressure, production pressure, Atlas Gate pressure, public hygiene failure, or any unsafe report field.

Report-safe receipt fields are limited to public-safe references and counters:

- `issue_ref`
- `operation_class`
- `max_operation_count=1`
- `operation_attempt_count`
- `actor_ref`
- `subject_ref`
- `owner_ref`
- `audience`
- `scope`
- `approval_ref`
- `expires_at_ref`
- `status` with `HOLD`, `DENIED_BEFORE_CALLBACK`, or future review vocabulary supplied by the later approved issue
- `stop_reason_ref`
- `rollback_expectation_ref`
- `audit_expectation_ref`
- `public_hygiene_result`
- `guarded_callback_counters`

The report-safe shape excludes raw source content, source path, source URI, credential material, raw platform identifiers, raw query/payload content, private correlation references, backend response bodies, Runtime Registry data, persistence record bodies, and audit/custody record bodies.

## Rollback, audit, and hygiene expectations

Rollback expectation: because this packet authorizes no execution and the future proof is read-side/report-safe only, rollback must require no mutation rollback and must preserve all write/custody/delete/reindex/rollback/cache-purge behavior as unsupported unless a separate later issue explicitly changes that boundary.

Audit expectation: future evidence may name report-safe references and zero counters, but this packet creates no persistence/audit/custody records and no cache mutation. A later issue must define any audit receipt separately before implementation.

Public hygiene expectation: all artifacts must pass `python scripts/public_hygiene_scan.py` and must not include secrets, credentials, private paths, raw document content, raw prompt/query text, live source identifiers, OAuth/keychain/env material, Runtime Registry references, raw backend responses, or private correlation references.

## Preserved no-go ledger

L6U.02 preserves the full rail hold:

- no implementation or execution of live/private reads;
- no credentials, auth, env, keychain, OAuth, or auth-file reads;
- no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption;
- no Runtime Registry consumption;
- no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- no mutation execution, no `allowed=true` path, no write/custody/delete/reindex/rollback/cache-purge behavior, no persistence/audit/custody records, and no cache mutation;
- no service/listener/startup/cron activation, global Hermes/MCP/client/runtime config mutation, package publication, repository visibility change, provider/prod/canary authority, production authority, or Atlas Gate movement.

## Acceptance evidence

Companion tests prove this packet is HITL-only, future-only, not approval, limited to exactly one future operation class with `max_operation_count=1`, and resistant to approval recognition via packet text, merge events, labels, stale comments, issue closure, unrelated approvals, stale/variant/copied/mismatched/broadened approval text, callback requests, activation requests, publication requests, provider/prod/canary requests, and Atlas Gate requests.
