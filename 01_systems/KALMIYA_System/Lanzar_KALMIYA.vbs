' Lanzar_KALMIYA.vbs
' Lanzador oficial de KALMIYA con permisos de Administrador
' Se ejecuta automaticamente al iniciar Windows

Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' Ruta base del sistema KALMIYA
strBase = "c:\Users\maria\env\01_systems\KALMIYA_System"
pythonPath = "C:\Python314\python.exe"
launcherPath = strBase & "\kalmiya_launcher.py"

' Verificar que existen los archivos
If Not fso.FileExists(pythonPath) Then
    MsgBox "No se encontro Python en: " & pythonPath, 16, "KALMIYA Error"
    WScript.Quit
End If

If Not fso.FileExists(launcherPath) Then
    MsgBox "No se encontro el launcher en: " & launcherPath, 16, "KALMIYA Error"
    WScript.Quit
End If

' Ejecutar KALMIYA como Administrador (elevado)
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute pythonPath, Chr(34) & launcherPath & Chr(34), strBase, "runas", 1

' Limpiar
Set objShell = Nothing
Set fso = Nothing
Set WshShell = Nothing
