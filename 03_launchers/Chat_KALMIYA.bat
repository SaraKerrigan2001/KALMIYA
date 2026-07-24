@echo off
REM Lanzador de Chat KALMIYA para Windows
REM =====================================

echo.
echo ========================================
echo   KALMIYA - Chat
echo ========================================
echo.

cd /d "%~dp0"

REM Crea acceso directo en el escritorio si no existe
if not exist "%USERPROFILE%\Desktop\KALMIYA Chat.lnk" (
    echo Creando acceso directo en el escritorio...
    cscript //nologo "..\01_systems\KALMIYA_System\crear_acceso_chat.vbs"
)

REM Intenta con python3 primero, luego python
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python start_chat.py
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        python3 start_chat.py
    ) else (
        echo Error: Python no esta instalado o no esta en PATH
        pause
        exit /b 1
    )
)

pause
