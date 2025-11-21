@echo off
REM Change to the directory where this script is located, then start the frontend
cd /d "%~dp0"
set BROWSER=none
npm start 2>&1
pause
