@echo off
REM Script para abrir el vault en Obsidian
REM Nota: Requiere que Obsidian esté instalado y en PATH

echo Abriendo Vault en Obsidian...
cd /d "%~dp0"

REM Intenta ejecutar Obsidian con la carpeta actual como vault
start obsidian "$(PWD)"

REM Si no funciona, abre el explorador de vaults
REM uncomment la siguiente línea:
REM start obsidian

echo.
echo Si Obsidian no se abre, hazlo manualmente:
echo 1. Abre Obsidian
echo 2. Click "Abrir carpeta como Vault"
echo 3. Selecciona: %cd%
pause
