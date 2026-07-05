from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import memory_seam.cli as cli_module
from memory_seam import _style
from memory_seam.cli import CLI_HELD_SURFACES, build_parser, no_live_response
from memory_seam.cli import _json_safe, main

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
WORDMARK_FIRST_LINE = "███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗"
RECEIPT_GATE_LINE = "+───────────────────[ receipt gate ]───────────────────+"


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

    assert "memory-seam v0.1.0 · adapter=markdown" in completed.stdout
    assert "1 files scanned" in completed.stdout
    assert "1. Launch Notes" in completed.stdout
    assert "   launch.md" in completed.stdout
    assert "CLI recall test snippet" in completed.stdout
    assert "Receipt: verdict=useful; reason=safe_context_sufficient;" in completed.stdout
    assert "service_started=false" in completed.stdout
    assert "\r" not in completed.stdout
    assert WORDMARK_FIRST_LINE not in completed.stdout
    assert completed.stderr == ""


def test_local_markdown_recall_json_full_envelope(tmp_path: Path):
    (tmp_path / "notes.md").write_text(
        "# Agent Notes\n\nAgents should check receipt_verdict and safe_posture.",
        encoding="utf-8",
    )

    completed = run_cli_completed("recall", str(tmp_path), "receipt_verdict", "--json", check=True)
    payload = json.loads(completed.stdout)
    body = payload["body"]

    assert "\r" not in completed.stdout
    assert WORDMARK_FIRST_LINE not in completed.stdout
    assert payload["status_code"] == 200
    assert body["endpoint"] == "recall"
    assert body["provider"] == "local-markdown-cli"
    assert body["adapter"] == "local-markdown-folder"
    assert body["items"][0]["title"] == "Agent Notes"
    assert body["items"][0]["path"] == "notes.md"
    assert body["read_receipt"]["usefulness_shape"]["verdict"] == "useful"
    assert body["runtime"]["decision"] == "allowed"
    assert body["allowed_scopes"] == ["context", "wiki"]


def test_style_helper_enables_only_for_supported_tty(monkeypatch):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    assert _style.bold("Title") == "\033[1mTitle\033[0m"
    assert _style.dim("path.md") == "\033[2mpath.md\033[0m"
    assert _style.green("ok") == "\033[32mok\033[0m"
    assert _style.yellow("warn") == "\033[33mwarn\033[0m"
    assert _style.red("err") == "\033[31merr\033[0m"
    assert _style.cyan("root") == "\033[36mroot\033[0m"


@pytest.mark.parametrize(
    ("isatty", "env", "term"),
    [
        (False, {}, "xterm-256color"),
        (True, {"NO_COLOR": "1"}, "xterm-256color"),
        (True, {}, "dumb"),
    ],
)
def test_style_helper_disables_for_pipe_no_color_and_dumb_term(monkeypatch, isatty, env, term):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: isatty)
    monkeypatch.delenv("NO_COLOR", raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("TERM", term)

    assert _style.cyan("plain") == "plain"


def test_local_markdown_recall_uses_style_when_stdout_is_tty(monkeypatch, tmp_path: Path, capsys):
    (tmp_path / "launch.md").write_text("# Launch Notes\n\nCLI recall taste.", encoding="utf-8")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    assert main(["recall", str(tmp_path), "taste", "--n", "1"]) == 0

    captured = capsys.readouterr()
    assert f"\rmemory-seam: scanning {tmp_path} … 0 files\r" in captured.out
    assert "\033[36mmemory-seam v0.1.0 · adapter=markdown" in captured.out
    assert "1. \033[1mLaunch Notes\033[0m" in captured.out
    assert "\033[2m\033[36mlaunch.md\033[0m\033[0m" in captured.out
    assert "\033[32m✓ Receipt: verdict=useful; reason=safe_context_sufficient;\033[0m" in captured.out
    assert captured.err == ""


def test_local_markdown_recall_no_color_disables_style(monkeypatch, tmp_path: Path, capsys):
    (tmp_path / "launch.md").write_text("# Launch Notes\n\nCLI recall taste.", encoding="utf-8")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("TERM", "xterm-256color")

    assert main(["recall", str(tmp_path), "taste", "--n", "1"]) == 0

    captured = capsys.readouterr()
    assert "\r" not in captured.out
    assert "\033[" not in captured.out
    assert "✓ Receipt: verdict=useful; reason=safe_context_sufficient;" in captured.out


def test_local_markdown_json_output_is_byte_identical_to_envelope_dump(monkeypatch, tmp_path: Path, capsys):
    (tmp_path / "notes.md").write_text(
        "# Agent Notes\n\nAgents should check receipt_verdict and safe_posture.",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    response = {
        "status_code": 200,
        "body": {
            "endpoint": "recall",
            "items": [{"title": "Agent Notes", "path": "notes.md"}],
            "allowed_scopes": frozenset({"wiki", "context"}),
        },
    }
    monkeypatch.setattr(cli_module, "local_markdown_response", lambda *args, **kwargs: response)

    expected = json.dumps(_json_safe(response), indent=2, sort_keys=True)
    assert main(["recall", str(tmp_path), "receipt_verdict", "--json"]) == 0

    captured = capsys.readouterr()
    assert captured.out == expected + "\n"
    assert "\r" not in captured.out
    assert WORDMARK_FIRST_LINE not in captured.out
    assert "\033[" not in captured.out
    assert captured.err == ""


def test_banner_on_no_args_exits_zero():
    completed = run_cli_completed()

    assert completed.returncode == 0
    lines = completed.stdout.splitlines()
    assert lines[0] == WORDMARK_FIRST_LINE
    assert RECEIPT_GATE_LINE in lines
    receipt_gate_index = lines.index(RECEIPT_GATE_LINE)
    assert lines[receipt_gate_index][0] == "+"
    assert lines[receipt_gate_index][-1] == "+"
    assert len(lines[receipt_gate_index]) == len(RECEIPT_GATE_LINE)
    assert "v0.1.0 · receipt-first memory boundary for AI agents" in completed.stdout
    assert 'usage: memory-seam recall <root> "query"' in completed.stdout
    assert completed.stderr == ""

    version_completed = run_cli_completed("--version")
    assert version_completed.returncode == 0
    assert version_completed.stdout == completed.stdout
    assert version_completed.stderr == ""


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
