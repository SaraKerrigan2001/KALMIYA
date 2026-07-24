$startupPath = [System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Start Menu\Programs\Startup\KALMIYA_Neural_Link.lnk')
$targetPath = 'c:\Users\maria\env\KALMIYA_System\Launch_KALMIYA.vbs'
$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut($startupPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = 'c:\Users\maria\env\KALMIYA_System'
$shortcut.Save()
Write-Host "Enlace creado con éxito en $startupPath"
