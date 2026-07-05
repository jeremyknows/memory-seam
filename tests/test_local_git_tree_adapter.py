from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import memory_seam.local_adapters.git_tree as git_tree_module
from memory_seam import (
    ADAPTER_PROTOCOL_VERSION,
    AdapterMemorySeamProvider,
    LocalReadOnlyRuntime,
    ReadOnlyRuntimeConfig,
    RuntimeRequest,
    StaticIdentityVerifier,
)
from memory_seam.local_adapters.git_tree import (
    DEFAULT_GIT_TREE_EXTENSIONS,
    GIT_TREE_ADAPTER_PROTOCOL_VERSION,
    LocalGitTreeAdapter,
    MAX_FILE_BYTES,
    MAX_SCAN_FILES,
    PRISM_POSTURE_RULINGS,
)

HELPER_PATH = Path(__file__).resolve().parents[1] / "tests" / "adapter_certification.py"
HELPER_SPEC = importlib.util.spec_from_file_location("adapter_certification_for_local_git_tree", HELPER_PATH)
assert HELPER_SPEC and HELPER_SPEC.loader
adapter_certification = importlib.util.module_from_spec(HELPER_SPEC)
sys.modules[HELPER_SPEC.name] = adapter_certification
HELPER_SPEC.loader.exec_module(adapter_certification)

AdapterCertificationConfig = adapter_certification.AdapterCertificationConfig
assert_source_adapter_certified = adapter_certification.assert_source_adapter_certified


def test_local_git_tree_adapter_passes_lane_10_certification(tmp_path: Path):
    repo = _git_repo(tmp_path)
    (repo / "authority.md").write_text(
        "# Authority\n\nReceipt-first local note recall proves authority.",
        encoding="utf-8",
    )
    outside = tmp_path / "outside-certification-note.md"
    outside.write_text("# Outside\n\nmemory seam certification zero match", encoding="utf-8")
    (repo / "outside.md").symlink_to(outside)
    _git(repo, "add", "authority.md", "outside.md")

    assert_source_adapter_certified(
        LocalGitTreeAdapter(repo),
        repo,
        config=AdapterCertificationConfig(
            recall_query="authority receipt",
            allowed_retrieval_backends=frozenset({"git_current_tree_scan"}),
        ),
    )


def test_adapter_declares_protocol_version_and_default_allowlist(tmp_path: Path):
    adapter = LocalGitTreeAdapter(tmp_path)

    assert adapter.adapter_protocol_version == ADAPTER_PROTOCOL_VERSION
    assert GIT_TREE_ADAPTER_PROTOCOL_VERSION == ADAPTER_PROTOCOL_VERSION
    assert DEFAULT_GIT_TREE_EXTENSIONS == (
        ".md",
        ".txt",
        ".rst",
        ".py",
        ".js",
        ".ts",
        ".toml",
        ".yaml",
        ".json",
        ".cfg",
        ".ini",
    )


def test_recall_reads_tracked_current_tree_and_excludes_untracked(tmp_path: Path):
    repo = _git_repo(tmp_path)
    (repo / "tracked.md").write_text("# Tracked\n\nneedle authority", encoding="utf-8")
    (repo / "untracked.md").write_text("# Untracked\n\nneedle authority", encoding="utf-8")
    _git(repo, "add", "tracked.md")

    adapter = LocalGitTreeAdapter(repo)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["tracked.md"]
    assert items[0]["posture_rulings"]["history"] == "REJECTED"
    assert adapter.last_scan_summary["posture_rulings"] == PRISM_POSTURE_RULINGS


def test_default_and_configurable_allowlists(tmp_path: Path):
    repo = _git_repo(tmp_path)
    (repo / "alpha.py").write_text("needle = True", encoding="utf-8")
    (repo / "beta.yaml").write_text("value: needle", encoding="utf-8")
    (repo / "ignored.html").write_text("needle", encoding="utf-8")
    (repo / "custom.memo").write_text("needle", encoding="utf-8")
    _git(repo, "add", "alpha.py", "beta.yaml", "ignored.html", "custom.memo")

    default_items = LocalGitTreeAdapter(repo).recall_items("needle", scope="wiki", token_subject=None, n=10)
    custom_items = LocalGitTreeAdapter(repo, extension_allowlist=("memo",)).recall_items(
        "needle",
        scope="wiki",
        token_subject=None,
        n=10,
    )

    assert [item["path"] for item in default_items] == ["alpha.py", "beta.yaml"]
    assert [item["path"] for item in custom_items] == ["custom.memo"]


def test_binary_and_large_tracked_files_are_skipped(tmp_path: Path):
    repo = _git_repo(tmp_path)
    (repo / "binary.txt").write_bytes(b"needle\x00not text")
    (repo / "huge.txt").write_text("needle\n" + ("x" * (MAX_FILE_BYTES + 1)), encoding="utf-8")
    (repo / "visible.txt").write_text("visible needle", encoding="utf-8")
    _git(repo, "add", "binary.txt", "huge.txt", "visible.txt")

    adapter = LocalGitTreeAdapter(repo)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.txt"]
    assert adapter.last_scan_summary["files_scanned"] == 3
    assert adapter.last_scan_summary["files_skipped"] == 2
    assert adapter.last_scan_summary["binary_files_skipped"] == 1


