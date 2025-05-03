<#
.SYNOPSIS
Lista todos los archivos ocultos en una ruta especificada.

.DESCRIPTION
Busca archivos ocultos de forma recursiva en la ruta indicada y los muestra en pantalla.

.PARAMETER Ruta
Ruta donde se desea buscar archivos ocultos. Por defecto es el directorio actual.

#>

function Listar-Archivos {
    param (
        [string]$Ruta = "."
    )

    try {
        Write-Host "Buscando archivos ocultos en: $Ruta" -ForegroundColor Cyan
        $archivosOcultos = Get-ChildItem -Path $Ruta -Recurse -Force -ErrorAction Stop |
                           Where-Object { $_.Attributes -match "Hidden" }

        if (-not $archivosOcultos) {
            Write-Host "No se encontraron archivos ocultos." -ForegroundColor Yellow
        } else {
            Write-Host "Archivos ocultos encontrados:" -ForegroundColor Green
            $archivosOcultos | ForEach-Object {
                Write-Host $_.FullName -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "Error al buscar archivos ocultos: $_" -ForegroundColor Red
    }
}
