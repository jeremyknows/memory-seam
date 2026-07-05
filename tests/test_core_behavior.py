from __future__ import annotations

from pathlib import Path

from memory_seam.descriptors import ContextSourceDescriptor, describe_context_source_descriptors
from memory_seam.policy import (
    policy,
    context_scope_allowed,
    scope_allowed,
    effective_source_subject,
    subject_can_act_for_agent,
)
from memory_seam.receipts import read_receipt_enabled, replay_read_receipt
from memory_seam.router import route_request
from memory_seam.testing import synthetic_project_doc_fixture_allowlist


def test_descriptor_report_is_metadata_only(tmp_path):
    root = tmp_path / "profile"
    target = root / "docs" / "project.md"
    target.parent.mkdir(parents=True)
    target.write_text("private fixture text", encoding="utf-8")
    desc = ContextSourceDescriptor(
        subject="agent:example",
        include_family="project",
        root_ref="profile",
        relative_path="docs/project.md",
        source_tier="fixture",
        private_class="internal",
        canonicality="canonical",
        retrieval_backend="filesystem",
        max_bytes=100,
    )
    report = describe_context_source_descriptors(roots={"profile": root}, descriptors=[desc])
    assert report["descriptor_count"] == 1
    assert report["descriptors"][0]["root_ref"] == "profile"
    rendered = repr(report)
    assert str(root) not in rendered
    assert "private fixture text" not in rendered


def test_policy_denies_wrong_actor_narrowing():
    subject = policy("agent:example", ["context:project"], acting_for="agent:example-target")
    assert context_scope_allowed(subject, "project") is True
    assert scope_allowed(subject, "context", "project") is True
    assert effective_source_subject(subject, "example-target") == "agent:example-target"
    assert subject_can_act_for_agent("alice", subject) is False


def test_router_denies_write_like_routes_before_handler():
    calls = []

    def handler(**kwargs):
        calls.append(kwargs)
        return {"ok": True}

    response = route_request(
        "POST",
        "/context?include=project&agent=sax",
        health_handler=lambda: {"ok": True},
        context_handler=handler,
        recall_handler=lambda query, **kwargs: {"query": query},
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context"],
    )
    assert response["status_code"] == 405
    assert calls == []


def test_router_context_route_parses_read_receipt_flag():
    calls = []

    def context_handler(**kwargs):
        calls.append(kwargs)
        return {"ok": True, "kwargs": kwargs}

    response = route_request(
        "GET",
        "/context?include=project,soul&mode=startup&agent=sax&timeout_ms=250&read_receipt=metadata_only",
        health_handler=lambda: {"ok": True},
        context_handler=context_handler,
        recall_handler=lambda query, **kwargs: {"query": query},
        read_receipt_enabled=read_receipt_enabled,
        token_subject="agent:example",
        allowed_scopes=["context"],
    )
    assert response["status_code"] == 200
    assert calls[-1]["include"] == ["project", "soul"]
    assert calls[-1]["include_read_receipt"] is True


def test_testing_fixture_and_receipt_helpers_are_available():
    allowlist = synthetic_project_doc_fixture_allowlist("sax_project_doc_granted")
    assert allowlist.get("agent:example", "project") is not None
    assert read_receipt_enabled("metadata_only") is True
    receipt = replay_read_receipt()
    assert receipt["endpoint"] == "receipt_replay"
    assert receipt["no_go"]["live_reads"] is False
