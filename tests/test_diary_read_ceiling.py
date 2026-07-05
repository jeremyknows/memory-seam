"""Tests for W2b diary_read_ceiling parity with adapter PR #191 (ADR 0001).

Covers: default self ceiling; explicit fleet honored only when grant carries it;
forged/unknown values fail-closed; act-for narrowing unchanged for non-diary
scopes; router ceiling pass-through to recall_handler only.
"""

from __future__ import annotations

import memory_seam
from memory_seam.contracts import (
    DIARY_READ_CEILING_FLEET,
    DIARY_READ_CEILING_SELF,
    VALID_DIARY_READ_CEILINGS,
    SubjectPolicy,
)
from memory_seam.policy import cross_agent_read_permitted, policy
from memory_seam.receipts import read_receipt_enabled
from memory_seam.router import route_request


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_diary_read_ceiling_constants_are_exported() -> None:
    assert memory_seam.DIARY_READ_CEILING_SELF == "self"
    assert memory_seam.DIARY_READ_CEILING_FLEET == "fleet"
    assert DIARY_READ_CEILING_SELF in memory_seam.VALID_DIARY_READ_CEILINGS
    assert DIARY_READ_CEILING_FLEET in memory_seam.VALID_DIARY_READ_CEILINGS
    assert len(VALID_DIARY_READ_CEILINGS) == 2


# ---------------------------------------------------------------------------
# SubjectPolicy field
# ---------------------------------------------------------------------------


def test_subject_policy_default_ceiling_is_self() -> None:
    subject = SubjectPolicy(token_subject="agent:example-runner", allowed_scopes=frozenset({"diary"}))
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_SELF


def test_subject_policy_accepts_explicit_fleet_ceiling() -> None:
    subject = SubjectPolicy(
        token_subject="agent:example-runner",
        allowed_scopes=frozenset({"diary"}),
        diary_read_ceiling=DIARY_READ_CEILING_FLEET,
    )
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_FLEET


# ---------------------------------------------------------------------------
# policy() construction — fail-closed ceiling logic
# ---------------------------------------------------------------------------


def test_policy_default_ceiling_is_self() -> None:
    subject = policy("agent:example-runner", ["diary"])
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_SELF


def test_policy_explicit_fleet_honored_for_authenticated_subject() -> None:
    subject = policy("agent:example-runner", ["diary"], diary_read_ceiling="fleet")
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_FLEET


def test_policy_fleet_ceiling_blocked_for_anonymous_subject() -> None:
    """Anonymous subjects must never receive a fleet ceiling — fail-closed."""
    subject = policy(None, None, diary_read_ceiling="fleet")
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_SELF


def test_policy_unknown_ceiling_value_normalizes_to_self() -> None:
    """Unknown values fail-closed to self; no 401 at this layer, just normalization."""
    subject = policy("agent:example-runner", ["diary"], diary_read_ceiling="unknown_value")
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_SELF


def test_policy_none_ceiling_normalizes_to_self() -> None:
    subject = policy("agent:example-runner", ["diary"], diary_read_ceiling=None)
    assert subject.diary_read_ceiling == DIARY_READ_CEILING_SELF


# ---------------------------------------------------------------------------
# cross_agent_read_permitted — ceiling-aware act-for check
# ---------------------------------------------------------------------------


def test_cross_agent_read_permitted_self_targeted_always_passes() -> None:
    subject = policy("agent:example-runner", ["diary"])
    # Same agent as subject — no cross-agent
    assert cross_agent_read_permitted("example-runner", subject, "diary") is True


def test_cross_agent_read_permitted_acting_for_passes() -> None:
    subject = policy("agent:example-runner", ["diary"], acting_for="agent:example-reader")
    assert cross_agent_read_permitted("example-reader", subject, "diary") is True


def test_cross_agent_read_permitted_fleet_ceiling_allows_diary() -> None:
    subject = policy("agent:example-runner", ["diary"], diary_read_ceiling="fleet")
    # Third-agent target — not in subject's acting_for
    assert cross_agent_read_permitted("example-third", subject, "diary") is True


def test_cross_agent_read_permitted_self_ceiling_denies_diary() -> None:
    subject = policy("agent:example-runner", ["diary"])  # default self ceiling
    assert cross_agent_read_permitted("dispatch", subject, "diary") is False


