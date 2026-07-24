Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\KALMIYA.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)

' El acceso directo ejecutará el script VBS maestro
oLink.TargetPath = "wscript.exe"
oLink.Arguments = "c:\Users\maria\env\01_systems\KALMIYA_System\Lanzar_KALMIYA.vbs"
oLink.IconLocation = "c:\Users\maria\env\01_systems\KALMIYA_System\kalmiya.ico, 0"
oLink.WorkingDirectory = "c:\Users\maria\env\01_systems\KALMIYA_System"
oLink.Description = "KALMIYA - Neural AI Assistant"
oLink.Save
