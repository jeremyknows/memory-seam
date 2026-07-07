# L6P.07 supervised live-use next-rail decision packet

Status: `HITL_ISSUE_RAIL_PACKET_ONLY`
Decision: `SELECT_SUPERVISED_LIVE_USE_ISSUE_RAIL`
Parent: #6
Rail issue: #169
Prerequisite: #168 closed/PASS
Source floor: `cce1364` or later
Upstream packet: `docs/l6-live-use-pivot-frontier-packet.md`

This L6P.07 packet is docs/tests only, HITL-only, no-execution, and no-approval. It packages the exact next rail after L6P.06 by selecting a supervised live-use issue rail, not an implementation approval phrase. It does not include future exact approval language, does not approve implementation, does not perform live/private reads, does not read credentials, does not discover sources, does not call provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, does not persist receipts or audit records, does not consume Runtime Registry data, does not mutate global Hermes/MCP/client/runtime configuration, does not activate a service/listener/startup/cron path, does not publish a package, does not change repository visibility, does not claim provider/prod/canary authority, and does not move Atlas Gate.

## Decision

Selected next artifact type: `ISSUE_RAIL`.

Rejected next artifact type: `FUTURE_APPROVAL_PHRASE`.

Reason: L6P.06 selected `SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET` as the next tranche, but the safest next move is a deck-friendly issue rail that separates adapter mapping, approval packet drafting, local synthetic smoke design, dogfood prompt design, and trust-boundary review. That split keeps live/private reads and implementation held until a later issue supplies HITL decision details and Jeremy separately approves any future bounded execution.

This decision is intentionally not ambiguous: the next rail is an issue rail only. No implementation approval phrase is drafted in this packet.

## Carry-forward evidence from L6P.06

L6P.06 summarized the positive-authorization receipt proof and the live-use gap:

- `positive_authorization_recognized_mutation_held` remains receipt-only and mutation-held;
- `allowed=false`, `mutation_attempted=false`, `mutation_supported=false`, and `allowed_result_count=0` remain preserved;
- callback, persistence, source, activation, publication, provider/prod/canary, production, and Atlas Gate surfaces remain held;
- the near-term value gap is one supervised read-side usefulness proof over an operator-approved target, not mutation/custody execution;
- the recommended future tranche is a supervised live-read adapter approval packet, but that packet still needs its own issue-bound HITL drafting and tests before any implementation or execution can be considered.

## Proposed deck-friendly issue rail

The following issue rail is a proposal for Jeremy/operator review. It is not created by this packet and does not recursively schedule cron work.

### L6U.01: supervised live-use adapter wiring map

Scope:
- Docs/tests only.
- Map the minimal adapter boundary for one future supervised live-use proof.
- Name allowed synthetic fixtures, report-safe source-card/descriptor shapes, caller identity fields, and callback families that must remain at zero.
- Define dependency direction for any Atlas Query/Hermes adapter: downstream depends on Memory Seam, not core depending on downstream.

No-go:
- No implementation, no live/private reads, no credentials, no source discovery, no Runtime Registry, no provider/backend/source callbacks, no service/listener/startup/cron activation, no publication, no visibility change, no provider/prod/canary authority, no Atlas Gate movement.

Acceptance:
- Packet is discoverable from docs index and contract-test inventory.
- Tests prove the map is adapter-boundary-only, default-off, no-live, no-callback, no-source-discovery, and no Runtime Registry.
- Tests prove one future proof target shape is named without raw private content or credentials.

### L6U.02: supervised live-read approval packet

Scope:
- Docs/tests only HITL decision packet.
- Draft future-only exact approval requirements for one bounded supervised read-side proof, including issue binding, actor/subject/owner, max one operation, expiry, stop conditions, report-safe receipt fields, rollback/audit expectations, and public hygiene requirements.
- Define stale, variant, copied, mismatched, broadened, callback-requesting, activation-requesting, publication-requesting, provider/prod/canary, and Gate denial cases before callbacks.

No-go:
- The packet itself is not approval.
- No implementation, no live/private reads, no credentials, no source discovery, no Runtime Registry, no callbacks, no persistence, no activation, no publication, no visibility change, no provider/prod/canary authority, no Atlas Gate movement.

