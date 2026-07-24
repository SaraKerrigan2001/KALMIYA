# KALMIYA - HP OMEN 16-b0511la Driver Downloader
# Downloads all critical drivers from HP FTP

$downloadPath = "c:\Users\maria\env\KALMIYA_System\HP_Drivers"

$drivers = @(
    @{ Name = "Realtek_HD_Audio_Driver";      URL = "https://ftp.hp.com/pub/softpaq/sp142001-142500/sp142490.exe";  Size = "193.4 MB" },
    @{ Name = "Intel_Serial_IO_Driver";       URL = "https://ftp.hp.com/pub/softpaq/sp139001-139500/sp139425.exe";  Size = "~5 MB" },
    @{ Name = "Intel_Chipset_Utility";        URL = "https://ftp.hp.com/pub/softpaq/sp142001-142500/sp142406.exe";  Size = "~3 MB" },
    @{ Name = "Intel_MEI_Driver";             URL = "https://ftp.hp.com/pub/softpaq/sp142001-142500/sp142478.exe";  Size = "~90 MB" }
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  KALMIYA - HP OMEN Driver Downloader" -ForegroundColor Cyan
Write-Host "  Modelo: HP OMEN 16-b0511la" -ForegroundColor Cyan
Write-Host "  Destino: $downloadPath" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$total = $drivers.Count
$current = 0

foreach ($driver in $drivers) {
    $current++
    $fileName = ($driver.URL -split '/')[-1]
    $outputFile = Join-Path $downloadPath $fileName

    if (Test-Path $outputFile) {
        Write-Host "[$current/$total] EXISTE: $($driver.Name) - $fileName (ya descargado)" -ForegroundColor Yellow
        continue
    }

    Write-Host "[$current/$total] DESCARGANDO: $($driver.Name) ($($driver.Size))" -ForegroundColor Green
    Write-Host "             URL: $($driver.URL)" -ForegroundColor Gray
    Write-Host "             Archivo: $fileName" -ForegroundColor Gray

    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $driver.URL -OutFile $outputFile -UseBasicParsing
        $fileInfo = Get-Item $outputFile
        $sizeMB = [math]::Round($fileInfo.Length / 1MB, 1)
        Write-Host "             OK - Descargado ($sizeMB MB)" -ForegroundColor Green
    } catch {
        Write-Host "             ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DESCARGA COMPLETADA" -ForegroundColor Green
Write-Host "  Archivos en: $downloadPath" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Para instalar, ejecuta cada .exe como Administrador" -ForegroundColor Yellow
Write-Host "  Orden recomendado:" -ForegroundColor Yellow
Write-Host "    1. Intel_Chipset_Utility (sp142406.exe)" -ForegroundColor White
Write-Host "    2. Intel_Serial_IO (sp139425.exe)" -ForegroundColor White
Write-Host "    3. Intel_MEI (sp142478.exe)" -ForegroundColor White
Write-Host "    4. Realtek_HD_Audio (sp142490.exe) <-- MICROPHONE FIX" -ForegroundColor White
Write-Host "    5. Reiniciar el equipo" -ForegroundColor White
