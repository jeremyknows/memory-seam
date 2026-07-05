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
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    completed = subprocess.run(
        [sys.executable, "-m", "memory_seam", *args],
        cwd=ROOT,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


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
