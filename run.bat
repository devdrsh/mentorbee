@echo off
echo ==========================================================
echo Starting MentorBee Class Link Management System
echo ==========================================================
python bootstrap.py
echo Starting Uvicorn Web Server on http://localhost:8000 ...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
