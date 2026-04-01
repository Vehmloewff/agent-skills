#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_PYTHON="$VENV_DIR/bin/python"

ensure_venv() {
  if [[ ! -x "$VENV_PYTHON" ]] || ! grep -q "$VENV_DIR" "$VENV_DIR/pyvenv.cfg" 2>/dev/null; then
    echo "Creating virtual environment at $VENV_DIR" >&2
    rm -rf "$VENV_DIR"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
  fi
}

ensure_venv

if [[ ! -f "$VENV_DIR/.deps_installed" ]] || [[ "$REQUIREMENTS_FILE" -nt "$VENV_DIR/.deps_installed" ]]; then
  echo "Installing Python dependencies" >&2
  "$VENV_PYTHON" -m pip install --upgrade pip >&2
  "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_FILE" >&2
  touch "$VENV_DIR/.deps_installed"
fi

exec "$VENV_PYTHON" "$SCRIPT_DIR/ask_user.py" "$@"
