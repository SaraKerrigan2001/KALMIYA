Set oWS = WScript.CreateObject("WScript.Shell")
sStartup = oWS.SpecialFolders("Startup")
sLinkFile = sStartup & "\KALMIYA.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)

' Ejecutar el lanzador maestro al iniciar sesión
oLink.TargetPath = "wscript.exe"
oLink.Arguments = "c:\Users\maria\env\KALMIYA_System\Lanzar_KALMIYA.vbs"
oLink.IconLocation = "c:\Users\maria\env\KALMIYA_System\kalmiya.ico, 0"
oLink.WorkingDirectory = "c:\Users\maria\env\KALMIYA_System"
oLink.Description = "KALMIYA Neural Core - Auto Launch"
oLink.Save
