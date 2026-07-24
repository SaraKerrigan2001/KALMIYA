$mic = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*microphone*' }
$bt = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Bluetooth*' }

Write-Host "--- ESTADO DE DISPOSITIVOS ---" -ForegroundColor Cyan
Write-Host ""

if ($mic) {
    foreach ($m in $mic) {
        $color = if ($m.Status -eq 'OK') { 'Green' } else { 'Red' }
        Write-Host "Microfono: $($m.FriendlyName)" -NoNewline
        Write-Host " -> ESTADO: $($m.Status)" -ForegroundColor $color
    }
} else {
    Write-Host "Microfono: NO ENCONTRADO" -ForegroundColor Red
}

Write-Host ""

if ($bt) {
    foreach ($b in $bt) {
        $color = if ($b.Status -eq 'OK') { 'Green' } else { 'Red' }
        Write-Host "Bluetooth: $($b.FriendlyName)" -NoNewline
        Write-Host " -> ESTADO: $($b.Status)" -ForegroundColor $color
    }
} else {
    Write-Host "Bluetooth: NO ENCONTRADO" -ForegroundColor Red
}
