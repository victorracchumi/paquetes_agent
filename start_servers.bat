@echo off
echo ========================================
echo Starting Recepcion Paquetes System
echo ========================================

echo.
echo [1/2] Starting Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && ..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Frontend (Streamlit)...
start "Frontend - Streamlit" cmd /k "cd /d %~dp0frontend && ..\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501"

echo.
echo ========================================
echo Servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
