# Script PowerShell para cambiar rápidamente entre ejemplos de componentes
# Uso: .\examples\cambiar-ejemplo.ps1 [nombre-componente]
# Ejemplo: .\examples\cambiar-ejemplo.ps1 BienesTable

param(
    [string]$Componente
)

$ejemplos = @{
    'AuthScreen' = 'App-AuthScreen.jsx'
    'LoadingScreen' = 'App-LoadingScreen.jsx'
    'Header' = 'App-Header.jsx'
    'Sidebar' = 'App-Sidebar.jsx'
    'Dashboard' = 'App-Dashboard.jsx'
    'BienesTable' = 'App-BienesTable.jsx'
    'BienModal' = 'App-BienModal.jsx'
    'CuentadantesTable' = 'App-CuentadantesTable.jsx'
    'CuentadanteModal' = 'App-CuentadanteModal.jsx'
    'AsignacionModal' = 'App-AsignacionModal.jsx'
    'StatsCards' = 'App-StatsCards.jsx'
    'NotificationContainer' = 'App-NotificationContainer.jsx'
    'NotificationCenter' = 'App-NotificationCenter.jsx'
    'PerfilModal' = 'App-PerfilModal.jsx'
    'ConfiguracionModal' = 'App-ConfiguracionModal.jsx'
}

function Mostrar-Ayuda {
    Write-Host ""
    Write-Host "📚 Cambiar Ejemplo de Componente" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\examples\cambiar-ejemplo.ps1 [componente]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Componentes disponibles:" -ForegroundColor Green
    $i = 1
    foreach ($nombre in $ejemplos.Keys | Sort-Object) {
        Write-Host "  $i. $nombre" -ForegroundColor White
        $i++
    }
    Write-Host ""
    Write-Host "Ejemplo: .\examples\cambiar-ejemplo.ps1 BienesTable" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para restaurar: .\examples\cambiar-ejemplo.ps1 restaurar" -ForegroundColor Magenta
    Write-Host ""
}

function Cambiar-Ejemplo {
    param([string]$NombreComponente)
    
    if (-not $ejemplos.ContainsKey($NombreComponente)) {
        Write-Host "❌ Error: Componente '$NombreComponente' no encontrado" -ForegroundColor Red
        Mostrar-Ayuda
        exit 1
    }

    $archivoEjemplo = $ejemplos[$NombreComponente]
    $rutaEjemplo = Join-Path $PSScriptRoot $archivoEjemplo
    $rutaApp = Join-Path $PSScriptRoot "..\src\App.jsx"

    try {
        # Leer el archivo de ejemplo
        $contenidoEjemplo = Get-Content $rutaEjemplo -Raw -Encoding UTF8
        
        # Hacer backup del App.jsx actual
        $backupPath = Join-Path $PSScriptRoot "..\src\App.jsx.backup"
        if (Test-Path $rutaApp) {
            Copy-Item $rutaApp $backupPath -Force
            Write-Host "💾 Backup creado: src\App.jsx.backup" -ForegroundColor Yellow
        }
        
        # Escribir el nuevo contenido
        Set-Content -Path $rutaApp -Value $contenidoEjemplo -Encoding UTF8
        
        Write-Host ""
        Write-Host "✅ Ejemplo cambiado exitosamente a: $NombreComponente" -ForegroundColor Green
        Write-Host "📄 Archivo: $archivoEjemplo" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🔄 El navegador se recargará automáticamente" -ForegroundColor Yellow
        Write-Host "💡 Para restaurar: .\examples\cambiar-ejemplo.ps1 restaurar" -ForegroundColor Magenta
        Write-Host ""
    }
    catch {
        Write-Host "❌ Error al cambiar ejemplo: $_" -ForegroundColor Red
        exit 1
    }
}

function Restaurar-Backup {
    $backupPath = Join-Path $PSScriptRoot "..\src\App.jsx.backup"
    $rutaApp = Join-Path $PSScriptRoot "..\src\App.jsx"

    if (-not (Test-Path $backupPath)) {
        Write-Host "❌ No se encontró backup para restaurar" -ForegroundColor Red
        exit 1
    }

    try {
        Copy-Item $backupPath $rutaApp -Force
        Write-Host ""
        Write-Host "✅ App.jsx restaurado desde backup" -ForegroundColor Green
        Write-Host "🔄 El navegador se recargará automáticamente" -ForegroundColor Yellow
        Write-Host ""
    }
    catch {
        Write-Host "❌ Error al restaurar backup: $_" -ForegroundColor Red
        exit 1
    }
}

# Procesar argumentos
if ([string]::IsNullOrEmpty($Componente)) {
    Mostrar-Ayuda
    exit 0
}

switch ($Componente.ToLower()) {
    'restaurar' { Restaurar-Backup }
    'restore' { Restaurar-Backup }
    'ayuda' { Mostrar-Ayuda }
    'help' { Mostrar-Ayuda }
    '-h' { Mostrar-Ayuda }
    '--help' { Mostrar-Ayuda }
    default { Cambiar-Ejemplo -NombreComponente $Componente }
}