def test_non_repo_root_returns_friendly_reason(tmp_path: Path):
    adapter = LocalGitTreeAdapter(tmp_path)

    assert adapter.context_items(include=["memory"], token_subject=None) == []
    assert adapter.last_empty_reason == "not_a_git_repository"
    assert adapter.last_scan_summary["reason"] == "not_a_git_repository"


def test_missing_git_returns_friendly_reason(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("PATH", "")
    adapter = LocalGitTreeAdapter(tmp_path)

    assert adapter.context_items(include=["memory"], token_subject=None) == []
    assert adapter.last_empty_reason == "git_unavailable"


def test_tracked_symlink_is_not_followed(tmp_path: Path):
    repo = _git_repo(tmp_path / "repo")
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n\nneedle", encoding="utf-8")
    (repo / "outside.md").symlink_to(outside)
    (repo / "visible.md").write_text("# Visible\n\nneedle", encoding="utf-8")
    _git(repo, "add", "outside.md", "visible.md")

    items = LocalGitTreeAdapter(repo).recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.md"]


def test_toctou_swap_to_symlink_is_not_followed(monkeypatch, tmp_path: Path):
    repo = _git_repo(tmp_path / "repo")
    victim = repo / "victim.md"
    victim.write_text("# Victim\n\nneedle", encoding="utf-8")
    outside = tmp_path / "git-race-outside.md"
    outside.write_text("# Outside\n\nneedle", encoding="utf-8")
    _git(repo, "add", "victim.md")
    original = git_tree_module._safe_git_relative_path
    swapped = {"done": False}

    def swap_before_open(value: str) -> str | None:
        rel = original(value)
        if value == "victim.md" and not swapped["done"]:
            swapped["done"] = True
            victim.unlink()
            victim.symlink_to(outside)
        return rel

    monkeypatch.setattr(git_tree_module, "_safe_git_relative_path", swap_before_open)

    assert LocalGitTreeAdapter(repo).recall_items("needle", scope="wiki", token_subject=None, n=10) == []


def test_runtime_envelope_carries_structured_non_repo_reason(tmp_path: Path):
    runtime = LocalReadOnlyRuntime(
        config=ReadOnlyRuntimeConfig(enabled=True, provider_name="local-git-tree-test"),
        provider=AdapterMemorySeamProvider(LocalGitTreeAdapter(tmp_path), provider_name="local-git-tree-test"),
        identity_verifier=StaticIdentityVerifier(
            subject="agent:test",
            allowed_scopes=frozenset({"context", "wiki"}),
        ),
    )

    response = runtime.handle(RuntimeRequest("GET", "/context?include=memory"))
    body = response["body"]

    assert response["status_code"] == 200
    assert body["items"] == []
    assert body["reason"] == "not_a_git_repository"
    assert body["adapter_scan_summary"]["reason"] == "not_a_git_repository"


def test_scan_cap_adds_truncation_item(tmp_path: Path):
    repo = _git_repo(tmp_path)
    for index in range(MAX_SCAN_FILES + 1):
        (repo / f"{index:04d}.txt").write_text("needle", encoding="utf-8")
    _git(repo, "add", ".")

    adapter = LocalGitTreeAdapter(repo)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=1)

    assert len(items) == 1
    assert items[0]["title"] == "0000"
    assert adapter.last_scan_summary["files_scanned"] == MAX_SCAN_FILES
    assert adapter.last_scan_summary["truncated"] is True
    assert adapter.last_scan_summary["scan_notice"]["title"] == "Local Git current-tree scan truncated"
    assert "Scan stopped after" in adapter.last_scan_summary["scan_notice"]["message"]


def test_submodule_gitlink_is_skipped_when_git_allows_file_protocol(tmp_path: Path):
    parent = _git_repo(tmp_path / "parent")
    child = _git_repo(tmp_path / "child")
    (child / "nested.md").write_text("# Nested\n\nneedle", encoding="utf-8")
    _git(child, "add", "nested.md")
    _git(child, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "child")
    try:
        _git(parent, "-c", "protocol.file.allow=always", "submodule", "add", str(child), "vendor/child.md")
    except AssertionError:
        return
    (parent / "visible.md").write_text("# Visible\n\nneedle", encoding="utf-8")
    _git(parent, "add", "visible.md")

    adapter = LocalGitTreeAdapter(parent)
    items = adapter.recall_items("needle", scope="wiki", token_subject=None, n=10)

    assert [item["path"] for item in items] == ["visible.md"]
    assert adapter.last_scan_summary["gitlinks_skipped"] == 1


def _git_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init")
    return path


def _git(cwd: Path, *args: str) -> None:
    git = shutil.which("git")
    assert git is not None, "git unavailable in test environment"
    result = subprocess.run(
        [git, *args],
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
