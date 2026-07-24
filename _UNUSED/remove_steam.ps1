$steamPath = "C:\Program Files (x86)\Steam"
$tempEmpty = "C:\Temp_Empty_Dir"

# Crear carpeta vacía
if (-not (Test-Path $tempEmpty)) { New-Item -ItemType Directory -Path $tempEmpty -Force | Out-Null }

# Espejo a carpeta vacía (borra Steam)
robocopy $tempEmpty $steamPath /MIR /R:0 /W:0 2>&1 | Out-Null

# Eliminar carpetas
Remove-Item -Path $steamPath -Force -ErrorAction SilentlyContinue
Remove-Item -Path $tempEmpty -Force -ErrorAction SilentlyContinue

# Verificar
if (Test-Path $steamPath) { "FAIL: exists" } else { "SUCCESS: removed" }
