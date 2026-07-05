# L6U.04 dogfood/use-proof prompt set

Status: `REPORT_SAFE_DOGFOOD_PROMPT_SET_NOT_EXECUTION`

Parent: #6  
Issue: #180  
Source floor: `1299f4f` or later on `origin/main`  
Upstream packet: `docs/l6-supervised-live-use-next-rail-decision-packet.md`  
Prerequisites: L6U.01 closed/PASS adapter wiring map and L6U.02 packet shape available

This packet drafts report-safe dogfood prompts and a usefulness rubric for one future supervised read-side proof. It is documentation and contract-test evidence only. It does not execute prompts, implement adapters, perform live/private reads, discover sources, run broad recall, read credentials, call provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, consume Runtime Registry data, persist receipts, mutate caches, activate services, publish packages, change repository visibility, claim provider/prod/canary authority, move Atlas Gate, or recognize any approval.

## One future use-proof target

Future dogfood target: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.

The prompt set is limited to exactly one future proof target and exactly one supervised read-side operation class. It may only be used after a later exact HITL-approved issue binds the actor, subject, owner, source-card descriptor, expiry, and max-one-operation limit described by L6U.02. This packet itself is future-only, HITL-only, and not approval to connect to private sources.

The future use-proof goal is narrow: evaluate whether a report-safe source-card/descriptor read-side proof helps an operator answer bounded orientation/current-truth questions without weakening source, privacy, callback, production, or Gate boundaries.

## Report-safe dogfood prompt set

The following prompts are templates only. They must not be executed by this packet. A later approved proof may instantiate placeholders only with report-safe references, never raw private content, secrets, source paths, source URIs, backend responses, Runtime Registry references, raw query text, or private correlation references.

### Prompt A — answerability from source card

`Using only the approved report-safe source-card descriptor <source_card_ref> for <proof_subject_ref>, answer the bounded operator question <question_ref>. Cite the source-card reference, state whether the evidence was sufficient, and return HOLD if the descriptor is degraded, too redacted, unsafe, ambiguous, or missing.`

Purpose: prove answerability from the source-card descriptor before any fallback. Required citation: `source_card_ref`. Required fallback stance: `fallback_avoided=true` unless the answer is HOLD.

### Prompt B — current-truth continuity check

`Using only the approved report-safe descriptor <descriptor_ref>, identify the current accepted/held/next-action state for <proof_subject_ref>. Cite the descriptor reference, avoid raw content, and return HOLD if the evidence is degraded, too redacted, unsafe, ambiguous, stale, or mismatched.`

Purpose: prove operator usefulness for current-truth orientation while preserving report-safe evidence. Required citation: `descriptor_ref`. Required output must be metadata-only and public-safe.

### Prompt C — boundary-aware degraded handling

`Using only the approved report-safe references <source_card_ref> and <descriptor_ref>, decide whether the proof can answer <question_ref> without live/private reads, source discovery, broad recall, credentials, callbacks, Runtime Registry consumption, activation, publication, provider/prod/canary authority, or Atlas Gate movement. If any boundary would be needed, return HOLD and name the public-safe hold reason.`

Purpose: prove the operator sees useful HOLD outcomes rather than unsafe fallback. Required HOLD outcomes include `HOLD_DEGRADED_EVIDENCE`, `HOLD_TOO_REDACTED`, `HOLD_UNSAFE_EVIDENCE`, and `HOLD_AMBIGUOUS_EVIDENCE`.

## Public-safe prompt inputs

Allowed future placeholder fields:

- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.
- `source_card_ref`: report-safe synthetic or approved source-card reference.
- `descriptor_ref`: report-safe synthetic or approved descriptor reference.
- `proof_subject_ref`: report-safe subject reference.
- `caller_subject_ref`: report-safe caller identity reference.
- `acting_for_ref`: report-safe owner / acting-for reference.
- `question_ref`: report-safe question identifier, not raw prompt/query text.
- `approval_packet_ref`: report-safe pointer to the L6U.02 packet shape, not approval.

