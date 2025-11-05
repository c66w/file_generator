#!/usr/bin/env bash
set -euo pipefail

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-6424}
VENV_PATH=${VENV_PATH:-.venv}
LOG_FILE=${LOG_FILE:-uvicorn.log}

if [ -d "${VENV_PATH}" ]; then
  # shellcheck disable=SC1090
  source "${VENV_PATH}/bin/activate"
fi

if pgrep -f "uvicorn main:app --host ${HOST} --port ${PORT}" >/dev/null; then
  echo "Stopping existing Uvicorn process on ${HOST}:${PORT}..."
  pkill -f "uvicorn main:app --host ${HOST} --port ${PORT}"
  sleep 1
fi

echo "Starting Uvicorn on ${HOST}:${PORT}..."
nohup uvicorn main:app --host "${HOST}" --port "${PORT}" >"${LOG_FILE}" 2>&1 &
echo "Service running in background (PID $!). Logs: ${LOG_FILE}"
