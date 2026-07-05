from __future__ import annotations

import ast
import sys
import sysconfig
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = REPO_ROOT / "src" / "memory_seam"
BOUNDARY_DOC = REPO_ROOT / "docs" / "adapter-import-boundary.md"
DOWNSTREAM_SMOKE_PLAN = REPO_ROOT / "docs" / "downstream-integration-smoke-plan.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
CONTRACT_TEST_INVENTORY = REPO_ROOT / "docs" / "contract-test-inventory.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"

STDLIB_MODULES = set(sys.stdlib_module_names) | set(sys.builtin_module_names)
STDLIB_MODULES.update({"__future__", "typing_extensions"})
STDLIB_PATH = Path(sysconfig.get_path("stdlib")).resolve()

FORBIDDEN_IMPORT_PREFIXES = (
    "backends",
    "fastmcp",
    "mcp",
    "hermes",
    "runtime_registry",
    "atlas",
    "system_pipes",
    "keyring",
    "oauth",
)

FORBIDDEN_BOUNDARY_TERMS = (
    "Runtime Registry endpoint",
    "launchctl load",
    "crontab -e",
    "twine upload",
    "gh repo edit --visibility public",
)


def _top_level_module(name: str) -> str:
    return name.split(".", 1)[0]


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                continue
            if node.module:
                modules.append(node.module)
    return modules


def test_core_imports_are_stdlib_or_package_local_only():
    unexpected: list[str] = []
    for path in sorted(CORE_DIR.glob("*.py")):
        for module in _imported_modules(path):
            top_level = _top_level_module(module)
            if top_level == "memory_seam" or top_level in STDLIB_MODULES:
                continue
            unexpected.append(f"{path.name}: {module}")

    assert unexpected == []


def test_core_imports_do_not_reference_downstream_adapter_surfaces():
    offenders: list[str] = []
    for path in sorted(CORE_DIR.glob("*.py")):
        for module in _imported_modules(path):
            normalized = module.lower().replace("-", "_")
            if normalized.startswith(FORBIDDEN_IMPORT_PREFIXES):
                offenders.append(f"{path.name}: {module}")

    assert offenders == []


def test_adapter_import_boundary_doc_is_discoverable_and_no_live():
    boundary = BOUNDARY_DOC.read_text(encoding="utf-8")
    smoke_plan = DOWNSTREAM_SMOKE_PLAN.read_text(encoding="utf-8")
    docs_index = DOCS_INDEX.read_text(encoding="utf-8")
    inventory = CONTRACT_TEST_INVENTORY.read_text(encoding="utf-8")
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    normalized = " ".join(boundary.split())

    required_terms = [
        "# Adapter import-boundary compatibility",
        "downstream adapter wrapper -> memory_seam package -> Python standard library",
        "memory_seam package -> downstream adapter wrapper",
        "The `src/memory_seam` package must remain importable",
        "downstream-integration-smoke-plan.md",
        "route_request",
        "provider_handlers",
        "synthetic_safe_content_provider",
        "Do not add submodules, pinned production clones, global client configuration, service activation, or live adapter wiring",
        "<DOWNSTREAM_CHECKOUT>",
    ]
    for term in required_terms:
        assert term in normalized

    for term in FORBIDDEN_BOUNDARY_TERMS:
        assert term not in boundary

    assert "adapter-import-boundary.md" in docs_index
    assert "adapter import-boundary compatibility" in docs_index
    assert "AST-based import-boundary" in inventory
    assert "dependencies = []" in pyproject
    assert "memory-seam package imports ok" in smoke_plan
