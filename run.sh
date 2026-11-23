#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
exec "${PYTHON:-python3}" -X utf8 "$root/src/main.py" "$@"
