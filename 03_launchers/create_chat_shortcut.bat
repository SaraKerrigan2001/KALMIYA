@echo off
REM Crea un acceso directo de Chat KALMIYA en el escritorio usando VBS.

cd /d "%~dp0"

if exist "%USERPROFILE%\Desktop\KALMIYA Chat.lnk" (
    echo El acceso directo ya existe en el escritorio.
) else (
    echo Creando acceso directo en el escritorio...
    cscript //nologo "..\01_systems\KALMIYA_System\crear_acceso_chat.vbs"
)

echo Listo.
pause
