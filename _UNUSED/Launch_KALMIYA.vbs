Set WshShell = CreateObject("WScript.Shell")
' Obtener la ruta del directorio actual de forma correcta
Set fso = CreateObject("Scripting.FileSystemObject")
strPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambiar al directorio de KALMIYA
WshShell.CurrentDirectory = strPath

' Comando para iniciar KALMIYA en segundo plano usando el Python del entorno virtual
WshShell.Run "..\Scripts\python.exe kalmiya_core.py", 0, False

' Esperar 2 segundos para que el servidor arranque
WScript.Sleep 2000

' Abrir el Dashboard específicamente en Microsoft Edge
' Usamos "msedge" para forzar el navegador de Microsoft
WshShell.Run "msedge http://localhost:5000"