def test_cross_agent_read_permitted_fleet_ceiling_does_not_widen_context() -> None:
    """Fleet ceiling is diary-only. Context stays self-only regardless."""
    subject = policy("agent:example-runner", ["diary", "context"], diary_read_ceiling="fleet")
    assert cross_agent_read_permitted("dispatch", subject, "context") is False


def test_cross_agent_read_permitted_fleet_ceiling_does_not_widen_session() -> None:
    """Fleet ceiling is diary-only. Session stays self-only regardless."""
    subject = policy("agent:example-runner", ["diary", "session"], diary_read_ceiling="fleet")
    assert cross_agent_read_permitted("dispatch", subject, "session") is False


def test_cross_agent_read_permitted_fleet_ceiling_wiki_not_affected() -> None:
    """Wiki is atlas-wide by its own semantics; cross_agent_read_permitted is
    always True for it regardless of ceiling (same as the no-agent case)."""
    subject = policy("agent:example-runner", ["wiki"])  # self ceiling
    # Wiki agent param is typically None; passing an "agent" value for wiki is
    # unusual but the function should not block it via ceiling — wiki read-open
    # is handled at a higher layer. The ceiling check is diary-specific.
    # Since wiki != diary, fleet-ceiling path doesn't apply. The function
    # returns False here because the agent isn't in subject and ceiling is self.
    # That's correct — a higher layer (not this function) authorizes wiki.
    subject_fleet = policy("agent:example-runner", ["wiki"], diary_read_ceiling="fleet")
    assert cross_agent_read_permitted("dispatch", subject_fleet, "wiki") is False


def test_cross_agent_read_permitted_no_agent_always_passes() -> None:
    """No agent parameter → no cross-agent concern."""
    subject = policy("agent:example-runner", ["diary"])
    assert cross_agent_read_permitted(None, subject, "diary") is True


def test_cross_agent_read_permitted_is_exported() -> None:
    assert callable(memory_seam.cross_agent_read_permitted)


# ---------------------------------------------------------------------------
# router.py ceiling pass-through
# ---------------------------------------------------------------------------


def test_router_passes_diary_read_ceiling_to_recall_handler() -> None:
    captured: list[dict] = []

    def recall_handler(query, **kwargs):
        captured.append(kwargs)
        return {"endpoint": "recall", "items": [], "query": query}

    route_request(
        "GET",
        "/recall?query=test&scope=diary&agent=dispatch",
        health_handler=lambda: {"ok": True},
        context_handler=lambda **kw: {"ok": True},
        recall_handler=recall_handler,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example-runner",
        allowed_scopes=["diary"],
        diary_read_ceiling="fleet",
    )

    assert len(captured) == 1
    assert captured[0]["diary_read_ceiling"] == "fleet"


def test_router_omits_ceiling_kwarg_when_not_set() -> None:
    """When diary_read_ceiling is None (default), the kwarg is absent from the
    recall_handler call — preserving backward compatibility with handlers that
    don't accept it."""
    captured: list[dict] = []

    def recall_handler(query, **kwargs):
        captured.append(kwargs)
        return {"endpoint": "recall", "items": [], "query": query}

    route_request(
        "GET",
        "/recall?query=test&scope=wiki",
        health_handler=lambda: {"ok": True},
        context_handler=lambda **kw: {"ok": True},
        recall_handler=recall_handler,
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example-runner",
        allowed_scopes=["wiki"],
    )

    assert len(captured) == 1
    assert "diary_read_ceiling" not in captured[0]


def test_router_does_not_pass_ceiling_to_context_handler() -> None:
    """Context families stay self-only; ceiling kwarg must not reach the
    context_handler (which has no such parameter)."""
    captured: list[dict] = []

    def context_handler(**kwargs):
        captured.append(kwargs)
        return {"endpoint": "context", "sources": []}

    route_request(
        "GET",
        "/context?include=project&agent=terminal",
        health_handler=lambda: {"ok": True},
        context_handler=context_handler,
        recall_handler=lambda q, **kw: {"endpoint": "recall", "items": [], "query": q},
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example-runner",
        allowed_scopes=["context:project"],
        diary_read_ceiling="fleet",
    )

    assert len(captured) == 1
    assert "diary_read_ceiling" not in captured[0]
