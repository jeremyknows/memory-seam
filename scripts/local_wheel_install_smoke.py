#!/usr/bin/env python3
"""Build a local wheel and import-smoke it from an isolated temp install.

This script is intentionally local-only: it never publishes artifacts, starts a
service, reads private/live sources, consumes Runtime Registry state, or performs
write/custody/reindex behavior.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import venv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = REPO_ROOT / "scripts" / "package_import_smoke.py"
PACKAGE_DIR = REPO_ROOT / "src" / "memory_seam"


def run(command: list[str], *, cwd: Path = REPO_ROOT, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, env=env, check=True)


def clean_import_environment() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("__PYVENV_LAUNCHER__", None)
    return env


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def create_isolated_venv(venv_dir: Path, *, env: dict[str, str]) -> None:
    try:
        venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    except subprocess.CalledProcessError:
        uv = shutil.which("uv")
        if not uv:
            raise
        run([uv, "venv", "--clear", "--seed", str(venv_dir)], env=env)


def build_minimal_wheel(dist_dir: Path) -> None:
    """Build a pure-Python wheel with stdlib tools when build backends are unavailable."""
    dist_dir.mkdir(parents=True, exist_ok=True)
    name = "memory_seam"
    version = "0.1.0"
    dist_info = f"{name}-{version}.dist-info"
    wheel_path = dist_dir / f"{name}-{version}-py3-none-any.whl"
    records: list[str] = []

    def write_text(zf: zipfile.ZipFile, archive_name: str, text: str) -> None:
        zf.writestr(archive_name, text)
        records.append(archive_name)

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive_name = path.relative_to(REPO_ROOT / "src").as_posix()
                zf.write(path, archive_name)
                records.append(archive_name)

        write_text(
            zf,
            f"{dist_info}/METADATA",
            "\n".join(
                [
                    "Metadata-Version: 2.1",
                    "Name: memory-seam",
                    f"Version: {version}",
                    "License-Expression: Apache-2.0",
                    "Requires-Python: >=3.10",
                    "Description-Content-Type: text/markdown",
                    "",
                    "Portable no-live memory-boundary core for agent memory systems.",
                    "",
                ]
            ),
        )
        write_text(
            zf,
            f"{dist_info}/WHEEL",
            "\n".join(
                [
                    "Wheel-Version: 1.0",
                    "Generator: memory-seam-local-smoke",
                    "Root-Is-Purelib: true",
                    "Tag: py3-none-any",
                    "",
                ]
            ),
        )
        write_text(zf, f"{dist_info}/RECORD", "\n".join([f"{record},," for record in records] + [f"{dist_info}/RECORD,,", ""]))


def build_wheel(dist_dir: Path, *, env: dict[str, str]) -> None:
    """Build a wheel into a temp dist dir without writing checkout caches."""
    try:
        subprocess.run(
            [sys.executable, "-m", "build", "--version"],
            cwd=REPO_ROOT,
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        uv = shutil.which("uv")
        if not uv:
            build_minimal_wheel(dist_dir)
            return
        try:
            run([uv, "build", "--wheel", "--out-dir", str(dist_dir)], env=env)
        except subprocess.CalledProcessError:
            build_minimal_wheel(dist_dir)
            return
        # uv build leaves a stray dist/ (containing only its own .gitignore)
        # in the project root even with --out-dir; remove it so the post-run
        # cleanliness check stays honest. Never touch a dist/ holding real files.
        stray_dist = REPO_ROOT / "dist"
        if stray_dist.is_dir():
            leftovers = [p.name for p in stray_dist.iterdir()]
            if leftovers in ([], [".gitignore"]):
                for p in stray_dist.iterdir():
                    p.unlink()
                stray_dist.rmdir()
    else:
        run([sys.executable, "-m", "build", "--outdir", str(dist_dir)], env=env)


def main() -> int:
    if not SMOKE_SCRIPT.exists():
        raise SystemExit(f"missing package smoke script: {SMOKE_SCRIPT}")

    with tempfile.TemporaryDirectory(prefix="memory-seam-wheel-smoke-") as temp_name:
        temp_dir = Path(temp_name)
        dist_dir = temp_dir / "dist"
        install_dir = temp_dir / "venv"
        env = clean_import_environment()
        env["UV_CACHE_DIR"] = str(temp_dir / "uv-cache")

        build_wheel(dist_dir, env=env)
        wheels = sorted(dist_dir.glob("memory_seam-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected exactly one memory_seam wheel, found {len(wheels)} in {dist_dir}")

        create_isolated_venv(install_dir, env=env)
        python = venv_python(install_dir)
        run(
            [str(python), "-m", "pip", "install", "--no-index", "--find-links", str(dist_dir), str(wheels[0])],
            env=env,
        )
        run([str(python), str(SMOKE_SCRIPT)], env=env)

        if (REPO_ROOT / "dist").exists() or (REPO_ROOT / "build").exists():
            raise SystemExit("local wheel smoke left generated dist/build artifacts in the worktree")
        if any(REPO_ROOT.glob("*.egg-info")):
            raise SystemExit("local wheel smoke left egg-info artifacts in the worktree")

    print("local wheel install smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
