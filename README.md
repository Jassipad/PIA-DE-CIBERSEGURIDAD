# ProyectoFinal_Ciberseguridad

Aplicar conocimientos de programacion en Powershell, Bash y Python para desarrollar scripts y modulos orientados a tareas de ciberseguridad, integrando el uso de Github para el control de versiones y publicacion de resultados

POWERSHELL

Al inicio del programa se muestra una lista de los parámetros  las funciones utilizadas, de las cuales puedes obtener información gracias al Get-Help.
Se importan los módulos, aquí es necesario descargar el programa  los módulos, al igual de modificar la ruta especificada.
Finalmente, nos adentramos al menú con cuatro opciones y salimos del bucle con el número '4'.

En el módulo 1, es necesario verificar primero el archivo deseado desde el API de 'VirusTotal' ya que de lo contrario marcará error ya que no está en la nube del API.

En el módulo 2, solamente es introducir la ruta del directorio donde se buscarán los archivos ocultos.

BASH
# Herramientas de Ciberseguridad para Git Bash

## 🔍 1. Escaneo de Puertos
- **Función**: Escanea puertos TCP/UDP en un objetivo
- **Características**:
  - Menú interactivo con 7 opciones
  - Detección de puertos abiertos/cerrados
  - Ping automático a redes con máscara configurable
  - Genera reportes en archivo

## 📡 2. Monitor de Red
- **Función**: Analiza tráfico y conexiones de red
- **Características**:
  - Monitoreo de interfaces y ancho de banda
  - Ping continuo y traceroute integrado
  - Muestra conexiones activas TCP/UDP
  - Configuración de tiempos personalizados

**Uso**: Ejecutar con `bash nombre_script.sh` en Git Bash

# Herramientas de Ciberseguridad para Git Bash

## 📋 Requisitos Previos

### Para ambos scripts:
- **Git Bash** (instalado con [Git para Windows](https://gitforwindows.org/))
- **Paquetes básicos de red** (vienen con Windows)

### 🔍 1. Escaneo de Puertos
- **Herramientas requeridas**:
  ```bash
  # Instalar netcat (opcional para escaneo UDP)
  choco install netcat -y  # Usando Chocolatey
  # O descargar manualmente de https://nmap.org/ncat/

ejecutar los archivos:
  bash escaneo_puertos.sh
# o
bash escaneo_redes.sh




PYTHON


Este proyecto realiza búsquedas en Google sobre instituciones o personas, analiza las URLs obtenidas con las APIs de [VirusTotal](https://www.virustotal.com) y [AbuseIPDB](https://www.abuseipdb.com), y genera reportes de seguridad con los resultados.

Debes crear un archivo `config.txt` en la raíz con este formato:
VIRUSTOTAL_API=tu_clave_de_virustotal
ABUSEIPDB_API=tu_clave_de_abuseipdb

Corre el sistema con: python PIA_script.py
Desde el menú podrás:
1. Buscar en Google y guardar los links
2. Analizar los links con VirusTotal
3. Analizar los links con AbuseIPDB
4. Generar un reporte completo
5. Salir




