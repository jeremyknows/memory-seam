# L6P.06 live-use pivot frontier packet

Status: `LIVE_USE_PIVOT_FRONTIER_PACKET_ONLY`
Review verdict: `RECOMMEND_SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET`
Parent: #6
Rail issue: #168
Prerequisite: #167 closed/PASS
Source floor: `cce1364` or later
Reviewed evidence: `docs/l6-positive-authorization-trust-boundary-review.md`; `docs/l6-positive-authorization-receipt-skeleton.md`; `docs/l6-positive-authorization-denial-hardening.md`; `docs/l6-positive-authorization-report-hygiene.md`; `docs/l6-positive-authorization-no-production-smoke.md`

This L6P.06 packet is docs/tests only, no-execution, no-approval, and decision-only. It compares the next plausible tranche after the positive-authorization receipt skeleton proof and recommends exactly one future tranche. It does not implement behavior, approve live use, perform live/private reads, discover sources, call provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks, execute mutation, persist receipts or audit records, consume Runtime Registry data, read credential/auth/env/keychain/OAuth/auth-file material, mutate global Hermes/MCP/client/runtime configuration, activate a service/listener/startup/cron path, publish a package, change repository visibility, claim provider/prod/canary authority, or move Atlas Gate.

The recommendation is a frontier choice only. It is not approval language, not approval by implication, not a provider/prod/canary grant, and not permission to read private/live sources. Any future tranche still needs its own issue-bound HITL decision packet, exact approval fields, expiry, maximum operation count, stop conditions, rollback/audit expectations, public hygiene proof, and denial-before-callback tests before implementation or execution.

## L6P evidence summary

L6P.01-L6P.05 proved a narrow synthetic/no-production positive-authorization receipt skeleton:

- exact issue #163 approval-field recognition for `L6_POSITIVE_AUTHORIZATION_RECEIPT_SKELETON` only;
- status exactly `positive_authorization_recognized_mutation_held`;
- `allowed=false`, `mutation_attempted=false`, `mutation_supported=false`, `allowed_result_count=0`, `operation_count=1`, and `max_operation_count=1`;
- non-persistent report-safe receipt metadata only, with `fixture_is_persistent=false`, `persistent_receipt_count=0`, `durable_write_record_count=0`, `audit_persistence_count=0`, and `cache_mutation_count=0`;
- stale, variant, copied, mismatched, unsafe, live-read, callback, activation, publication, provider/prod/canary, and Gate attempts deny before callbacks;
- report hygiene rejects raw approval text, private source text, credentials, token-shaped input, private paths, raw platform IDs, raw query/payload content, and private correlation refs before reportable positive receipt output;
- L6P.05 recorded PASS while keeping all production, mutation, persistence, callback, source, activation, publication, provider/prod/canary, and Atlas Gate surfaces held.

This evidence is useful but it proves authorization-recognition safety, not operator-facing answer usefulness. The live-use gap is that Memory Seam still lacks an approved, bounded, supervised path for one operator-valuable read-side proof over actual operator context. The current repository already has synthetic quickstarts, source-card usefulness proof, no-service identity semantics, Atlas Query bridge docs, and a prior L5 one-read receipt packet, but this L6P rail has not selected the next post-authorization frontier.

## Candidate comparison

| Candidate | Near-term operator value | Safety/readiness fit | Why not selected now |
| --- | --- | --- | --- |
| Next L6 custody persistence planning | Medium for future write/custody durability; low immediate answer usefulness | Would stay docs/tests-only and can preserve holds | It deepens mutation/custody planning while the biggest current gap is useful read-side proof. It risks spending the next tranche on storage semantics before proving live-use value. |
| Supervised live-read adapter approval packet | High: creates the narrow HITL decision frame for one future bounded read-side value proof | Fits the next frontier if kept packet-only: no read, no implementation, no credentials, exact future approval, max-one operation, denial-before-callback, public hygiene | Selected. It addresses usefulness without executing a read in this tranche. |
| Hermes/Atlas Query integration smoke | Medium-high for downstream integration confidence | Useful after a supervised approval model names the read target, stop conditions, and report shape | Too implementation-adjacent as the immediate next move unless the approval packet first bounds adapter/source/read authority. |
| Dogfood/use-proof prompt set | Medium for evaluation design and operator taste | Safe as docs/tests-only, but weaker than an approval packet for unlocking real value | Better as evidence inside or after the supervised approval packet, not the primary next tranche. |

## Exactly one recommended next tranche

Recommended next tranche: `SUPERVISED_LIVE_READ_ADAPTER_APPROVAL_PACKET`.

The next issue should be a docs/tests-only HITL decision packet for one future supervised live-read adapter/use-proof slice. It should prioritize near-term useful read-side benefit while preserving all current holds until fresh approval exists. The packet should define:

1. exactly one future read-side operation class, such as `L6_SUPERVISED_LIVE_READ_ADAPTER_ONE_PROOF`;
2. exactly one operator-approved target shape, supplied by the operator as a report-safe source-card or bounded descriptor, with no source discovery or broad recall;
3. max one operation, short expiry, explicit actor/subject/owner binding, and exact approval phrase requirements;
4. denial-before-callback proof for stale, variant, mismatched, copied, broadened, unsafe, callback-requesting, source-discovery, activation, publication, provider/prod/canary, and Gate attempts;
5. report-safe receipt fields that exclude raw private source text, credentials, auth/env/keychain/OAuth/auth-file material, private paths, raw platform IDs, raw query/payload content, private correlation refs, and token-shaped inputs;
6. stop conditions for hygiene failure, missing approval, callback counter movement, unexpected persistence, more than one operation, degraded usefulness, or ambiguous trust boundary;
7. rollback/audit expectations that do not require persistent storage in the packet tranche;
8. public hygiene and full verification gates before any later implementation PR.

This recommendation is singular. The packet rejects parallel recommendation of custody persistence planning, immediate Atlas Query smoke implementation, or dogfood prompt-set-only work as the next tranche.

## Preserved holds

The following surfaces remain held after this packet:

- any implementation or execution of live/private reads;
- source discovery, workspace scans, family scans, broad recall, index queries, source-stat calls, source-read calls, provider/backend callbacks, or Runtime Registry consumption;
- mutation execution, `allowed=true` result paths, write execution, custody transfer, custody receipt persistence, delete, reindex, rollback, and cache purge;
- provider/backend/source-stat/source-read/write/custody/delete/reindex/rollback/cache-purge callbacks;
- receipt persistence, audit persistence, durable write records, cache mutation, filesystem/database/object storage/remote API/Git/issue-comment custody stores;
- credential/auth/env/keychain/OAuth/auth-file reads;
- service/listener/startup/cron activation or recurring runner behavior;
- global Hermes/MCP/client/runtime configuration mutation;
- package publication, repository visibility changes, provider/prod/canary authority, production authority, and Atlas Gate movement.

## Acceptance evidence

The companion tests prove this packet is discoverable from the docs index and contract-test inventory, remains docs/tests-only and no-approval, summarizes L6P evidence, names the live-use gap, compares all four requested candidates, recommends exactly one next tranche, prioritizes supervised read-side usefulness, rejects parallel recommendations, and preserves positive-authorization receipt invariants and hard holds.
