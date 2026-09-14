#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/.venv/bin/activate"

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR"
export PYTHONDONTWRITEBYTECODE=1
exec "$ROOT_DIR/.venv/bin/python" -m flask --app FlaskApp.app run