Forbidden prompt inputs and outputs: raw source content, private/raw content, secrets, credentials, token-like material, env values, OAuth material, keychain material, auth-file content, private paths, source URIs, raw platform identifiers, raw prompts, raw queries, raw payload content, raw backend responses, Runtime Registry references, audit/custody bodies, persistence bodies, source discovery results, broad recall output, or private correlation references.

## Usefulness rubric

A later approved dogfood proof must score each prompt with this public-safe rubric:

| Rubric dimension | PASS requirement | HOLD requirement |
| --- | --- | --- |
| Answerability | The answer is supported by only the approved report-safe source-card/descriptor reference. | `HOLD_TOO_REDACTED` or `HOLD_AMBIGUOUS_EVIDENCE` if support is insufficient. |
| Citation | The answer cites `source_card_ref` or `descriptor_ref` and no raw private content. | `HOLD_UNSAFE_EVIDENCE` if citation would reveal raw/private material. |
| Fallback avoidance | The answer avoids broad recall, source discovery, raw source reads, provider/backend callbacks, and Runtime Registry consumption. | `HOLD_DEGRADED_EVIDENCE` if a safe answer would require any held fallback. |
| Boundary preservation | The answer preserves no-live, no-callback, no-production, no-activation, no-publication, no-provider/prod/canary, and no-Gate holds. | `HOLD_UNSAFE_EVIDENCE` if usefulness depends on weakening any held boundary. |
| Operator value | The answer gives a concise accepted/held/next-action or bounded orientation result using metadata-only evidence. | `HOLD_AMBIGUOUS_EVIDENCE` if it cannot improve operator decision quality without unsafe detail. |

The rubric prioritizes usefulness only when source and privacy boundaries remain unchanged. It measures usefulness without weakening any held boundary. A useful-looking answer that requires raw content, credentials, source discovery, broad recall, callbacks, Runtime Registry consumption, production authority, provider/prod/canary authority, activation, publication, or Atlas Gate movement is a HOLD, not a lower-scored pass.

## Required public result shape

A future report must include only these report-safe fields:

- `status`: one of `DOGFOOD_USE_PROOF_PROMPT_PASS`, `HOLD_DEGRADED_EVIDENCE`, `HOLD_TOO_REDACTED`, `HOLD_UNSAFE_EVIDENCE`, or `HOLD_AMBIGUOUS_EVIDENCE`.
- `operation_class`: `SUPERVISED_REPORT_SAFE_SOURCE_CARD_READ_PROOF`.
- `prompt_id`: `prompt_a_answerability_from_source_card`, `prompt_b_current_truth_continuity_check`, or `prompt_c_boundary_aware_degraded_handling`.
- `source_card_ref` or `descriptor_ref`.
- `citation_present`.
- `fallback_avoided`.
- `public_hygiene_result`.
- `guarded_callback_counters`: all guarded callback families fixed at zero.
- `live_private_read_count`: `0`.
- `source_discovery_count`: `0`.
- `runtime_registry_consumption_count`: `0`.

The result must not echo raw prompts, raw private content, source paths, source URIs, credentials, token-like material, env values, OAuth material, keychain material, auth-file content, raw backend responses, Runtime Registry references, audit/custody bodies, persistence bodies, source discovery results, broad recall output, or private correlation references.

## Preserved rail hold

L6U.04 preserves the full rail hold:

- no prompt execution against live/private sources;
- no implementation or execution of live/private reads;
- no credentials, auth, env, keychain, OAuth, or auth-file reads;
- no source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption;
- no Runtime Registry consumption;
- no provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- no mutation execution, no `allowed=true` path;
- no persistence/audit/custody records;
- no cache mutation;
- no service/listener/startup/cron activation;
- no global Hermes/MCP/client/runtime config mutation;
- no package publication;
- no repository visibility change;
- no provider/prod/canary authority;
- no production authority;
- no Atlas Gate movement.

Companion tests prove this prompt set is discoverable from the docs index and contract-test inventory, docs/tests-only, future-only, report-safe, no-live, no-callback, no-source-discovery, broad-recall-free, Runtime-Registry-free, and bounded to exactly one future proof target with explicit HOLD outcomes for degraded, too-redacted, unsafe, or ambiguous evidence.
