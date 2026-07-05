from __future__ import annotations

from dataclasses import dataclass

import pytest

from memory_seam.runtime import IdentityDecision, LocalReadOnlyRuntime, ReadOnlyRuntimeConfig, RuntimeRequest
from memory_seam.providers import NullMemorySeamProvider


class ReadSpyProvider(NullMemorySeamProvider):
    """Provider spy that proves identity denials happen before backend reads."""

    def __init__(self) -> None:
        self.context_calls = 0
        self.recall_calls = 0

    def context(self, **kwargs):  # pragma: no cover - negative cases must not reach this
        self.context_calls += 1
        raise AssertionError("context provider was called after identity denial")

    def recall(self, query, **kwargs):  # pragma: no cover - negative cases must not reach this
        self.recall_calls += 1
        raise AssertionError("recall provider was called after identity denial")

    @property
    def read_calls(self) -> int:
        return self.context_calls + self.recall_calls


@dataclass(frozen=True)
class SyntheticTokenShapeVerifier:
    """Fixture-only token-shape verifier; no credentials, keys, env, OAuth, or keychain."""

    now: int = 100
    required_audience: str = "memory-seam-runtime"

    def verify(self, request: RuntimeRequest) -> IdentityDecision:
        token = request.headers.get("x-memory-seam-token-shape", "")
        if not token.startswith("fixture-token-v0;"):
            return IdentityDecision(allowed=False, reason="invalid_token_shape")
        fields = {}
        for part in token.split(";")[1:]:
            if "=" not in part:
                return IdentityDecision(allowed=False, reason="invalid_token_shape")
            key, value = part.split("=", 1)
            fields[key] = value
        required = {"subject", "audience", "scope", "expires_at"}
        if not required.issubset(fields):
            return IdentityDecision(allowed=False, reason="invalid_token_shape")
        if fields["audience"] != self.required_audience:
            return IdentityDecision(allowed=False, reason="token_audience_mismatch")
        try:
            expires_at = int(fields["expires_at"])
        except ValueError:
            return IdentityDecision(allowed=False, reason="invalid_token_shape")
        if expires_at <= self.now:
            return IdentityDecision(allowed=False, reason="expired_token_shape")
        acting_for = fields.get("acting_for")
        if acting_for and not fields["scope"].startswith("context:"):
            return IdentityDecision(allowed=False, reason="confused_deputy_scope_mismatch")
        return IdentityDecision(
            allowed=True,
            subject=fields["subject"],
            allowed_scopes=frozenset(scope for scope in fields["scope"].split(",") if scope),
            acting_for=acting_for,
        )


def _request(token: str, target: str = "/context?agent=example&include=project", body=None) -> RuntimeRequest:
    return RuntimeRequest(
        "GET",
        target,
        headers={"x-memory-seam-token-shape": token},
        body={} if body is None else body,
    )


def _token(**overrides: str) -> str:
    fields = {
        "subject": "agent:example",
        "audience": "memory-seam-runtime",
        "scope": "context:project",
        "expires_at": "200",
    }
    fields.update(overrides)
    return "fixture-token-v0;" + ";".join(f"{key}={value}" for key, value in fields.items())


@pytest.mark.parametrize(
    ("name", "runtime_request", "expected_error"),
    [
        (
            "forged_subject",
            _request(_token(subject="agent:mallory")),
            "subject_agent_mismatch",
        ),
        (
            "wrong_audience",
            _request(_token(audience="other-runtime")),
            "token_audience_mismatch",
        ),
        (
            "wrong_scope",
            _request(_token(scope="context:memory")),
            "scope_not_allowed",
        ),
        (
            "expired_token_shape",
            _request(_token(expires_at="99")),
            "expired_token_shape",
        ),
        (
            "invalid_token_shape",
            _request("fixture-token-v0;subject=agent:example;scope=context:project"),
            "invalid_token_shape",
        ),
        (
            "query_body_agent_mismatch",
            _request(_token(), body={"agent": "other", "include": "project"}),
            "query_body_identity_mismatch",
        ),
        (
            "query_body_include_mismatch",
            _request(_token(), body={"agent": "example", "include": "memory"}),
            "query_body_identity_mismatch",
        ),
        (
            "confused_deputy_worker_recall",
            _request(
                _token(subject="worker:batch", scope="wiki", acting_for="agent:example"),
                target="/recall?agent=example&scope=wiki&query=boundary",
            ),
            "confused_deputy_scope_mismatch",
        ),
    ],
)
def test_no_service_identity_negative_matrix_denies_before_provider_reads(name, runtime_request, expected_error):
    provider = ReadSpyProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=SyntheticTokenShapeVerifier(),
    )

    response = runtime.handle(runtime_request)

    assert response["status_code"] in {403, 405}, name
    assert response["body"]["error"] == expected_error, name
    runtime_receipt = response["body"]["runtime"]
    assert runtime_receipt["service_started"] is False, name
    assert runtime_receipt["runtime_registry_consumed"] is False, name
    assert runtime_receipt["audit_persisted"] is False, name
    assert runtime_receipt["write_custody_or_reindex"] is False, name
    assert runtime_receipt["audit_receipt"]["privacy_pass"] is True, name
    assert provider.read_calls == 0, name


def test_no_service_identity_negative_matrix_keeps_health_no_service_no_global_mutation():
    provider = ReadSpyProvider()
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True),
        provider=provider,
        identity_verifier=SyntheticTokenShapeVerifier(),
    )

    health = runtime.health()

    assert health["service_started"] is False
    assert health["service_start_allowed"] is False
    assert health["runtime_registry_consumed"] is False
    assert health["audit_persisted"] is False
    assert health["write_custody_or_reindex"] is False
    assert "global_config_mutation" in health["held_surfaces"]
    assert provider.read_calls == 0
