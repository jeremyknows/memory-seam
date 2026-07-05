from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "public_hygiene_scan.py"
DOC = REPO_ROOT / "docs" / "public-hygiene.md"
GITIGNORE = REPO_ROOT / ".gitignore"

spec = importlib.util.spec_from_file_location("public_hygiene_scan", SCRIPT)
assert spec is not None and spec.loader is not None
public_hygiene_scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(public_hygiene_scan)


def write_text(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def assert_single_hit(tmp_path: Path, rel: str, text: str, kind: str) -> None:
    write_text(tmp_path, rel, text)
    hits = public_hygiene_scan.scan(tmp_path)
    assert len(hits) == 1
    assert f"{rel}:1: {kind}:" in hits[0]


def supervised_proof_json(key: str, value: str) -> str:
    quote = '"'
    return "{" + quote + key + quote + ": " + value + "}"


def test_public_hygiene_scan_rejects_private_path_variants(tmp_path: Path):
    mac_path = "/" + "Users" + "/alice/project"
    linux_path = "/" + "home" + "/alice/project"
    windows_path = "C:" + "\\" + "Users" + "\\" + "alice" + "\\" + "project"
    darwin_temp_path = "/" + "private" + "/var/folders/zz/example"
    cases = [
        ("mac.md", f"operator path {mac_path}"),
        ("linux.md", f"operator path {linux_path}"),
        ("windows.md", f"operator path {windows_path}"),
        ("darwin-cache.md", f"cache path {darwin_temp_path}"),
    ]
    for rel, text in cases:
        case_root = tmp_path / rel.removesuffix(".md")
        assert_single_hit(case_root, rel, text, "host_private_path")


def test_public_hygiene_scan_rejects_platform_ids_and_token_like_strings(tmp_path: Path):
    discord_id = "1502096019" + "087687880"
    slack_channel = "C" + "123456789"
    github_token = "gho_" + "a" * 36
    aws_access_key = "AKIA" + "A" * 16

    cases = [
        ("discord.md", f"raw Discord channel {discord_id}", "platform_identifier"),
        ("slack.md", f"raw Slack channel {slack_channel}", "platform_identifier"),
        ("github.md", f"token {github_token}", "token_like"),
        ("aws.md", f"aws key {aws_access_key}", "token_like"),
    ]
    for rel, text, kind in cases:
        case_root = tmp_path / rel.removesuffix(".md")
        assert_single_hit(case_root, rel, text, kind)


def test_public_hygiene_scan_rejects_private_provenance_references(tmp_path: Path):
    source_floor = "example-source@" + "abcdef1234567890"
    operator_path = "/" + "Users" + "/alice/example-source"
    source_deck = "1502096019" + "087687880"
    atlas_source_path = "docs/" + "atlas-" + "source" + "/extraction.md"
    text = "\n".join(
        [
            f"Atlas source floor {source_floor}",
            f"Operator checkout {operator_path}",
            f"Source deck {source_deck}",
            "See " + "docs/" + "atlas-" + "source" + "/private-note.md",
        ]
    )
    write_text(tmp_path, atlas_source_path, text)
    hits = public_hygiene_scan.scan(tmp_path)
    assert any("atlas_source_floor" in hit for hit in hits)
    assert any("host_private_path" in hit for hit in hits)
    assert any("platform_identifier" in hit for hit in hits)
    assert any("docs_atlas_source_reference" in hit for hit in hits)


def test_public_hygiene_scan_rejects_issue_comment_urls_and_internal_operator_terms(tmp_path: Path):
    issue_comment_url = (
        "https://github.com/"
        + "example/project/issues/"
        + "123#issuecomment-456789"
    )
    cases = [
        ("issue-comment.md", issue_comment_url, "github_issue_comment_url"),
        ("baton.md", "master-" + "baton handoff", "internal_baton_reference"),
        ("operator-term.md", "Example operator" + " poke cron", "internal_operator_term"),
        ("removed-doc.md", "see stewardship" + "-transition", "internal_operator_term"),
    ]
    for rel, text, kind in cases:
        case_root = tmp_path / rel.removesuffix(".md")
        assert_single_hit(case_root, rel, text, kind)


def test_public_hygiene_scan_skips_generated_caches(tmp_path: Path):
    token_like = "sk-" + "c" * 40
    write_text(tmp_path, ".pytest_cache/v/cache/nodeids", f"cached {token_like}")
    private_path = "/" + "Users" + "/alice/project"
    platform_id = "1502096019" + "087687880"
    write_text(tmp_path, ".mypy_cache/3.11/cache.json", f"cached {private_path}")
    write_text(tmp_path, "pkg.egg-info/PKG-INFO", f"cached {platform_id}")
    write_text(tmp_path, "src/safe.py", "print('safe')\n")

    assert public_hygiene_scan.scan(tmp_path) == []


def test_public_hygiene_scan_exceptions_are_documented():
    text = DOC.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    assert "Private provenance has no public-tree quarantine" in normalized
    assert "Internal planning and provenance documents are maintained privately and omitted from this repository" in normalized
    assert "GitHub issue-comment URLs" in text
    assert "internal operator/provenance labels" in text
    assert "Generated cache" in text
    assert "stay out of git entirely" in text


def test_public_hygiene_scan_rejects_unsafe_l6v_supervised_proof_receipt_flags(tmp_path: Path):
    unsafe_artifacts = {
        "allowed.json": supervised_proof_json("allowed", "true"),
        "allowed-count.json": supervised_proof_json("allowed_result_count", "1"),
        "live-adapter.json": supervised_proof_json("live_adapter_invoked", "true"),
        "raw-source-flag.json": supervised_proof_json("raw_source_content_included", "true"),
        "private-correlation-flag.json": supervised_proof_json("private_correlation_refs_included", "true"),
        "approval-raw.json": supervised_proof_json("raw_approval_text_included", "true"),
    }
    expected_kinds = {
        "allowed.json": "l6v_supervised_proof_true_flag",
        "allowed-count.json": "l6v_supervised_proof_nonzero_count",
        "live-adapter.json": "l6v_supervised_proof_true_flag",
        "raw-source-flag.json": "l6v_supervised_proof_true_flag",
        "private-correlation-flag.json": "l6v_supervised_proof_true_flag",
        "approval-raw.json": "l6v_supervised_proof_true_flag",
    }

    for rel, text in unsafe_artifacts.items():
        case_root = tmp_path / rel.removesuffix(".json")
        assert_single_hit(case_root, rel, text, expected_kinds[rel])


def test_public_hygiene_scan_rejects_unsafe_l6v_supervised_proof_refs_and_values(tmp_path: Path):
    quoted = lambda text: '"' + text + '"'
    unsafe_artifacts = {
        "descriptor-ref.json": supervised_proof_json("descriptor_ref", quoted("private_descriptor:workspace-note")),
        "source-card-ref.json": supervised_proof_json("source_card_ref", quoted("source_card:live-workspace-note")),
        "raw-content.json": supervised_proof_json("raw_source_content", quoted("raw private content")),
        "raw-prompt.json": supervised_proof_json("raw_prompt_text", quoted("summarize private source")),
        "source-identifier.json": supervised_proof_json("source_identifier", quoted("private-source-123")),
        "private-correlation.json": supervised_proof_json("private_correlation_ref", quoted("operator-thread-123")),
    }
    expected_kinds = {
        "descriptor-ref.json": "l6v_supervised_proof_unsafe_ref",
        "source-card-ref.json": "l6v_supervised_proof_unsafe_ref",
        "raw-content.json": "l6v_supervised_proof_unsafe_value",
        "raw-prompt.json": "l6v_supervised_proof_unsafe_value",
        "source-identifier.json": "l6v_supervised_proof_unsafe_value",
        "private-correlation.json": "l6v_supervised_proof_unsafe_value",
    }

    for rel, text in unsafe_artifacts.items():
        case_root = tmp_path / rel.removesuffix(".json")
        assert_single_hit(case_root, rel, text, expected_kinds[rel])


def test_public_hygiene_scan_allows_report_safe_l6v_supervised_proof_artifact(tmp_path: Path):
    artifact = "\n".join(
        [
            '{',
            '  "descriptor_ref": "synthetic_descriptor:l6v-report-safe-project-doc-v1",',
            '  "source_card_ref": "synthetic_source_card:l6v-report-safe-project-doc-v1",',
            '  "allowed": false,',
            '  "allowed_result_count": 0,',
            '  "live_adapter_invoked": false,',
            '  "callbacks_invoked": false,',
            '  "raw_source_content_included": false,',
            '  "private_correlation_refs_included": false',
            '}',
        ]
    )
    write_text(tmp_path, "proof.json", artifact)

    assert public_hygiene_scan.scan(tmp_path) == []


def test_public_hygiene_scan_scans_template_suffixes(tmp_path: Path):
    private_path = "/" + "Users" + "/alice/project"
    write_text(tmp_path, "src/pkg/agent_packages/example/templates/unsafe.template", private_path)

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("host_private_path" in hit for hit in hits)


def test_public_hygiene_scan_covers_integrations_tree(tmp_path: Path):
    private_path = "/" + "Users" + "/alice/project"
    write_text(tmp_path, "integrations/claude-plugin/README.md", private_path)

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("integrations/claude-plugin/README.md:1: host_private_path" in hit for hit in hits)


def test_public_hygiene_scan_covers_bridge_tree(tmp_path: Path):
    private_path = "/" + "Users" + "/alice/project"
    write_text(tmp_path, "bridge/README.md", private_path)

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("bridge/README.md:1: host_private_path" in hit for hit in hits)


def test_public_hygiene_scan_rejects_unapproved_template_placeholders(tmp_path: Path):
    bad_placeholder = "{" * 2 + "BAD_NAME" + "}" * 2
    write_text(tmp_path, "starter.template", f"operator {bad_placeholder}")

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("unapproved_template_placeholder" in hit for hit in hits)


def test_public_hygiene_scan_rejects_unfilled_placeholders_outside_templates(tmp_path: Path):
    bad_placeholder = "{" * 2 + "AGENT_NAME" + "}" * 2
    write_text(tmp_path, "docs/example.md", f"operator {bad_placeholder}")

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("unfilled_placeholder" in hit for hit in hits)


def test_public_hygiene_scan_rejects_real_operator_defaults_in_templates(tmp_path: Path):
    real_name = "Jer" + "emy"
    write_text(tmp_path, "starter.template", f"operator {real_name}")

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("real_operator_default" in hit for hit in hits)


def test_public_hygiene_scan_rejects_authority_phrases_in_templates(tmp_path: Path):
    write_text(tmp_path, "starter.template", "The starter may autonomous publish updates.")

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("authority_phrase" in hit for hit in hits)


def test_public_hygiene_scan_rejects_non_stdio_mcp_examples(tmp_path: Path):
    text = '{"mcpServers": {"memory": {"transport": "http"}}}'
    write_text(tmp_path, "src/pkg/agent_packages/example/templates/config/mcp.example.json.template", text)

    hits = public_hygiene_scan.scan(tmp_path)

    assert any("mcp_non_stdio_config" in hit for hit in hits)


def test_public_hygiene_scan_rejects_packaged_skill_missing_posture(tmp_path: Path):
    rel = "src/pkg/agent_packages/example/skills/seam-ops/SKILL.md"
    write_text(tmp_path, rel, "---\nname: seam-ops\ndescription: bad\n---\n# seam-ops\n")

    hits = public_hygiene_scan.scan(tmp_path)

    assert any(f"{rel}:1: missing_required_librarian_posture" in hit for hit in hits)
    assert any("No-authority-expansion rule:" in hit for hit in hits)


def test_l6v_supervised_proof_hygiene_ratchet_is_documented():
    text = DOC.read_text(encoding="utf-8")
    assert "L6V supervised source-card proof ratchet" in text
    assert "`allowed=true`" in text
    assert "descriptor/source-card refs" in text
    assert "raw prompt" in text


def test_generated_cache_paths_are_ignored_by_git():
    ignore_text = GITIGNORE.read_text(encoding="utf-8")
    required_rules = {
        "__pycache__/",
        "*.py[cod]",
        ".pytest_cache/",
        ".ruff_cache/",
        ".mypy_cache/",
        ".tox/",
        ".venv/",
        ".coverage",
        "htmlcov/",
        "dist/",
        "build/",
        "site-packages/",
        "*.egg-info/",
        "*.dist-info/",
    }

    assert required_rules <= set(ignore_text.splitlines())


def test_no_generated_cache_artifacts_are_tracked():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    tracked = result.stdout.splitlines()
    generated_parts = {
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".tox",
        ".venv",
        "htmlcov",
        "dist",
        "build",
        "site-packages",
    }
    generated_suffixes = (".pyc", ".pyo", ".pyd", ".egg-info", ".dist-info")

    offenders = [
        path
        for path in tracked
        if any(part in generated_parts for part in Path(path).parts)
        or path.endswith(generated_suffixes)
        or Path(path).name == ".coverage"
    ]

    assert offenders == []
