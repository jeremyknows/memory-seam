#!/usr/bin/env bash
set -euo pipefail

BRIDGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${BRIDGE_DIR}/.." && pwd)"
VENV_DIR="${BRIDGE_DIR}/.venv"

cd "${BRIDGE_DIR}"

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -e "${REPO_ROOT}"
"${VENV_DIR}/bin/python" -m pip install -e ".[test]"
"${VENV_DIR}/bin/python" -m pytest tests
"${VENV_DIR}/bin/memory-seam-mcp" --root "${BRIDGE_DIR}/tests" --print-config
