@echo off
echo ========================================
echo Starting Recepcion Paquetes System - LAN MODE
echo ========================================

echo.
echo Detectando tu IP local...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP:~1%
echo Tu IP local es: %IP%

echo.
echo [1/2] Starting Backend (FastAPI) en red local...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && ..\\.venv\\Scripts\\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend (Streamlit) en red local...
start "Frontend - Streamlit" cmd /k "cd /d %~dp0frontend && set BACKEND_URL=http://%IP%:8000 && ..\\.venv\\Scripts\\python.exe -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ========================================
echo Servidores iniciados en modo LAN
echo ========================================
echo.
echo COMPARTE ESTA URL CON LA RECEPCIONISTA:
echo.
echo    http://%IP%:8501
echo.
echo ========================================
echo.
echo Instrucciones:
echo 1. La recepcionista debe estar en la misma red WiFi
echo 2. Dale la URL de arriba para que la abra en su navegador
echo 3. Deja esta ventana abierta mientras ella trabaja
echo 4. Para detener: cierra las ventanas del Backend y Frontend
echo.
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
