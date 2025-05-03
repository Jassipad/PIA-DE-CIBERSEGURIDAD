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
