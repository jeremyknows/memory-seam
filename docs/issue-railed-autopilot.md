# Issue-railed autopilot template

This template captures the bounded maintenance pattern used for Memory Seam source-package work. It is a reusable prompt and operating checklist for human-supervised autonomous repo work. It is documentation only: do not create, update, remove, or schedule jobs from this document.

Use it when a repository has a known issue queue, explicit holds, and a safe local verification gate. Keep the run bounded to one short work item unless the operator explicitly assigns a larger harvest.

## Inputs to fill before a run

- **Primary repo:** `<absolute path to the checkout>`
- **GitHub repo:** `<owner>/<repo>`
- **Reference repos:** `<read-only reference paths, if any>`
- **Source deck/channel:** `<private source reference, if any; avoid embedding platform IDs in public docs>`
- **Verified baseline:** `<main commit>`, local test result, public hygiene result, compile/type-check result, and latest CI status
- **Open rails:** issue numbers, titles, priority/order, and any issues that are held
- **Allowed actions:** concrete repo-local actions the agent may take without further confirmation
- **Hard holds:** actions the agent must not take even if technically possible
- **Verification gate:** commands required before push/merge/close
- **Report destination:** where the final summary is delivered by the surrounding scheduler or operator

## Issue rail shape

Each rail should be a normal issue with acceptance criteria that can be verified from repository artifacts. Good rails are small, ordered, and closeable by evidence.

Recommended issue body:

```md
## Goal
One sentence describing the artifact or behavior to add.

## Acceptance
- Repository artifact exists or behavior is covered by tests.
- No live/private reads, credentials, service starts, publication, or global config mutation.
- Local verification gate passes.

## Notes
Any references, downstream consumers, or explicit non-goals.
```

## Bounded autopilot prompt skeleton

```text
You are running a bounded issue-railed autopilot for <repo>. Do not ask questions.
Do not create/update/remove cron jobs from inside this run.

Primary repo: <path>
GitHub: <owner>/<repo>
Reference repos: <paths and read-only/bridge-only boundaries>

Verified baseline:
- main/origin head: <commit>
- Local verification: <commands and results>
- CI: <status>

Open rails now:
- #<n> <title>
- #<n+1> <title>
- #<held> <title> — HOLD unless <condition>

Allowed without further confirmation:
- Create branches/PRs/commits/merges when checks pass.
- Close/update issues based on verified completion.
- Add tests/docs/examples/package metadata/CI-only no-live synthetic tools.

Hard holds:
- Do not make the repository public or publish packages.
- Do not start/install persistent services/listeners.
- Do not read credentials, auth stores, keychains, or secrets.
- Do not mutate global client/runtime configuration.
- Do not perform live/private source reads.
- Do not add write/custody/reindex behavior outside design/test-only packets.

Per-tick operating loop:
1. Verify repo state: git status, origin/main, GitHub auth, open issues, recent PRs/checks.
2. Choose the lowest open safe issue. Prefer code/tests/examples over docs when equally safe.
3. Work on a short-lived branch. Keep changes scoped to the selected issue.
4. Run the required verification gate.
5. Push/open PR. Verify PR metadata. Merge only when local proof and/or CI satisfy the repo policy.
6. After merge, verify origin/main/local main, then close/update the issue only if acceptance is met.
7. Final report: repo head, issue/PR moved, tests run, merges done, blockers/held boundary, next issue target.
```

## Safe execution rules

- Treat credentials, platform identifiers, private paths, and source-deck details as sensitive. Use placeholders in reusable docs.
- Escalate or hold on identity/direction forks, ownership conflicts, high-blast-radius actions, repeated verification failure, or any request that crosses a hard hold.
- Prefer root-cause fixes when they are clearly within the selected rail; otherwise preserve a small diff.
- Never fabricate CI, test, package, or GitHub results. If verification is blocked, report the blocker.
- Do not recurse by spawning a new autopilot or scheduler from inside the run.

## Final harvest checklist

Before the rail set is considered closed, collect a final review packet with:

- merged PRs and closed issues;
- current `origin/main` commit;
- local verification results;
- CI status;
- unresolved holds and why they remain held;
- release/publication decision boundary;
- downstream bridge or migration notes still outstanding.

The harvest packet is a decision aid, not an executable release script.
