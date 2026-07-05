from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from memory_seam.runtime import (
    LocalReadOnlyRuntime,
    RUNTIME_HELD_SURFACES,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "l6-write-intent-threat-model.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_l6_threat_model_states_no_write_implementation_added():
    text = normalized(DOC)

    required_terms = [
        "L6.01 write-intent threat model and custody boundary",
        "NO WRITE IMPLEMENTATION ADDED",
        "threat model and custody-boundary note only",
        "does not add, enable, schedule, authorize, simulate, or execute write/custody/reindex/delete/cache-purge behavior",
        "Memory Seam remains a read-only, default-off package surface",
        "Write implementation: `UNSUPPORTED_HELD`",
        "Custody implementation: `UNSUPPORTED_HELD`",
        "Delete implementation: `UNSUPPORTED_HELD`",
        "Reindex implementation: `UNSUPPORTED_HELD`",
        "Cache purge implementation: `UNSUPPORTED_HELD`",
    ]
    for term in required_terms:
        assert term in text


def test_l6_threat_model_distinguishes_write_custody_and_read_receipts():
    text = normalized(DOC)

    required_terms = [
        "Write intent | A request, proposal, or plan to mutate memory/source/custody state",
        "Custody | Ownership and responsibility for approving, sequencing, recording, and rolling back any future memory/source mutation",
        "Delete | Removing memory/source/index/cached state or marking it as removed",
        "Reindex | Rebuilding, refreshing, or changing retrieval/index state",
        "Cache purge | Invalidating or removing cached read/source/index artifacts",
        "Read receipt | Metadata-only evidence that a read-only request was allowed, denied, or degraded",
        "read receipts are not custody receipts and cannot authorize mutation",
    ]
    for term in required_terms:
        assert term in text


def test_l6_threat_model_lists_future_approval_and_audit_requirements():
    text = normalized(DOC)

    required_terms = [
        "Required future approvals before any write/custody design or execution",
        "Jeremy must provide explicit approval naming the exact slice",
        "issue number and document path for the approved slice",
        "operation class: write intent, custody receipt design, delete, reindex, cache purge, or implementation",
        "maximum number of operations and timeout/expiry",
        "required denial-before-callback counters",
        "custody owner and human review path",
        "Future audit fields required before mutation is even designed",
        "`operation_class` from `write_intent`, `custody`, `delete`, `reindex`, `cache_purge`, or `read_receipt`",
        "`approval_issue` and `approval_phrase_hash` or other report-safe approval reference",
        "posture counters proving zero provider/backend/source/file-stat/custody/reindex callbacks when denied",
        "`write_custody_or_reindex` boolean, expected to remain `false` until a later explicit unhold",
    ]
    for term in required_terms:
        assert term in text


def test_l6_threat_model_preserves_held_surfaces_and_public_hygiene():
    text = normalized(DOC)

    required_terms = [
        "service/listener/cron/startup activation",
        "credential/auth/env/keychain/OAuth/auth-file material",
        "Runtime Registry consumption",
        "global Hermes/MCP/client/runtime configuration mutation",
        "live/private source reads",
        "source discovery",
        "repository visibility change",
        "package publication",
        "provider/prod/canary authority",
        "Atlas Gate movement",
        "raw private source text",
        "private absolute paths",
        "raw platform IDs",
        "raw query payloads",
        "private correlation refs",
        "Write-like denial bodies must use stable reason codes instead of echoing raw payloads",
    ]
    for term in required_terms:
        assert term in text


def test_current_runtime_write_custody_surfaces_remain_unsupported_before_callbacks():
    class ProviderSpy:
        def __init__(self) -> None:
            self.health_calls = 0
            self.context_calls = 0
            self.recall_calls = 0
            self.file_stat_calls = 0
            self.read_backend_calls = 0
            self.write_custody_or_reindex = False

        def health(self):
            self.health_calls += 1
            return {"ok": True}

        def context(
            self,
            *,
            include: list[str],
            mode: str,
            agent: str | None,
            token_subject: str | None,
            allowed_scopes: Iterable[str] | None,
            acting_for: str | None,
            timeout_ms: int,
            context_sources: Any = None,
            context_source_allowlist: Any = None,
            include_read_receipt: bool = False,
        ) -> dict[str, Any]:
            self.context_calls += 1
            raise AssertionError("context provider must not run for write-like denial")

        def recall(
            self,
            query: str,
            *,
            scope: str,
            agent: str | None,
            token_subject: str | None,
            allowed_scopes: Iterable[str] | None,
            acting_for: str | None,
            n: int,
            timeout_ms: int,
            context_sources: Any = None,
            context_source_allowlist: Any = None,
            include_read_receipt: bool = False,
        ) -> dict[str, Any]:
            self.recall_calls += 1
            raise AssertionError("recall provider must not run for write-like denial")

    provider = ProviderSpy()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=StaticIdentityVerifier(subject="agent:example"),
    )

    for method, target in [
        ("POST", "/diary/append"),
        ("POST", "/delete"),
        ("POST", "/reindex"),
    ]:
        response = runtime.handle(
            RuntimeRequest(
                method=method,
                target=target,
                body={"unsafe_payload": "redacted-by-test"},
            )
        )
        body = response["body"]
        runtime_receipt = body["runtime"]

        assert response["status_code"] == 405
        assert body["error"] == "write_like_route_unavailable"
        assert runtime_receipt["write_custody_or_reindex"] is False
        assert runtime_receipt["read_only"] is True
        assert runtime_receipt["rollback"]["write_custody_or_reindex_required"] is False

    assert provider.health_calls == 0
    assert provider.context_calls == 0
    assert provider.recall_calls == 0
    assert provider.file_stat_calls == 0
    assert provider.read_backend_calls == 0
    assert provider.write_custody_or_reindex is False
    assert "write_custody_reindex" in RUNTIME_HELD_SURFACES


def test_idle_tick_write_custody_remains_held_without_side_effects():
    tick = LocalReadOnlyRuntime().idle_tick()

    assert tick["write_custody_or_reindex"] is False
    assert tick["write_custody_unheld"] is False
    assert tick["read_backend_called"] is False
    assert tick["source_read_called"] is False
    assert tick["file_stat_called"] is False
    assert tick["service_started"] is False
    assert tick["runtime_registry_consumed"] is False
    assert tick["global_config_mutation"] is False


def test_l6_threat_model_is_discoverable():
    docs_index = normalized(DOCS_INDEX)
    inventory = normalized(CONTRACT_TEST_INVENTORY)

    assert "l6-write-intent-threat-model.md" in docs_index
    assert "tests/test_l6_write_intent_threat_model.py" in inventory
    assert "L6.01 write-intent threat model and custody boundary" in inventory
