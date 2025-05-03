Set-StrictMode -Version Latest

Write-Host "`nCdmlets utilizados:" -BackgroundColor DarkCyan 
Write-Host "∘Get-FileHash"
Write-Host "∘Write-Host"
Write-Host "∘Invoke-RestMethod"
Write-Host "∘ConvertTo-Json"
Write-Host "∘Get-ChildItem"
Write-Host "∘Where-Object"
Write-Host "∘ForEach-Object"
Write-Host "∘Get-CimInstance"

Write-Host "`nFunciones utilizadas:" -BackgroundColor DarkCyan
Write-Host "∘Revisar-Hashes"
Write-Host "∘Listar-Archivos"
Write-Host "∘Revisar-Recursos"

While ($true) {
    $op2= Read-Host "`n¿Desea buscar ayuda acerca de alguno de los cmdlets o funciones?(si/no)"
    if ($op2 -eq "si") {
        $bus= Read-Host "Ingrese el cmdlet o función a buscar"
        Get-Help $bus -Full
        $op3= Read-Host "¿Desea buscar ayuda nuevamente?(si/no)" 
        if ($op3 -eq "no") {
            break
        }
    } elseif ($op2 -eq "no") {
        break
    }
}

try {
    Import-Module C:\Users\Dell\Desktop\PIA\modulo1.ps1 -Force
    Import-Module C:\Users\Dell\Desktop\PIA\modulo2.ps1 -Force
    Import-Module C:\Users\Dell\Desktop\PIA\modulo3.ps1 -Force
} catch {
    Write-Host "Error al cargar los módulos: $_" -ForegroundColor Red
}


while ($true) {
    Write-Host "`nSeleccione una opción:" -Foreground Magenta
    Write-Host "1-Revisión de hashes y consulta a la API de VirusTotal."
    Write-Host "2-Listado de archivos ocultos."
    Write-Host "3-Revisión del uso de recursos del sistema."
    Write-Host "4-Salir."
    
    $op = Read-Host "Ingrese la opción deseada"

    try {
        switch ($op) {
            '1' {
                Import-Module C:\Users\Dell\Desktop\PIA\modulo1.ps1 -Force
                $archivo = Read-Host "Ingrese la ruta del documento a buscar"
                Revisar-Hashes -FilePath $archivo

            }
            '2' {
                Import-Module C:\Users\Dell\Desktop\PIA\modulo2.ps1 -Force
                $ruta = Read-Host "Ingrese la ruta donde desea buscar archivos ocultos"
                Listar-Archivos -Ruta $ruta

            }
            '3' {
                Import-Module C:\Users\Dell\Desktop\PIA\modulo3.ps1 -Force
                Revisar-Recursos
            }
            '4' {
                Write-Host "Saliendo del programa.." -ForegroundColor Yellow
                exit
            }
            default {
                Write-Host "Opción no válida, intente de nuevo."
            }
        }
    } catch {
        Write-Host "Error al ejecutar la opción seleccionado: $_"
    }
}