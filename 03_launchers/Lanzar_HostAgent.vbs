' Lanzar_HostAgent.vbs
' Lanzador silencioso del Host Agent de KALMIYA
' Corre kalmiya_host_agent.py en segundo plano (sin ventana)
' para que Docker pueda consultar el estado real del PC.

Set fso = CreateObject("Scripting.FileSystemObject")

' Ruta al script del host agent
strBase     = "c:\Users\maria\env\03_launchers"
pythonPath  = "C:\Python314\python.exe"
agentPath   = strBase & "\kalmiya_host_agent.py"

' Verificar que Python existe
If Not fso.FileExists(pythonPath) Then
    MsgBox "No se encontro Python en: " & pythonPath & vbCrLf & _
           "Edita la variable pythonPath en este archivo.", _
           16, "KALMIYA Host Agent - Error"
    WScript.Quit
End If

' Verificar que el script existe
If Not fso.FileExists(agentPath) Then
    MsgBox "No se encontro el Host Agent en: " & agentPath, _
           16, "KALMIYA Host Agent - Error"
    WScript.Quit
End If

' Ejecutar sin ventana (0 = oculto)
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & pythonPath & Chr(34) & " " & Chr(34) & agentPath & Chr(34), 0, False

' Limpiar
Set WshShell = Nothing
Set fso = Nothing
