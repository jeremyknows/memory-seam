# Memory expansion boundary

Memory Seam can help agents expand usable memory context, but the current package is intentionally a read-only seam core. It does not own profile memory, session artifact storage, live source retrieval, write custody, or reindexing. Operators should treat it as a boundary layer that can normalize and route already-permitted memory context while leaving durable memory authority downstream.

## What Memory Seam can do today

- Define portable contracts for context and recall requests.
- Describe source families and policy posture without requiring Atlas runtime access.
- Route requests through a provider protocol and return structured response envelopes.
- Produce metadata-only read receipts for audit, rollback, and usefulness checks.
- Run a default-off in-process runtime skeleton for tests and explicit local demos.
- Exercise package behavior through synthetic fixtures and committed examples.

These capabilities are enough to prove shape, policy, and usefulness scoring around memory context without touching live/private stores.

## What Memory Seam does not do today

- It does not read live profile memories, Discord, repositories, Runtime Registry, or private source systems by itself.
- It does not start a service, listener, FastMCP server, Hermes tool, or global adapter.
- It does not mutate Hermes profiles, MCP/client config, provider config, gates, or production authority.
- It does not write memories, claim custody, reindex source material, or perform retention/deletion workflows.
- It does not publish packages or change repository visibility.

If an adapter later connects Memory Seam to a real source, that adapter must bring its own identity verification, source authorization, audit sink, operational kill switch, and rollback story. The core package should not silently widen authority.

## Operator-facing memory lanes

### Profile memory

Profile memory is durable agent/user memory owned by the runtime profile or memory system. Memory Seam can describe and route profile-memory-shaped context only when an authorized adapter supplies it. The package does not directly inspect, edit, import, export, or persist profile memories.

### Session artifacts

Session artifacts are per-run files, logs, transcripts, or tool outputs. Memory Seam can help normalize references to already-selected artifacts, but it does not discover session files, scrape worktrees, or decide which artifacts should become long-term memory.

### Read-only seam context

Read-only seam context is the safe current lane: an authorized provider returns bounded context/recall items, and Memory Seam wraps them in contracts, policy decisions, and metadata-only receipts. Synthetic providers and fixtures in this repository prove this lane without live reads.

### Future write custody

Write custody is held. Future work may define companion packets for proposed writes, review gates, retention policy, rollback handles, and custody transfer, but the current repository must keep that work design/test-only. No implementation should create, rewrite, delete, or reindex durable memories until explicit write-custody authority exists.

## Safe expansion pattern

1. Keep the core package default-off and read-only.
2. Require adapters to prove identity, source permission, and audit behavior before live reads.
3. Prefer metadata receipts over content persistence inside Memory Seam.
4. Separate recall/context reads from any proposed write-custody packet.
5. Make held surfaces explicit in docs, tests, and examples.

## Current boundary

This note is a design boundary, not an activation decision. It does not enable unsupervised reads, live adapters, service startup, Runtime Registry consumption, write custody, reindexing, provider/prod/canary authority, package publication, or public release.
