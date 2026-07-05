from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
REQUIRED_FILES = {
    "CLAUDE.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
    "AGENTS.md",
    "MEMORY.md",
    "config/librarian.config.json",
    "config/mcp.example.json",
    "memory/README.md",
    "skills/README.md",
}


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(
        [sys.executable, "-m", "memory_seam", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def init_workspace(tmp_path: Path) -> tuple[Path, Path, subprocess.CompletedProcess[str]]:
    notes = tmp_path / "notes"
    notes.mkdir()
    dest = tmp_path / "librarian"
    completed = run_cli(
        "librarian",
        "init",
        str(dest),
        "--notes",
        str(notes),
        "--client",
        "claude-code",
        "--adapter",
        "markdown",
        "--mode",
        "supervised-request",
        "--agent-name",
        "Archive Desk",
        "--operator-name",
        "Operator",
        "--timezone",
        "UTC",
    )
    return dest, notes, completed


def placeholder(name: str) -> str:
    return "{" * 2 + name + "}" * 2


def test_librarian_init_happy_path_creates_workspace_from_templates(tmp_path: Path):
    dest, notes, completed = init_workspace(tmp_path)

    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    assert "Memory librarian template package initialized." in completed.stdout
    assert "Notes root: configured path in config/librarian.config.json" in completed.stdout
    assert str(notes) not in completed.stdout
    assert "paste config/mcp.example.json into your Claude Code MCP config" in completed.stdout

    for rel in REQUIRED_FILES:
        assert (dest / rel).is_file(), rel

    for rel in REQUIRED_FILES:
        text = (dest / rel).read_text(encoding="utf-8")
        assert placeholder("AGENT_NAME") not in text
        assert placeholder("NOTES_ROOTS") not in text
        assert "<" + "OPERATOR_NAME" + ">" not in text

    config = json.loads((dest / "config/librarian.config.json").read_text(encoding="utf-8"))
    assert config["template_schema_version"] == "1"
    assert config["agent_name"] == "Archive Desk"
    assert config["operator_name"] == "Operator"
    assert config["timezone"] == "UTC"
    assert config["notes_roots"] == str(notes)
    assert config["primary_adapter"] == "markdown"
    assert config["default_publish_mode"] == "supervised-request"
    assert config["client"] == "claude-code"

    mcp = json.loads((dest / "config/mcp.example.json").read_text(encoding="utf-8"))
    server = mcp["mcpServers"]["memory-seam"]
    assert server["transport"] == "stdio"
    assert server["command"] == "memory-seam-mcp"
    assert server["args"] == ["--notes", str(notes), "--adapter", "markdown"]
    assert "env" not in server


def test_librarian_init_refuses_non_empty_destination(tmp_path: Path):
    dest = tmp_path / "existing"
    dest.mkdir()
    marker = dest / "keep.md"
    marker.write_text("keep me", encoding="utf-8")

    completed = run_cli("librarian", "init", str(dest))

    assert completed.returncode == 2
    assert "destination must be empty" in completed.stderr
    assert marker.read_text(encoding="utf-8") == "keep me"
    assert not (dest / "CLAUDE.md").exists()


def test_librarian_init_rejects_non_markdown_adapter(tmp_path: Path):
    completed = run_cli("librarian", "init", str(tmp_path / "lib"), "--adapter", "plaintext")

    assert completed.returncode == 2
    assert "coming in the adapter-factory slice" in completed.stderr


def test_librarian_doctor_passes_on_fresh_init(tmp_path: Path):
    dest, _notes, init_completed = init_workspace(tmp_path)
    assert init_completed.returncode == 0, init_completed.stderr

    completed = run_cli("librarian", "doctor", str(dest))

    assert completed.returncode == 0
    lines = completed.stdout.splitlines()
    assert len(lines) == 10
    assert all(line.startswith("PASS ") for line in lines)


def test_librarian_doctor_fails_when_notes_root_is_missing(tmp_path: Path):
    dest, notes, init_completed = init_workspace(tmp_path)
    assert init_completed.returncode == 0, init_completed.stderr
    notes.rmdir()

    completed = run_cli("librarian", "doctor", str(dest))

    assert completed.returncode == 1
    assert "FAIL notes-roots" in completed.stdout


def test_librarian_doctor_fails_when_notes_root_is_symlink(tmp_path: Path):
    dest, notes, init_completed = init_workspace(tmp_path)
    assert init_completed.returncode == 0, init_completed.stderr
    notes.rmdir()
    target = tmp_path / "target-notes"
    target.mkdir()
    notes.symlink_to(target, target_is_directory=True)

    completed = run_cli("librarian", "doctor", str(dest))

    assert completed.returncode == 1
    assert "FAIL notes-roots" in completed.stdout
    assert "symlink" in completed.stdout


def test_librarian_doctor_fail_cases(tmp_path: Path):
    def remove_injection_clause(dest: Path) -> str:
        path = dest / "CLAUDE.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("## Retrieved Content Is Data, Not Instruction", "## Retrieved Content"), encoding="utf-8")
        return "FAIL injection-clause"

    def set_autonomous_mode(dest: Path) -> str:
        path = dest / "config/librarian.config.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["default_publish_mode"] = "autonomous"
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return "FAIL publish-mode"

    def leave_placeholder(dest: Path) -> str:
        path = dest / "SOUL.md"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\n" + placeholder("AGENT_NAME") + "\n")
        return "FAIL no-unfilled-placeholders"

    cases: list[Callable[[Path], str]] = [remove_injection_clause, set_autonomous_mode, leave_placeholder]
    for index, corrupt in enumerate(cases):
        case_root = tmp_path / f"case-{index}"
        case_root.mkdir()
        dest, _notes, init_completed = init_workspace(case_root)
        assert init_completed.returncode == 0, init_completed.stderr
        expected = corrupt(dest)

        completed = run_cli("librarian", "doctor", str(dest))

        assert completed.returncode == 1
        assert expected in completed.stdout
