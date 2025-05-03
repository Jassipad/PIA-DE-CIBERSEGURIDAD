<#
.SYNOPSIS
Muestra el uso actual de CPU, memoria RAM y discos del sistema.

.DESCRIPTION
Consulta y muestra el uso promedio de CPU, uso total y disponible de memoria RAM,
y el estado de los discos locales del sistema.

#>

function Revisar-Recursos {
    Write-Host "Revisando el uso de recursos del sistema..." -ForegroundColor Cyan

    $cpu = Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property LoadPercentage -Average
    Write-Host "`nUso promedio de CPU: $($cpu.Average)%"

    $ram = Get-CimInstance -ClassName Win32_OperatingSystem
    $totalRAM = [math]::round($ram.TotalVisibleMemorySize / 1MB, 2)
    $freeRAM = [math]::round($ram.FreePhysicalMemory / 1MB, 2)
    $usedRAM = [math]::round($totalRAM - $freeRAM, 2)
    Write-Host "Uso de memoria RAM: $usedRAM GB / $totalRAM GB"

    $discos = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3"
    foreach ($d in $discos) {
        $total = [math]::round($d.Size / 1GB, 2)
        $libre = [math]::round($d.FreeSpace / 1GB, 2)
        $usado = [math]::round($total - $libre, 2)
        Write-Host "`nDisco: $($d.DeviceID)"
        Write-Host "  Usado: $usado GB / $total GB"
    }
}
