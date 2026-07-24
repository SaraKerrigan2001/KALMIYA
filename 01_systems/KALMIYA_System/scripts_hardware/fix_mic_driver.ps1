# Fix Digital Microphone Device - KALMIYA System
# Attempts to update the driver using the generic High Definition Audio driver

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KALMIYA - Microphone Driver Fix" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the problematic device
$device = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Digital microphone*' -and $_.Status -eq 'Error' }

if ($device) {
    Write-Host "[+] Dispositivo encontrado: $($device.FriendlyName)" -ForegroundColor Yellow
    Write-Host "[+] Estado actual: $($device.Status)" -ForegroundColor Red
    Write-Host "[+] InstanceId: $($device.InstanceId)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[*] Deshabilitando y rehabilitando el dispositivo..." -ForegroundColor Cyan
    
    # Try to disable and re-enable the device first
    try {
        Disable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 2
        Enable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 3
        
        # New: Attempt to force driver update from extracted INF
        $infPath = "C:\SWSetup\SP142490\IHV_ISST7767\IntcDMic.inf"
        if (Test-Path $infPath) {
            Write-Host "[*] Intentando forzar instalacion desde $infPath..." -ForegroundColor Cyan
            pnputil /add-driver $infPath /install
            pnputil /update-device $device.InstanceId $infPath /force
        }

        # Check if status changed
        $deviceAfter = Get-PnpDevice -InstanceId $device.InstanceId
        if ($deviceAfter.Status -eq 'OK') {
            Write-Host "[OK] El dispositivo ahora funciona correctamente!" -ForegroundColor Green
        } else {
            Write-Host "[!] El dispositivo sigue con error. Estado: $($deviceAfter.Status)" -ForegroundColor Yellow
            Write-Host "[*] Intentando buscar driver en Windows Update..." -ForegroundColor Cyan
            
            # Try Windows Update scan
            $SearchResult = (New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0 and Type='Driver'")
            if ($SearchResult.Updates.Count -gt 0) {
                Write-Host "[+] Se encontraron $($SearchResult.Updates.Count) actualizaciones de drivers disponibles:" -ForegroundColor Green
                foreach ($update in $SearchResult.Updates) {
                    Write-Host "    - $($update.Title)" -ForegroundColor White
                }
            } else {
                Write-Host "[!] No se encontraron drivers en Windows Update." -ForegroundColor Yellow
            }
            
            Write-Host ""
            Write-Host "==========================================" -ForegroundColor Yellow
            Write-Host "  RECOMENDACION:" -ForegroundColor Yellow
            Write-Host "  1. Ve a support.hp.com" -ForegroundColor White
            Write-Host "  2. Selecciona 'Portatil'" -ForegroundColor White
            Write-Host "  3. Ingresa serial: PLKRQ028JGR16V" -ForegroundColor White
            Write-Host "  4. Descarga 'Controlador - Audio'" -ForegroundColor White
            Write-Host "==========================================" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "[!] Se necesitan permisos de administrador." -ForegroundColor Yellow
        Write-Host "[*] Ejecuta este script como Administrador." -ForegroundColor Yellow
    }
} else {
    Write-Host "[?] No se encontro el dispositivo 'Digital microphone device' con error." -ForegroundColor Yellow
    Write-Host "[*] Verificando todos los dispositivos de audio..." -ForegroundColor Cyan
    Get-PnpDevice | Where-Object { $_.Class -eq 'AudioEndpoint' -or $_.Class -eq 'MEDIA' -or $_.FriendlyName -like '*microphone*' -or $_.FriendlyName -like '*audio*' } | 
        Select-Object Status, Class, FriendlyName | Format-Table -AutoSize
}
