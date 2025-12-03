@echo off
echo ========================================
echo Configurar Firewall para Red Local
echo ========================================
echo.
echo Este script configurara el Firewall de Windows para permitir
echo el acceso a los puertos 8000 (Backend) y 8501 (Frontend)
echo desde otras computadoras en la red local.
echo.
echo IMPORTANTE: Necesitas ejecutar este script como ADMINISTRADOR
echo.
pause

echo.
echo Configurando regla para FastAPI (Puerto 8000)...
netsh advfirewall firewall add rule name="Sistema Paquetes - Backend" dir=in action=allow protocol=TCP localport=8000
if %errorlevel% equ 0 (
    echo [OK] Regla para Backend configurada correctamente
) else (
    echo [ERROR] No se pudo configurar la regla. Ejecuta como Administrador.
)

echo.
echo Configurando regla para Streamlit (Puerto 8501)...
netsh advfirewall firewall add rule name="Sistema Paquetes - Frontend" dir=in action=allow protocol=TCP localport=8501
if %errorlevel% equ 0 (
    echo [OK] Regla para Frontend configurada correctamente
) else (
    echo [ERROR] No se pudo configurar la regla. Ejecuta como Administrador.
)

echo.
echo ========================================
echo Configuracion completada
echo ========================================
echo.
echo Ahora puedes ejecutar start_servers_lan.bat
echo.
pause
