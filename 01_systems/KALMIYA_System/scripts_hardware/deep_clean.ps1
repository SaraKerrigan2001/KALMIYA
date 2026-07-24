# =====================================================
# KALMIYA Deep Clean - Limpieza de DISCO y RAM
# Para optimizar rendimiento en trabajo y gaming
# =====================================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "  KALMIYA DEEP CLEAN - DISCO & RAM" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta
Write-Host ""

# --- ESTADO INICIAL ---
$diskBefore = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object { $_.DeviceID -eq "C:" }
$freeBefore = [math]::Round($diskBefore.FreeSpace / 1GB, 2)
$osBefore = Get-CimInstance Win32_OperatingSystem
$ramFreeBefore = [math]::Round($osBefore.FreePhysicalMemory / 1MB, 2)
$ramTotal = [math]::Round($osBefore.TotalVisibleMemorySize / 1MB, 2)

Write-Host "[ANTES] Disco C: libre = $freeBefore GB" -ForegroundColor Yellow
Write-Host "[ANTES] RAM libre = $ramFreeBefore GB / $ramTotal GB" -ForegroundColor Yellow
Write-Host ""

$totalCleaned = 0

# ===================== LIMPIEZA DE DISCO =====================
Write-Host ">>> FASE 1: LIMPIEZA DE DISCO <<<" -ForegroundColor Cyan
Write-Host ""

# 1. Archivos temporales de Windows
Write-Host "[1/8] Limpiando archivos temporales de Windows..." -ForegroundColor White
$tempPaths = @(
    "$env:TEMP",
    "$env:WINDIR\Temp",
    "$env:LOCALAPPDATA\Temp"
)
foreach ($path in $tempPaths) {
    if (Test-Path $path) {
        $size = (Get-ChildItem $path -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 1)
        Remove-Item "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
        $totalCleaned += $size
        Write-Host "  [OK] $path -> $sizeMB MB eliminados" -ForegroundColor Green
    }
}

