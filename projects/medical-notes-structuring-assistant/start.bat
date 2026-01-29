@echo off
REM Medical Notes Structuring Assistant - Windows Startup Script
REM This script starts both the backend (FastAPI) and frontend (Streamlit) servers

echo ==========================================
echo   Medical Notes Structuring Assistant
echo ==========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

echo [1/4] Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Ollama is running
) else (
    echo [WARNING] Ollama is not running. Please start Ollama first.
    echo           Run: ollama serve
    echo.
)

echo.
echo [2/4] Starting Backend Server (FastAPI)...
echo         Backend will be available at: http://localhost:8000
echo         API Documentation at: http://localhost:8000/docs

REM Start backend in a new window
start "Medical Notes - Backend" cmd /k "cd /d %SCRIPT_DIR%backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo.
echo [3/4] Starting Frontend Server (Streamlit)...
echo         Frontend will be available at: http://localhost:8501

REM Start frontend in a new window
start "Medical Notes - Frontend" cmd /k "cd /d %SCRIPT_DIR%frontend && streamlit run app.py --server.port 8501"

echo.
echo [4/4] Both servers started successfully!
echo.
echo ==========================================
echo   Access Points:
echo   - Frontend: http://localhost:8501
echo   - Backend API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo ==========================================
echo.
echo Close the opened terminal windows to stop the servers.
echo.

REM Open the frontend in default browser
timeout /t 3 /nobreak >nul
start http://localhost:8501

pause