Acceptance:
- Tests prove the packet is HITL-only and future-only.
- Tests prove exactly one future operation class and max-one-operation limit.
- Tests prove no approval is recognized from packet text, merge events, labels, stale comments, issue closure, or unrelated approvals.

### L6U.03: local integration smoke design

Scope:
- Docs/tests only, or synthetic fixture-only smoke if separately approved by the rail issue.
- Define a local no-live smoke plan for adapter import/wiring using committed synthetic fixtures only.
- Prove stdout/report output remains public-safe and callback counters remain zero.

No-go:
- No live/private reads, no source discovery, no credentials, no Runtime Registry, no provider/backend/source callbacks, no mutation, no persistence, no service/listener/startup/cron activation, no publication, no visibility change, no provider/prod/canary authority, no Atlas Gate movement.

Acceptance:
- Tests prove the smoke plan is local-only, synthetic-only, default-off, and report-safe.
- Tests prove write/custody/delete/reindex/rollback/cache-purge remain unsupported.
- Tests prove no live adapter is invoked.

### L6U.04: dogfood/use-proof prompt set

Scope:
- Docs/tests only.
- Draft report-safe dogfood prompts and usefulness rubric for one future supervised read-side proof.
- Require answerability, source-card citation, fallback avoidance, degraded/HOLD handling, and public hygiene checks.

No-go:
- No prompt execution against live/private sources, no credentials, no source discovery, no broad recall, no Runtime Registry, no callbacks, no persistence, no activation, no publication, no provider/prod/canary authority, no Atlas Gate movement.

Acceptance:
- Tests prove prompts contain no private/raw content and request no secrets or credentials.
- Tests prove exactly one future proof target and explicit HOLD outcomes for degraded, too-redacted, unsafe, or ambiguous evidence.
- Tests prove the rubric prioritizes usefulness without weakening source/privacy boundaries.

### L6U.05: supervised live-use trust-boundary review

Scope:
- Docs/tests only, no-edit/no-execution review.
- Summarize L6U.01-L6U.04 evidence and decide PASS/HOLD/FIX_BEFORE_NEXT_SLICE before any implementation or live-read approval is considered.
- Verify public hygiene, denial-before-callback design, report-safe receipts, no-production holds, and one-operation bounds.

No-go:
- No implementation, no live/private reads, no credentials, no source discovery, no Runtime Registry, no callbacks, no persistence, no activation, no publication, no visibility change, no provider/prod/canary authority, no Atlas Gate movement.

Acceptance:
- Tests prove PASS/HOLD/FIX_BEFORE_NEXT_SLICE vocabulary only.
- Tests prove the review cannot approve implementation or execution.
- Tests prove all residual holds are restated and no `allowed=true` path is introduced.

## Rail ordering

Recommended order: L6U.01 adapter wiring map → L6U.02 approval packet → L6U.03 local integration smoke design → L6U.04 dogfood/use-proof prompt set → L6U.05 trust-boundary review.

The rail is intentionally parallel-friendly for deck review, but merge/execution order should stay gated: no implementation or live/private read work should begin until the approval packet and trust-boundary review produce an explicit PASS and Jeremy supplies any required fresh approval on the relevant issue.

## Preserved holds

The following surfaces remain held:

- implementation and execution of live/private reads;
- source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, and Runtime Registry consumption;
- mutation execution, `allowed=true` result paths, write execution, custody transfer, custody receipt persistence, delete, reindex, rollback, and cache purge;
- provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- receipt persistence, audit persistence, durable write records, cache mutation, filesystem/database/object storage/remote API/Git/issue-comment custody stores;
- credential/auth/env/keychain/OAuth/auth-file reads;
- service/listener/startup/cron activation and recurring runner behavior;
- global Hermes/MCP/client/runtime configuration mutation;
- package publication, repository visibility changes, provider/prod/canary authority, production authority, and Atlas Gate movement.

## Verification expectation

Any PR in this rail should run:

```bash
python -m pytest -q
python scripts/public_hygiene_scan.py
git diff --check
python -m compileall -q src tests examples
```

This packet's companion tests prove discoverability, HITL-only posture, issue-rail selection, absence of approval phrase selection, proposed issue titles/scopes/no-go/acceptance coverage, rail ordering, report safety, and preserved holds.