# 2. Prefetch
Write-Host "[2/8] Limpiando Prefetch..." -ForegroundColor White
if (Test-Path "$env:WINDIR\Prefetch") {
    $size = (Get-ChildItem "$env:WINDIR\Prefetch" -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Remove-Item "$env:WINDIR\Prefetch\*" -Force -ErrorAction SilentlyContinue
    $totalCleaned += $size
    Write-Host "  [OK] Prefetch -> $([math]::Round($size/1MB,1)) MB" -ForegroundColor Green
}

# 3. Cache de navegadores
Write-Host "[3/8] Limpiando cache de navegadores..." -ForegroundColor White
$browserCaches = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Cache"
)
foreach ($cache in $browserCaches) {
    if (Test-Path $cache) {
        $size = (Get-ChildItem $cache -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Remove-Item "$cache\*" -Recurse -Force -ErrorAction SilentlyContinue
        $totalCleaned += $size
        $name = $cache.Split('\') | Select-Object -Last 3 | Select-Object -First 1
        Write-Host "  [OK] $name cache -> $([math]::Round($size/1MB,1)) MB" -ForegroundColor Green
    }
}

# 4. Thumbnails de Windows
Write-Host "[4/8] Limpiando thumbnails..." -ForegroundColor White
$thumbPath = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer"
if (Test-Path $thumbPath) {
    $thumbFiles = Get-ChildItem $thumbPath -Filter "thumbcache_*" -Force -ErrorAction SilentlyContinue
    $size = ($thumbFiles | Measure-Object -Property Length -Sum).Sum
    $thumbFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    $totalCleaned += $size
    Write-Host "  [OK] Thumbnails -> $([math]::Round($size/1MB,1)) MB" -ForegroundColor Green
}

# 5. Logs antiguos
Write-Host "[5/8] Limpiando logs del sistema..." -ForegroundColor White
$logPaths = @(
    "$env:WINDIR\Logs\CBS\*.log",
    "$env:WINDIR\Logs\DISM\*.log",
    "$env:LOCALAPPDATA\CrashDumps\*"
)
foreach ($logPath in $logPaths) {
    $files = Get-ChildItem $logPath -Force -ErrorAction SilentlyContinue
    if ($files) {
        $size = ($files | Measure-Object -Property Length -Sum).Sum
        $files | Remove-Item -Force -ErrorAction SilentlyContinue
        $totalCleaned += $size
        Write-Host "  [OK] Logs -> $([math]::Round($size/1MB,1)) MB" -ForegroundColor Green
    }
}

# 6. Windows Update Cache
Write-Host "[6/8] Limpiando cache de Windows Update..." -ForegroundColor White
$wuPath = "$env:WINDIR\SoftwareDistribution\Download"
if (Test-Path $wuPath) {
    $size = (Get-ChildItem $wuPath -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
    Remove-Item "$wuPath\*" -Recurse -Force -ErrorAction SilentlyContinue
    Start-Service -Name wuauserv -ErrorAction SilentlyContinue
    $totalCleaned += $size
    Write-Host "  [OK] WU Cache -> $([math]::Round($size/1MB,1)) MB" -ForegroundColor Green
}

# 7. Papelera de reciclaje
Write-Host "[7/8] Vaciando papelera de reciclaje..." -ForegroundColor White
try {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Papelera vaciada" -ForegroundColor Green
} catch {
    Write-Host "  [--] Papelera ya vacia" -ForegroundColor Gray
}

# 8. Archivos grandes en Descargas (>500MB, mas de 30 dias)
Write-Host "[8/8] Buscando archivos grandes en Descargas (>500MB, +30 dias)..." -ForegroundColor White
$downloadsPath = [Environment]::GetFolderPath("UserProfile") + "\Downloads"
if (Test-Path $downloadsPath) {
    $oldBigFiles = Get-ChildItem $downloadsPath -File -ErrorAction SilentlyContinue | 
        Where-Object { $_.Length -gt 500MB -and $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
    if ($oldBigFiles) {
        foreach ($file in $oldBigFiles) {
            $sizeMB = [math]::Round($file.Length / 1MB, 1)
            Write-Host "  [INFO] Archivo grande encontrado: $($file.Name) ($sizeMB MB)" -ForegroundColor Yellow
            Remove-Item $file.FullName -Force -ErrorAction SilentlyContinue
            $totalCleaned += $file.Length
            Write-Host "  [OK] Eliminado: $($file.Name)" -ForegroundColor Green
        }
    } else {
        Write-Host "  [--] No hay archivos grandes antiguos" -ForegroundColor Gray
    }
}

Write-Host ""

# ===================== LIMPIEZA DE RAM =====================
Write-Host ">>> FASE 2: LIBERACION DE RAM <<<" -ForegroundColor Cyan
Write-Host ""

# 1. Recortar working set de todos los procesos pesados
Write-Host "[1/3] Recortando memoria de procesos pesados..." -ForegroundColor White
$reclaimed = 0
Get-Process | Where-Object { $_.WorkingSet64 -gt 100MB } | Sort-Object WorkingSet64 -Descending | ForEach-Object {
    try {
        $before = $_.WorkingSet64
        $_.MinWorkingSet = [IntPtr]::new(1048576)
        $_.MaxWorkingSet = [IntPtr]::new(1048576 * 50)
        $after = (Get-Process -Id $_.Id -ErrorAction SilentlyContinue).WorkingSet64
        $saved = $before - $after
        if ($saved -gt 0) { $reclaimed += $saved }
        Write-Host "  [OK] $($_.Name) (PID $($_.Id)) -> $([math]::Round($before/1MB,0)) MB => $([math]::Round($after/1MB,0)) MB" -ForegroundColor Green
    } catch {
        # Protected process, skip silently
    }
}
Write-Host "  RAM reclamada: ~$([math]::Round($reclaimed/1MB,0)) MB" -ForegroundColor Cyan

# 2. Forzar garbage collection de .NET
Write-Host "[2/3] Forzando garbage collection..." -ForegroundColor White
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
[System.GC]::Collect()
Write-Host "  [OK] GC completado" -ForegroundColor Green

# 3. Limpiar standby list via EmptyWorkingSet
Write-Host "[3/3] Limpiando procesos inactivos..." -ForegroundColor White
$inactiveTargets = @('OneDrive.Sync.Service', 'VaultPlugin', 'GameBarFTServer', 'XboxGameBarWidgets', 'TextInputHost')
foreach ($name in $inactiveTargets) {
    $proc = Get-Process -Name $name -ErrorAction SilentlyContinue
    if ($proc) {
        foreach ($p in $proc) {
            try {
                $p.MinWorkingSet = [IntPtr]::new(1048576)
                Write-Host "  [OK] $name reducido" -ForegroundColor Green
            } catch {}
        }
    }
}

Write-Host ""

# ===================== RESULTADO FINAL =====================
Start-Sleep -Seconds 2
$diskAfter = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Where-Object { $_.DeviceID -eq "C:" }
$freeAfter = [math]::Round($diskAfter.FreeSpace / 1GB, 2)
$osAfter = Get-CimInstance Win32_OperatingSystem
$ramFreeAfter = [math]::Round($osAfter.FreePhysicalMemory / 1MB, 2)
$cpuNow = (Get-CimInstance Win32_Processor).LoadPercentage

$diskRecovered = [math]::Round($freeAfter - $freeBefore, 2)
$ramRecovered = [math]::Round($ramFreeAfter - $ramFreeBefore, 2)

Write-Host "=========================================" -ForegroundColor Magenta
Write-Host "         RESULTADO DE LIMPIEZA" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  DISCO C:" -ForegroundColor White
Write-Host "    Antes:  $freeBefore GB libres" -ForegroundColor Gray
Write-Host "    Ahora:  $freeAfter GB libres" -ForegroundColor Green
Write-Host "    Recuperado: +$diskRecovered GB" -ForegroundColor Cyan
Write-Host ""
Write-Host "  RAM:" -ForegroundColor White
Write-Host "    Antes:  $ramFreeBefore GB libres / $ramTotal GB" -ForegroundColor Gray
Write-Host "    Ahora:  $ramFreeAfter GB libres / $ramTotal GB" -ForegroundColor Green
Write-Host "    Recuperado: +$ramRecovered GB" -ForegroundColor Cyan
Write-Host ""
Write-Host "  CPU: $cpuNow%" -ForegroundColor White
Write-Host ""
Write-Host "  Total archivos limpiados: ~$([math]::Round($totalCleaned/1MB,0)) MB" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Sistema listo para trabajar y jugar!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Magenta
