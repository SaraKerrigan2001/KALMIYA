' crear_acceso_chat.vbs
' Crea un acceso directo "KALMIYA Chat" en el escritorio
' Ejecutar una sola vez con doble clic

Set oWS  = WScript.CreateObject("WScript.Shell")
Set fso  = CreateObject("Scripting.FileSystemObject")

strBase  = fso.GetParentFolderName(WScript.ScriptFullName)
vbsChat  = strBase & "\Lanzar_Chat_KALMIYA.vbs"
icoPath  = strBase & "\kalmiya.ico"
desktop  = oWS.SpecialFolders("Desktop")
linkFile = desktop & "\KALMIYA Chat.lnk"

' Crear el acceso directo
Set oLink = oWS.CreateShortcut(linkFile)
oLink.TargetPath       = "wscript.exe"
oLink.Arguments        = Chr(34) & vbsChat & Chr(34)
oLink.WorkingDirectory = strBase
oLink.Description      = "KALMIYA — Chat de IA"

' Usar el icono si existe
If fso.FileExists(icoPath) Then
    oLink.IconLocation = icoPath & ", 0"
End If

oLink.Save

MsgBox "Acceso directo creado en el escritorio:" & vbCrLf & Chr(34) & "KALMIYA Chat" & Chr(34), 64, "KALMIYA"

Set oLink = Nothing
Set oWS   = Nothing
Set fso   = Nothing
