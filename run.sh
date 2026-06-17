#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo ""
  echo "Shutting down..."
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
  wait 2>/dev/null
  echo "Done."
}
trap cleanup EXIT INT TERM

# ── Backend ──
echo "Starting backend..."
cd "$ROOT"
uv run python main.py &
BACKEND_PID=$!

# Wait for backend to be ready
for i in $(seq 1 30); do
  if curl -s http://localhost:8080/api/v1/health >/dev/null 2>&1; then
    echo "Backend ready on http://localhost:8080"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "Backend failed to start"
    exit 1
  fi
  sleep 1
done

# ── Frontend ──
echo "Starting frontend..."
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "  Dashboard:  http://localhost:3000"
echo "  API:        http://localhost:8080"
echo "  Briefing:   http://localhost:8080/briefing"
echo ""
echo "Press Ctrl+C to stop both."
echo ""

# Wait for either to finish
wait
