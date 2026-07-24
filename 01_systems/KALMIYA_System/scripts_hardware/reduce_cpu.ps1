# KALMIYA CPU Optimization Script
# Reduce CPU usage by lowering priority of non-essential processes

Write-Host "=== KALMIYA: Optimizacion de CPU ===" -ForegroundColor Cyan

# 1. Bajar prioridad de procesos no esenciales
$targets = @('Discord', 'Battle.net', 'steam', 'steamwebhelper', 'OneDrive', 'HPAudioSwitch', 'SmartConnect', 'Agent')
foreach ($name in $targets) {
    Get-Process -Name $name -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            $_.PriorityClass = 'BelowNormal'
            Write-Host "  [OK] Prioridad reducida: $($_.Name) (PID $($_.Id))" -ForegroundColor Green
        } catch {
            Write-Host "  [!!] No se pudo cambiar: $($_.Name)" -ForegroundColor Yellow
        }
    }
}

# 2. Reducir afinidad de CPU de procesos pesados (limitar a 2 nucleos)
$heavyProcesses = @('Discord', 'Battle.net', 'steam')
foreach ($name in $heavyProcesses) {
    Get-Process -Name $name -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            $_.ProcessorAffinity = 0x3  # Solo nucleos 0 y 1
            Write-Host "  [OK] Afinidad limitada: $($_.Name) (PID $($_.Id))" -ForegroundColor Green
        } catch {
            Write-Host "  [!!] No se pudo limitar afinidad: $($_.Name)" -ForegroundColor Yellow
        }
    }
}

# 3. Limpiar memoria de trabajo de procesos con alto consumo
Write-Host "`n--- Limpiando memoria de trabajo ---" -ForegroundColor Cyan
Get-Process | Where-Object { $_.WorkingSet64 -gt 200MB } | ForEach-Object {
    try {
        $sizeBefore = [math]::Round($_.WorkingSet64/1MB, 1)
        [System.Diagnostics.Process]::GetProcessById($_.Id).MinWorkingSet = [IntPtr]::new(1048576)
        Write-Host "  [OK] Memoria recortada: $($_.Name) ($sizeBefore MB)" -ForegroundColor Green
    } catch {
        # Silently skip protected processes
    }
}

# 4. Desactivar servicios de indexacion temporalmente
Write-Host "`n--- Ajustes adicionales ---" -ForegroundColor Cyan
try {
    Stop-Service -Name "WSearch" -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Windows Search pausado" -ForegroundColor Green
} catch {
    Write-Host "  [!!] No se pudo pausar Windows Search" -ForegroundColor Yellow
}

# 5. Configurar plan de energia a Equilibrado con ahorro
try {
    powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
    Write-Host "  [OK] Plan de energia: Equilibrado" -ForegroundColor Green
} catch {}

# 6. Verificar resultado
Start-Sleep -Seconds 2
$cpuLoad = (Get-CimInstance Win32_Processor).LoadPercentage
Write-Host "`n=== CPU actual: $cpuLoad% ===" -ForegroundColor Cyan
Write-Host "Optimizacion completada." -ForegroundColor Green
