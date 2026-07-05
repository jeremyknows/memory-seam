# Packaging metadata and smoke boundary

Memory Seam v0.1.0 is packaged as a standalone `src/`-layout Python project for
public Apache-2.0 source use and downstream adapter development.

See `docs/package-boundary.md` for the package-wide boundary checklist covering
no-live examples, downstream adapter ownership, and held runtime/write surfaces.

## Current metadata posture

- Package name: `memory-seam`
- Current version: `0.1.0`
- Python support floor: `>=3.10`
- Runtime dependencies: none
- License: Apache-2.0
- Publication status: public source release. Registry publication, if any, is a
  separate maintainer action and is not automated by this repository.

The wheel includes only the `memory_seam` package. The source distribution also
includes tests, examples, scripts, docs, and CI metadata so downstream adapter
branches can reproduce package/build checks from a checkout archive.

## Local build smoke

```bash
python -m pip install -e '.[dev]'
python scripts/local_wheel_install_smoke.py
```

The smoke builds wheel/sdist artifacts under a temporary directory, creates an
isolated virtual environment, installs the local wheel without consulting a
package index, and runs `scripts/package_import_smoke.py` against the installed
package. It leaves no `dist/`, `build/`, or `*.egg-info` artifacts in the
worktree.

The smoke imports the installed wheel and exercises the no-live/null-provider
path only. It does not publish artifacts, read downstream adapter data, start
services, consume the Runtime Registry, or perform write/custody/reindex
behavior.
