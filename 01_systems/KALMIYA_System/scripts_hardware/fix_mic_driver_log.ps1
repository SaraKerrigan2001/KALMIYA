$logFile = "c:\Users\maria\env\KALMIYA_System\mic_fix_result.txt"

"========================================" | Out-File $logFile
"  KALMIYA - Microphone Driver Fix" | Out-File $logFile -Append
"  $(Get-Date)" | Out-File $logFile -Append
"========================================" | Out-File $logFile -Append
"" | Out-File $logFile -Append

$device = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Digital microphone*' -and $_.Status -eq 'Error' }

if ($device) {
    "[+] Dispositivo encontrado: $($device.FriendlyName)" | Out-File $logFile -Append
    "[+] Estado actual: $($device.Status)" | Out-File $logFile -Append
    "[+] InstanceId: $($device.InstanceId)" | Out-File $logFile -Append
    "" | Out-File $logFile -Append
    "[*] Deshabilitando y rehabilitando el dispositivo..." | Out-File $logFile -Append

    try {
        Disable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 2
        Enable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 3

        $deviceAfter = Get-PnpDevice -InstanceId $device.InstanceId
        if ($deviceAfter.Status -eq 'OK') {
            "[OK] El dispositivo ahora funciona correctamente!" | Out-File $logFile -Append
        } else {
            "[!] El dispositivo sigue con error. Estado: $($deviceAfter.Status)" | Out-File $logFile -Append
            "[*] Buscando drivers en Windows Update..." | Out-File $logFile -Append
            
            try {
                $SearchResult = (New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0 and Type='Driver'")
                if ($SearchResult.Updates.Count -gt 0) {
                    "[+] Se encontraron $($SearchResult.Updates.Count) drivers disponibles:" | Out-File $logFile -Append
                    foreach ($update in $SearchResult.Updates) {
                        "    - $($update.Title)" | Out-File $logFile -Append
                    }
                } else {
                    "[!] No se encontraron drivers en Windows Update." | Out-File $logFile -Append
                }
            } catch {
                "[!] Error buscando en Windows Update: $($_.Exception.Message)" | Out-File $logFile -Append
            }
        }
    } catch {
        "[ERROR] $($_.Exception.Message)" | Out-File $logFile -Append
        "[!] Se necesitan permisos de administrador." | Out-File $logFile -Append
    }
} else {
    "[?] No se encontro dispositivo con error." | Out-File $logFile -Append
    "[*] Listando dispositivos de audio..." | Out-File $logFile -Append
    Get-PnpDevice | Where-Object { $_.Class -eq 'AudioEndpoint' -or $_.Class -eq 'MEDIA' -or $_.FriendlyName -like '*microphone*' -or $_.FriendlyName -like '*audio*' } | 
        Select-Object Status, Class, FriendlyName | Format-Table -AutoSize | Out-String | Out-File $logFile -Append
}

"" | Out-File $logFile -Append
"========== FIN ==========" | Out-File $logFile -Append
