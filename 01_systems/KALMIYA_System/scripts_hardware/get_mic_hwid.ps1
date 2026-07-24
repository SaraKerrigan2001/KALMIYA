$devices = Get-PnpDevice | Where-Object { $_.FriendlyName -like '*Digital microphone*' }
foreach ($dev in $devices) {
    Write-Host "Device: $($dev.FriendlyName)"
    Write-Host "Status: $($dev.Status)"
    Write-Host "InstanceId: $($dev.InstanceId)"
    $props = Get-PnpDeviceProperty -InstanceId $dev.InstanceId -KeyName DEVPKEY_Device_HardwareIds
    Write-Host "Hardware IDs:"
    $props.Data | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
}
