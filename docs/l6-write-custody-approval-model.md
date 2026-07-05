# L6S.01 write/custody ownership and approval model

Status: `schema_fixture_implementation_held`.

Execution authority: `HELD_UNTIL_EXACT_JEREMY_APPROVAL`.

This packet defines the ownership and approval semantics for a future bounded L6 write/custody implementation slice. It is planning/design only: it does not implement, authorize, activate, schedule, simulate, or execute writes, custody transfer, delete, reindex, rollback, cache purge, service/listener/cron/startup behavior, recurring runners, source discovery, unsupervised reads, live/private source reads, provider/backend calls, Runtime Registry consumption, global Hermes/MCP/client/runtime configuration mutation, provider/prod/canary authority, package publication, repository visibility changes, Atlas Gate movement, or production-authoritative claims.

## Required approval fields

Every future implementation issue that asks to unhold write/custody behavior must include all of these fields before code may cross the held surface:

| Field | Requirement | Public/report-safe rule |
| --- | --- | --- |
| `approval_phrase_ref` | Identifies the exact future approval phrase location and confirms that variants, partial quotes, merge events, issue closure, emoji reactions, or unrelated comments are not approval. | Use a report-safe reference, not raw private platform IDs or private correlation refs. |
| `approval_issue` | Names the future issue number that scopes the approval. | Public issue numbers are allowed; do not include private raw platform IDs. |
| `operation_class` | Must be exactly one of `write_intent`, `custody_receipt_persistence`, `delete_intent`, `reindex_intent`, `rollback_intent`, or `cache_purge_intent`. | Do not include raw payload content or raw query payloads. |
| `custody_owner_role` | Names the accountable custody owner role for the data/memory surface. | Role/class only; no private source text, private paths, or credentials. |
| `approver_role` | Names Jeremy as the exact human approver required for implementation unhold. | Role/reference only; no auth/env/keychain/OAuth/auth-file material. |
| `actor_binding` | Binds the approved actor and acting-for subject that may perform the future bounded operation. | Use synthetic or report-safe actor refs only. |
| `expires_at` | Defines the timestamp or duration when authority expires and the slice must stop. | Do not encode private correlation refs. |
| `max_operation_count` | Defines the maximum number of allowed future operations; the schema fixture requires a positive integer and uses `1` in every sample. | Count only; no raw payload or source details. |
| `report_safe_reference` | Provides a public-safe approval reference suitable for issue/PR/receipt artifacts. | Must exclude raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, and private correlation refs. |

## Ownership model

- The `custody_owner_role` is accountable for memory/source custody outcomes, auditability, rollback readiness, and stop conditions.
- The `approver_role` is the human approval authority. For this rail that role is `jeremy_exact_human_approver_required`.
- The `actor_binding` must name the exact future actor and acting-for subject. A broad agent class, implied repo access, merge permission, or cron identity is insufficient.
- Ownership does not transfer just because a schema fixture exists, a PR merges, or an issue closes. The fixture records required semantics only.

## Approval model

A future approval is valid only when all required fields are present, the exact phrase is posted for the named issue, the operation class matches the future slice, the actor binding matches the actor attempting the operation, the approval has not expired, the maximum operation count has remaining capacity, and the public artifact can reference approval without leaking private material.

This L6S.01 packet is not approval. It cannot be used to perform writes, custody transfer, delete, reindex, rollback, cache purge, or any write-like mutation. It cannot be combined with previous L6 no-op fixtures to imply implementation authority.

## Schema fixture

`src/memory_seam/write_custody_approval.py` defines `L6_WRITE_CUSTODY_APPROVAL_FIXTURES` with one public-safe fixture for each operation class:

- `write_intent`
- `custody_receipt_persistence`
- `delete_intent`
- `reindex_intent`
- `rollback_intent`
- `cache_purge_intent`

Each fixture records:

- schema/status fields showing `schema_fixture_implementation_held`;
- exact approval field placeholders;
- custody owner, approver, actor binding, expiry, max-operation-count, and report-safe approval reference requirements;
- zero side-effect counters for write, custody, delete, reindex, rollback, cache purge, provider, backend, source discovery, source stat, source read, Runtime Registry, and activation callbacks;
- held surfaces for write/custody/delete/reindex/rollback/cache-purge execution, source discovery, live/private reads, unsupervised reads, recurring runner or activation behavior, credential/auth/env/keychain/OAuth/auth-file reads, provider/prod/canary authority, publication, visibility change, and Atlas Gate movement;
- report-safety flags excluding raw private source text, credentials/auth material, private paths, raw platform IDs, raw query payloads, raw payload content, and private correlation refs.

## Preserved held surfaces

Unless Jeremy posts exact future approval for a named implementation slice, these surfaces remain held:

- write/custody/reindex/delete/cache-purge/rollback behavior;
- service/listener/cron/startup activation, recurring runners, and recurring unsupervised reads;
- unsupervised reads, live/private source reads, and source discovery;
- credential/auth/env/keychain/OAuth/auth-file reads;
- Runtime Registry consumption;
- global Hermes/MCP/client/runtime configuration mutation;
- provider/prod/canary authority;
- repository visibility change and package publication;
- Atlas Gate movement and production-authoritative claims;
- public artifacts containing raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, raw payload content, or private correlation refs.

## Verification

`tests/test_l6_write_custody_approval_model.py` proves the doc and fixtures are discoverable, require exact approval fields, enforce actor/expiry/max-operation-count/report-safe approval references, preserve zero side effects, reject unsafe fixture regressions with report-safe error codes, and keep all implementation and activation surfaces held.
