' Lanzar_Chat_KALMIYA.vbs
' Abre directamente el Chat de KALMIYA (sin launcher completo)
' Sin ventana de consola, sin permisos de admin requeridos

Set fso = CreateObject("Scripting.FileSystemObject")

' Rutas
strBase   = "c:\Users\maria\env\01_systems\KALMIYA_System"
pythonPath = "C:\Python314\python.exe"
chatPath   = strBase & "\kalmiya_chat.py"

' Verificar Python — usar el del sistema si el principal no existe
If Not fso.FileExists(pythonPath) Then
    pythonPath = "C:\Users\maria\AppData\Local\Programs\Python\Python313\python.exe"
End If

' Verificar chat
If Not fso.FileExists(chatPath) Then
    MsgBox "No se encontro kalmiya_chat.py en:" & vbCrLf & chatPath, 16, "KALMIYA Chat Error"
    WScript.Quit
End If

' Lanzar sin ventana de consola (0 = oculta, False = no esperar)
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = strBase
WshShell.Run Chr(34) & pythonPath & Chr(34) & " " & Chr(34) & chatPath & Chr(34), 0, False

Set WshShell = Nothing
Set fso = Nothing
