@echo off
echo ========================================
echo Subir Proyecto a GitHub
echo ========================================
echo.
echo Este script te ayudara a subir tu proyecto a GitHub
echo de forma segura (sin credenciales).
echo.

REM Verificar si Git esta instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git no esta instalado.
    echo.
    echo Descarga Git desde: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git esta instalado
echo.

REM Verificar si .gitignore existe
if not exist ".gitignore" (
    echo [ADVERTENCIA] No existe .gitignore
    echo Creando .gitignore para proteger tus credenciales...
    echo.

    echo .env > .gitignore
    echo backend/.env >> .gitignore
    echo .venv/ >> .gitignore
    echo __pycache__/ >> .gitignore
    echo *.pyc >> .gitignore
    echo backend/paquetes.db >> .gitignore
    echo.
    echo [OK] .gitignore creado
    echo.
)

REM Verificar si ya existe repositorio Git
if not exist ".git" (
    echo Inicializando repositorio Git...
    git init
    echo [OK] Repositorio inicializado
    echo.
)

echo ========================================
echo Preparando archivos para subir...
echo ========================================
echo.

REM Agregar archivos
git add .
echo [OK] Archivos agregados
echo.

REM Commit
git commit -m "Sistema de recepcion de paquetes - Deploy to cloud"
echo [OK] Commit creado
echo.

echo ========================================
echo Instrucciones para Subir a GitHub
echo ========================================
echo.
echo 1. Ve a https://github.com
echo 2. Haz clic en "New repository"
echo 3. Nombre: paquetes_agent
echo 4. Descripcion: Sistema de recepcion de paquetes
echo 5. Privado: SI (recomendado para codigo interno)
echo 6. NO inicialices con README, .gitignore o licencia
echo 7. Haz clic en "Create repository"
echo.
echo 8. Copia la URL del repositorio que te da GitHub
echo    Ejemplo: https://github.com/tu-usuario/paquetes_agent.git
echo.

set /p REPO_URL="Pega aqui la URL de tu repositorio de GitHub: "

if "%REPO_URL%"=="" (
    echo.
    echo [ERROR] No ingresaste la URL
    echo.
    pause
    exit /b 1
)

echo.
echo Conectando con GitHub...
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Subiendo archivos a GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo [OK] Proyecto subido exitosamente a GitHub
    echo ========================================
    echo.
    echo URL de tu repositorio: %REPO_URL%
    echo.
    echo Siguiente paso:
    echo - Lee DESPLIEGUE_NUBE.md para desplegar en Railway y Streamlit Cloud
    echo.
) else (
    echo.
    echo [ERROR] Hubo un problema al subir a GitHub
    echo.
    echo Posibles causas:
    echo - Necesitas autenticarte con GitHub
    echo - La URL del repositorio es incorrecta
    echo - No tienes permisos
    echo.
    echo Intenta manualmente:
    echo git remote add origin TU-URL
    echo git push -u origin main
    echo.
)

pause
