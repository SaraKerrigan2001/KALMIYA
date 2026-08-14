@echo off
chcp 65001 >nul
REM Test simple del Chat KALMIYA

echo.
echo ============================================================
echo   TEST CHAT KALMIYA - QUICK TEST
echo ============================================================
echo.

cd /d "%~dp0"

echo Probando chat.py...
python chat.py

if errorlevel 1 (
    echo.
    echo ERROR: El chat no se pudo iniciar
    pause
    exit /b 1
)

echo.
echo Chat cerrado correctamente
pause
