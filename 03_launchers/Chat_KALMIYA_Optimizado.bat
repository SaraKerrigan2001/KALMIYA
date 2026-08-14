@echo off
REM Chat KALMIYA Optimizado - Launcher
REM Version: 3.6 - Balance perfecto

title Chat KALMIYA Optimizado

echo.
echo ================================================
echo   CHAT KALMIYA OPTIMIZADO v3.6
echo ================================================
echo.
echo Iniciando chat con avatar kawaii...
echo.

cd /d "%~dp0.."
python 03_launchers\chat_optimized.py

if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo iniciar el chat.
    echo Verifica que Python este instalado y las dependencias.
    echo.
    pause
)
