# ADR 0003 — Credentials: permanent values ban; pointer custody is a deployment pattern, not a core feature

**Status:** Accepted (operator decision, 2026-06-09 grill session — operator pre-committed to lead's synthesis after inviting an over-engineering challenge)
**Deciders:** project maintainers

## Context

The operator's stated intent included the seam helping agents who "need credentials and don't know where to find them" — pointer custody (where a credential lives + how to access it), never values. He proposed a deny-first, per-agent allowlisted pointer tier and explicitly asked to be challenged on over-engineering, noting OSS optionality is preferable. Facts weighed: the seam hard-bans credential/auth-material access at every layer (protected-path pre-read denial); the named problem ("agents forget how to use 1Password") is documentation already served by canonical wiki content through the existing receipted read path; on a single-user machine all agents run as one OS user with self-asserted identity, so a pointer allowlist cannot stop a misbehaving local process — it is a decorative wall that creates a real new artifact (a machine-readable index of secret locations); and the seam's existing grant-matrix + source-family model already provides the machinery a multi-user deployment would need to gate such a family.

## Decision

1. **Credential VALUES: banned from the seam permanently.** Written into the Fleet Adoption Contract as non-relitigable (no future class, scope, or grant may serve secret values through the seam).
2. **The pointer need is served by content, not machinery:** the canonical where-secrets-live / how-to-access wiki article flows through the normal receipted read path; keeping that article complete and recallable is a curation duty (eval-corpus question candidate post-proof), not a seam feature.
3. **Pointer-as-a-gated-scope is documented as an OSS deployment pattern** (a `sensitive_pointer` source family gated deny-first via the existing grant matrix) — built in core ONLY when a real multi-user/multi-host deployment or observed demand exists. "Your architecture, our timing."

## Consequences

- W6 (write/custody) architecture is unaffected by credential concerns — a major simplification.
- The OSS docs gain a deployment-pattern page (optionality with zero new core code or attack surface).
- Revisit triggers (named, not open-ended): telemetry showing repeated secret-access task failures, or the fleet going multi-user/multi-host where walls become real.
- Contract v1.2 carries the permanence language (batched with other grill-driven contract deltas).
