from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from memory_seam.cli import CLI_HELD_SURFACES, build_parser, no_live_response

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run_cli(*args: str) -> dict:
    completed = run_cli_completed(*args, check=True)
    return json.loads(completed.stdout)


def run_cli_completed(*args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    completed = subprocess.run(
        [sys.executable, "-m", "memory_seam", *args],
        cwd=ROOT,
        env=env,
        check=check,
        text=True,
        capture_output=True,
    )
    return completed


@pytest.mark.parametrize("command", [("health",), ("context", "--include", "project"), ("recall", "--query", "runtime")])
def test_module_cli_outputs_json_for_no_live_smoke_commands(command):
    payload = run_cli(*command)
    assert payload["headers"]["content-type"] == "application/json"
    assert payload["status_code"] == 200
    body = payload["body"]
    assert body["cli"]["synthetic_fixtures_only"] is True
    assert body["cli"]["service_started"] is False
    assert body["cli"]["live_source_reads"] is False
    assert body["cli"]["runtime_registry_consumed"] is False
    assert body["cli"]["write_like_routes_available"] is False
    assert body["cli"]["write_custody_or_reindex"] is False
    assert set(body["cli"]["held_surfaces"]) == set(CLI_HELD_SURFACES)


def test_context_cli_uses_committed_synthetic_fixture_only():
    payload = run_cli("context", "--include", "project", "--agent", "agent:memory-seam-cli")
    body = payload["body"]
    assert body["endpoint"] == "context"
    assert body["provider"] == "adapter-safe-content"
    assert body["adapter"] == "synthetic-safe-content"
    assert [item["id"] for item in body["items"]] == ["safe-dogfood-project-boundary"]
    assert body["read_backend_called"] is False
    assert body["raw_fallback_used"] is False


def test_recall_cli_uses_committed_synthetic_fixture_only():
    payload = run_cli("recall", "--query", "runtime", "--scope", "wiki", "--n", "1")
    body = payload["body"]
    assert body["endpoint"] == "recall"
    assert body["scope_effective"] == ["wiki"]
    assert [item["id"] for item in body["items"]] == ["safe-dogfood-runtime-answer"]
    assert body["service_started"] is False
    assert body["runtime_registry_consumed"] is False


def test_local_markdown_recall_human_output_happy_path(tmp_path: Path):
    (tmp_path / "launch.md").write_text(
        "# Launch Notes\n\nThe adapter campaign needs a CLI recall test snippet.",
        encoding="utf-8",
    )

    completed = run_cli_completed("recall", str(tmp_path), "CLI recall", "--n", "1", check=True)

    assert "1. Launch Notes" in completed.stdout
    assert "   launch.md" in completed.stdout
    assert "CLI recall test snippet" in completed.stdout
    assert "Receipt: verdict=useful; reason=safe_context_sufficient;" in completed.stdout
    assert "service_started=false" in completed.stdout
    assert completed.stderr == ""


def test_local_markdown_recall_json_full_envelope(tmp_path: Path):
    (tmp_path / "notes.md").write_text(
        "# Agent Notes\n\nAgents should check receipt_verdict and safe_posture.",
        encoding="utf-8",
    )

    completed = run_cli_completed("recall", str(tmp_path), "receipt_verdict", "--json", check=True)
    payload = json.loads(completed.stdout)
    body = payload["body"]

    assert payload["status_code"] == 200
    assert body["endpoint"] == "recall"
    assert body["provider"] == "local-markdown-cli"
    assert body["adapter"] == "local-markdown-folder"
    assert body["items"][0]["title"] == "Agent Notes"
    assert body["items"][0]["path"] == "notes.md"
    assert body["read_receipt"]["usefulness_shape"]["verdict"] == "useful"
    assert body["runtime"]["decision"] == "allowed"
    assert body["allowed_scopes"] == ["context", "wiki"]


def test_local_markdown_context_json_full_envelope(tmp_path: Path):
    (tmp_path / "context.md").write_text("# Context\n\nShared markdown context.", encoding="utf-8")

    completed = run_cli_completed("context", str(tmp_path), "--json", check=True)
    payload = json.loads(completed.stdout)
    body = payload["body"]

    assert payload["status_code"] == 200
    assert body["endpoint"] == "context"
    assert body["items"][0]["title"] == "Context"
    assert body["items"][0]["path"] == "context.md"
    assert body["read_receipt"]["usefulness_shape"]["verdict"] == "useful"


def test_local_markdown_missing_root_friendly_error(tmp_path: Path):
    missing = tmp_path / "missing"

    completed = run_cli_completed("recall", str(missing), "test")

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "cannot read markdown root" in completed.stderr
    assert "missing root (missing_root)" in completed.stderr
    assert "Traceback" not in completed.stderr


def test_cli_parser_has_no_write_like_or_live_commands():
    parser = build_parser()
    subparser_action = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    choices = set(subparser_action.choices)
    assert sorted(choices) == ["context", "health", "recall"]
    forbidden = {"write", "put", "post", "delete", "serve", "listen", "daemon", "live", "reindex", "custody"}
    assert not forbidden.intersection(choices)
    assert "write_like_routes" in CLI_HELD_SURFACES
    with pytest.raises(SystemExit):
        parser.parse_args(["serve"])


def test_no_live_response_rejects_unsupported_endpoint_defensively():
    with pytest.raises(ValueError, match="unsupported no-live CLI endpoint"):
        no_live_response("write", include="project", mode="startup", agent=None, query="", scope="wiki", n=1)
