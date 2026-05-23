#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${PALAMEDES_UI_PORT:-8765}"
cd "$ROOT/ui"
echo "Palamedes UI → http://127.0.0.1:${PORT}/" >&2
exec python3 -m http.server "$PORT" --bind 127.0.0.1
