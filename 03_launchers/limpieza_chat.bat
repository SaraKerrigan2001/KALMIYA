@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║    🧹 LIMPIEZA AUTOMÁTICA DE CHAT KALMIYA             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
cd /d %~dp0..
python 05_tests\limpieza_automatica.py
echo.
pause
