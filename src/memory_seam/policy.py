"""Portable Memory Seam policy helpers."""

from __future__ import annotations

from typing import Any, Iterable

from .contracts import (
    CONTEXT_SCOPE_PREFIX,
    DIARY_READ_CEILING_FLEET,
    DIARY_READ_CEILING_SELF,
    VALID_CONTEXT_INCLUDES,
    VALID_SCOPES,
    SubjectPolicy,
)


def policy(
    token_subject: str | None,
    allowed_scopes: Iterable[str] | None,
    acting_for: str | None = None,
    diary_read_ceiling: str | None = None,
) -> SubjectPolicy:
    default_scopes = {"wiki", "diary", "context"} if token_subject else {"wiki"}
    raw_scopes = frozenset(default_scopes if allowed_scopes is None else allowed_scopes)
    scopes = frozenset(
        scope
        for scope in raw_scopes
        if scope in VALID_SCOPES or scope.removeprefix(CONTEXT_SCOPE_PREFIX) in VALID_CONTEXT_INCLUDES
    )
    # Fail-closed: only the exact "fleet" sentinel widens; unknown/missing
    # values (and any anonymous subject) keep the self-only ceiling.
    ceiling = (
        DIARY_READ_CEILING_FLEET
        if diary_read_ceiling == DIARY_READ_CEILING_FLEET and token_subject
        else DIARY_READ_CEILING_SELF
    )
    return SubjectPolicy(token_subject=token_subject, allowed_scopes=scopes, acting_for=acting_for, diary_read_ceiling=ceiling)


def scope_allowed(subject: SubjectPolicy, scope: str, include_family: str | None = None) -> bool:
    if scope == "context":
        if "context" in subject.allowed_scopes:
            return True
        if include_family:
            return include_family in subject.allowed_scopes or f"context:{include_family}" in subject.allowed_scopes
        return any(scope_name.startswith(CONTEXT_SCOPE_PREFIX) for scope_name in subject.allowed_scopes)
    return scope in subject.allowed_scopes


def context_scope_allowed(subject: SubjectPolicy, include_family: str) -> bool:
    return scope_allowed(subject, "context", include_family)


def agent_matches_subject(agent: str | None, token_subject: str | None) -> bool:
    if not agent or not token_subject:
        return True
    return agent == token_subject or token_subject == f"agent:{agent}"


def subject_can_act_for_agent(agent: str | None, subject: SubjectPolicy) -> bool:
    if not agent:
        return True
    return (
        (subject.token_subject is not None and agent_matches_subject(agent, subject.token_subject))
        or (subject.acting_for is not None and agent_matches_subject(agent, subject.acting_for))
    )


def effective_source_subject(subject: SubjectPolicy, agent: str | None = None) -> str | None:
    if agent:
        if subject.token_subject and agent_matches_subject(agent, subject.token_subject):
            return subject.token_subject
        if subject.acting_for and agent_matches_subject(agent, subject.acting_for):
            return subject.acting_for
    return subject.acting_for or subject.token_subject


def with_request_identity(item: dict[str, Any], subject: SubjectPolicy, source_owner: str | None) -> dict[str, Any]:
    if not subject.acting_for:
        return item
    updated = dict(item)
    updated["identity_subject"] = subject.token_subject
    updated["agent_owner"] = source_owner
    return updated


def cross_agent_read_permitted(agent: str | None, subject: SubjectPolicy, scope: str) -> bool:
    """Return True if a cross-agent read is permitted under the subject's ceiling.

    Self-targeted reads always pass. A fleet ceiling (ADR 0001 W2b) opens
    cross-agent diary recall only; context and session families stay self-only
    regardless of ceiling. Narrowing-only: the fleet ceiling cannot widen a
    self-ceiling subject.
    """
    if not agent or subject_can_act_for_agent(agent, subject):
        return True  # self-targeted or acting-for delegation
    return subject.diary_read_ceiling == DIARY_READ_CEILING_FLEET and scope == "diary"
