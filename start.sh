#!/bin/bash
set -e

echo "=========================================================="
echo "Starting MentorBee Class Link Management System"
echo "=========================================================="

# Activate virtualenv if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run database setup & bootstrap
python bootstrap.py

# Launch Uvicorn ASGI Server
PORT="${PORT:-8000}"
echo "Server listening on http://0.0.0.0:${PORT}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
