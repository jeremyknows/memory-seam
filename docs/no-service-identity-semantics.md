# No-service identity semantics note

## Decision

Memory Seam's F4 identity model remains an in-process, no-service authority contract. It can prove whether a request is safe for the local read-only runtime to route through committed synthetic providers; it cannot prove production user identity, service tenancy, credential validity, multi-machine trust, persistent listener safety, or any live-source entitlement.

A request is eligible for read-only routing only after these identity axes agree before provider, backend, file, stat, discovery, Runtime Registry, service, credential, write, custody, or reindex behavior:

1. **Caller subject:** the verified token or fixture verifier subject, such as `agent:example`; request body, query parameters, ambient process identity, or caller assertions cannot create this subject.
2. **Acting-for:** optional delegation metadata carried by the verifier result. It is audit context, not permission by itself, and it cannot widen scope.
3. **Audience / scope:** the token-shaped authority must name the intended Memory Seam runtime audience and exact read scope family before the runtime considers routing.
4. **Descriptor subject:** any descriptor/grant/source-floor check remains tied to the verified subject and requested family. Descriptor presence is not identity proof.
5. **Query/body subject mismatch:** duplicate subject, include, or scope fields in query and body must agree. Mismatch denies before routing so callers cannot smuggle a different subject or family through a secondary channel.

The portable package therefore treats identity, audience/scope, descriptor/grant authority, and query/body agreement as an intersection, not a union. If any axis fails, the request denies before source materialization and the receipt remains metadata-only.

## What no-service identity authority can prove

The current no-service identity semantics can prove all of the following for deterministic local tests and examples:

- a fixture verifier can return an exact caller subject, allowed scopes, and optional acting-for metadata without reading credentials, env vars, OAuth stores, keychains, auth files, Runtime Registry entries, or live sources;
- forged subject, wrong audience, wrong scope, expired/invalid token shape, query/body mismatch, and confused-deputy worker-vs-interactive paths deny before provider/backend reads;
- read-only runtime receipts expose reportable-safe reason codes and no-service posture booleans such as `service_started=false`, `runtime_registry_consumed=false`, `audit_persisted=false`, and `write_custody_or_reindex=false`;
- denial tests can assert zero provider/backend/read/stat activity with a spy or equivalent monkeypatch assertion;
- acting-for metadata may be recorded in metadata-only audit receipts, but it does not grant source access.

## What no-service identity authority cannot prove

This note does not claim or authorize any of these surfaces:

- real credential, keychain, OAuth, auth-file, environment-secret, or external identity-provider verification;
- persistent service/listener activation, installation, localhost binding, public binding, cron/startup injection, or daemon behavior;
- Runtime Registry runtime consumption or global Hermes, MCP, client, or runtime configuration mutation;
- live/private source reads, source discovery, provider/prod/canary authority, unsupervised reads, or broad recall authority;
- writes, custody, reindex, thread-retirement behavior, persistent audit sink writes, package publication, repository visibility changes, or Atlas Gate movement;
- multi-agent, multi-machine, multi-user, or production service identity acceptance.

Issue `#6` remains held unless Jeremy explicitly unholds it. Any future F5 local persistent read-only service pilot needs a separate verifier packet and explicit authorization before service/listener work begins.

## Identity axis semantics

| Axis | Contract meaning | Fail-closed reason shape | No-service boundary |
| --- | --- | --- | --- |
| Caller subject | Subject returned by the verifier, not the request body or query. | `identity_verifier_unconfigured`, `invalid_token_shape`, or subject mismatch. | Fixture verifiers only; no credential/auth/env/keychain/OAuth/auth-file reads. |
| Acting-for | Delegation/audit metadata that may accompany a verified subject. | confused-deputy or acting-for scope mismatch. | Metadata only; cannot widen source family, subject, or scope. |
| Audience / scope | Intended runtime audience plus exact allowed context/recall family. | `token_audience_mismatch`, `scope_not_allowed`, unsupported include/scope. | No Runtime Registry, provider/prod, service tenancy, or live-source claim. |
| Descriptor subject | Descriptor/grant lookup subject must intersect with the verified subject. | descriptor/grant missing, disabled, or subject mismatch. | Descriptor presence is not identity proof and cannot discover sources. |
| Query/body mismatch | Duplicate request fields must agree across query and body. | `query_body_identity_mismatch`. | Denial happens before router/provider handling and before reads. |

## Denial-before-read evidence rule

Identity denials must happen before source/provider/file/stat/backend reads whenever the failure can be detected from verifier output and request metadata. Focused tests should use provider spies, backend counters, stat monkeypatches, or equivalent assertions and report zero source-read/stat/backend counters for negative paths.

Safe public evidence may include issue and PR numbers, command names, PASS/FAIL status, sanitized reason codes, booleans, and aggregate counters. Public issue/PR artifacts must not include raw private source text, credentials, auth/env/keychain material, raw platform IDs, private absolute paths, raw query payloads, or private correlation references.

## Current F4 evidence pointer

F4.01 added `tests/test_no_service_identity_negative_matrix.py`, which covers forged subject, wrong audience/scope, expired or invalid fixture token shape, query/body mismatch, confused-deputy routing, and no-service health posture. That matrix is the behavioral proof floor for this semantics note; this note explains the authority meaning without adding a service, credential verifier, live adapter, write path, or production claim.

## Next evidence needed

The F4 verifier packet should collect the merged F4 issue/PR/test/doc evidence and decide whether local read-only service design remains design-only or requires more no-service work. It must explicitly preserve the no persistent listener/service boundary and recommend any later F5 design-only packet while keeping execution held.
