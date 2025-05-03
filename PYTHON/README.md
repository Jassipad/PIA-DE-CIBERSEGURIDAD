
# 🛡️ Sistema de Análisis de Seguridad Web

Este proyecto realiza búsquedas en Google sobre instituciones o personas, analiza las URLs obtenidas con las APIs de [VirusTotal](https://www.virustotal.com) y [AbuseIPDB](https://www.abuseipdb.com), y genera reportes de seguridad con los resultados.

## 📁 Estructura del Proyecto

```
PIA/
├── PIA_modulo1.py        # Búsqueda en Google y guardado de URLs
├── PIA_modulo2.py        # Lectura y validación de URLs
├── PIA_modulo3.py        # Análisis con VirusTotal
├── PIA_modulo4.py        # Análisis con AbuseIPDB
├── PIA_modulo5.py        # Generación de reportes
├── main.py               # Script principal con menú interactivo
├── config.txt            # Contiene tus API Keys
├── salidas/              # Archivos de resultados generados
└── logs/                 # Logs de errores y ejecución
```

## 🔧 Requisitos

- Python 3.7 o superior
- Instalar dependencias con:

```bash
pip install googlesearch-python requests
```

## 🔑 Archivo `config.txt`

Debes crear un archivo `config.txt` en la raíz con este formato:

```
VIRUSTOTAL_API=tu_clave_de_virustotal
ABUSEIPDB_API=tu_clave_de_abuseipdb
```

## ▶️ Ejecución

Corre el sistema con:

```bash
python main.py
```

Desde el menú podrás:

1. Buscar en Google y guardar los links
2. Analizar los links con VirusTotal
3. Analizar los links con AbuseIPDB
4. Generar un reporte completo
5. Salir
