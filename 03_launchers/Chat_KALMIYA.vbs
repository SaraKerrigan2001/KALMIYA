Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d ""c:\Users\maria\env"" && python 03_launchers\chat.py", 0, False
Set WshShell = Nothing
