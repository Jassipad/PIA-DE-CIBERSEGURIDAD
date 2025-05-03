<#
.SYNOPSIS
Calcula el hash SHA256 de un archivo y lo consulta en la API de VirusTotal.

.DESCRIPTION
Esta función calcula el hash de un archivo usando SHA256 y consulta si ha sido analizado por VirusTotal.
Muestra los resultados del análisis si existen.

.PARAMETER FilePath
Ruta del archivo a analizar.

#>
function Revisar-Hashes {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath
    )

    $key = "60399a3b6ae563e306fd9f1786dc4399f96635f22eaed9a5fe8a1dfd72500936"
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    Write-Host "Hash calculado: $($hash.Hash)" -Foreground Green
    $url = "https://www.virustotal.com/api/v3/files/$($hash.Hash)"
    
    try {
        $response = Invoke-RestMethod -Uri $url -Headers @{ "x-apikey" = $Key } -Method Get
        Write-Host "Respuesta de VirusTotal: $($response | ConvertTo-Json)" 

        if ($response.data) {
            if ($response.data.attributes.last_analysis_stats) {
                Write-Host "Análisis de VirusTotal:" -ForegroundColor Cyan
                $malicious = $response.data.attributes.last_analysis_stats.malicious
                $harmless = $response.data.attributes.last_analysis_stats.harmless

                if ($malicious -ne $null) {
                    Write-Host "Archivos detectados como maliciosos: $malicious"
                } else {
                    Write-Host "No se detectaron archivos maliciosos." -ForegroundColor Yellow
                }

                if ($harmless -ne $null) {
                    Write-Host "Archivos detectados como limpios: $harmless"
                } else {
                    Write-Host "No se detectaron archivos limpios." -ForegroundColor Yellow
                }
            }
        } elseif ($response.error.code -eq 'NotFoundError') {
            Write-Host "El archivo no se encuentra en la base de datos de VirusTotal. Puede que no haya sido analizado antes." -ForegroundColor Red
        } else {
            Write-Host "Error desconocido al consultar la API de VirusTotal." -ForegroundColor Red
        }
    } catch {
        Write-Host "Error al consultar la API de VirusTotal: $_" -ForegroundColor Red
    }
}