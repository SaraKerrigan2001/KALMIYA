@echo off
REM ============================================================
REM KALMIYA v3.6 - Launcher Script
REM Inicia todos los servicios principales de KALMIYA
REM ============================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║             KALMIYA v3.6 - INICIANDO                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call .venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  Entorno virtual no encontrado, usando Python global
)

echo.
echo 🚀 Iniciando servicios...
echo.

REM === 1. Dashboard Visual ===
echo 📊 Iniciando Dashboard en Tiempo Real...
start "KALMIYA Dashboard" python 01_systems\KALMIYA_System\ui\dashboard_server.py
timeout /t 2 >nul
echo    ✅ Dashboard: http://localhost:5000
echo.

REM === 2. Skill Manager ===
REM echo ⚙️  Iniciando Skill Manager...
REM start "KALMIYA Skills" python 01_systems\KALMIYA_System\core\skill_manager.py
REM timeout /t 2 >nul
REM echo    ✅ Skills programados
REM echo.

REM === 3. Wake Word (Opcional) ===
echo 🎤 ¿Activar Wake Word Detection? (Hey KALMIYA)
choice /C YN /M "Presiona Y para activar, N para omitir"
if errorlevel 2 goto skip_wake_word
if errorlevel 1 (
    echo    Iniciando Wake Word...
    start "KALMIYA Wake Word" python 01_systems\KALMIYA_System\audio\wake_word.py
    timeout /t 2 >nul
    echo    ✅ Wake Word activo
)
:skip_wake_word
echo.

REM === 4. Sistema Principal (Opcional) ===
echo 🤖 ¿Iniciar Sistema Principal KALMIYA?
choice /C YN /M "Presiona Y para iniciar, N para solo servicios"
if errorlevel 2 goto skip_main
if errorlevel 1 (
    echo    Iniciando KALMIYA Core...
    start "KALMIYA Core" python 01_systems\KALMIYA_System\main.py
    timeout /t 2 >nul
    echo    ✅ Sistema principal activo
)
:skip_main
echo.

REM === Resumen ===
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║             ✅ KALMIYA v3.6 INICIADO                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📊 Dashboard:     http://localhost:5000
echo 🎤 Push-to-Talk:  Ctrl+Alt+M (si está activo)
echo 🎤 Wake Word:     "Hey KALMIYA" (si está activo)
echo.
echo 💡 Tip: Minimiza esta ventana (no la cierres) para mantener servicios activos
echo.
pause
