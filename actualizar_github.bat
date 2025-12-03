@echo off
echo ========================================
echo Actualizar Cambios en GitHub
echo ========================================
echo.

git add .
git commit -m "Fix: Configuracion para Railway deployment"
git push

if %errorlevel% equ 0 (
    echo.
    echo [OK] Cambios subidos exitosamente a GitHub
    echo.
    echo Railway detectara los cambios y re-desplegara automaticamente
    echo Espera 2-3 minutos y revisa el dashboard de Railway
    echo.
) else (
    echo.
    echo [ERROR] No se pudo subir a GitHub
    echo.
)

pause
