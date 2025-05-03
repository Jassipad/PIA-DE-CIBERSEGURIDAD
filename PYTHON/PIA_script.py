"""
Script Principal - Análisis de Seguridad Web
Versión: 4.0 (Corregido y optimizado)
"""

import os
import json
import logging
from datetime import datetime
from PIA_modulo1 import buscar_en_google
from PIA_modulo2 import leer_urls
from PIA_modulo3 import AnalizadorVirusTotal
from PIA_modulo4 import AnalizadorAbuseIPDB
from PIA_modulo5 import GeneradorReportes


def configurar_log():
    """Configura el sistema de logging principal"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logs/principal.log',
        encoding='utf-8'
    )
    return logging.getLogger(__name__)


def mostrar_menu():
    """Muestra el menú principal con formato mejorado"""
    print("\n" + "═" * 50)
    print(" SISTEMA DE ANÁLISIS DE SEGURIDAD WEB ".center(50))
    print("═" * 50)
    print("\n1. 🔍 Buscar institución/persona en Google")
    print("2. 🦠 Analizar URLs con VirusTotal")
    print("3. 🛡️ Analizar URLs con AbuseIPDB")
    print("4. 📊 Generar reporte completo")
    print("5. 🚪 Salir")
    return input("\nSeleccione una opción (1-5): ")


def verificar_archivo(ruta, mensaje_error):
    """Verifica que un archivo exista y no esté vacío"""
    try:
        if not os.path.exists(ruta):
            print(f"\n⚠️ {mensaje_error}")
            return False

        with open(ruta, 'r') as f:
            if not f.read().strip():
                print(f"\n⚠️ El archivo está vacío: {os.path.basename(ruta)}")
                return False

        return True
    except Exception as e:
        print(f"\n⚠️ Error verificando archivo: {str(e)}")
        return False


def main():
    logger = configurar_log()
    try:
        # Configuración inicial
        os.makedirs('salidas', exist_ok=True)
        os.makedirs('logs', exist_ok=True)

        # Leer configuración
        try:
            with open('config.txt', 'r') as f:
                config = {line.split('=')[0]: line.split('=')[1].strip()
                          for line in f if '=' in line}

            vt_api_key = config.get('VIRUSTOTAL_API')
            abuse_api_key = config.get('ABUSEIPDB_API')

            if not all([vt_api_key, abuse_api_key]):
                raise ValueError("Faltan API keys en config.txt")
        except Exception as e:
            print(f"\n❌ Error en config.txt: {str(e)}")
            print("Asegúrese de tener un archivo config.txt con:")
            print("VIRUSTOTAL_API=su_clave")
            print("ABUSEIPDB_API=su_clave")
            return

        # Variables de estado
        archivo_urls = None
        archivo_vt = None
        archivo_abuse = None

        while True:
            opcion = mostrar_menu()

            try:
                if opcion == "1":
                    print("\n" + "═" * 50)
                    print(" BÚSQUEDA EN GOOGLE ".center(50))
                    print("═" * 50)

                    consulta = input("\nIngrese la institución o persona a buscar: ").strip()
                    if not consulta:
                        print("\n⚠️ Error: La consulta no puede estar vacía")
                        continue

                    print("\n⏳ Buscando en Google...")
                    archivo_urls = buscar_en_google(consulta)

                    if verificar_archivo(archivo_urls, "No se generaron resultados de búsqueda"):
                        print(f"\n✅ Resultados guardados en: {archivo_urls}")
                        with open(archivo_urls, 'r') as f:
                            print("\nPrimeras URLs encontradas:")
                            for i, line in enumerate(f.readlines()[:3], 1):
                                print(f"{i}. {line.strip()}")
                            if i == 3:
                                print("...")

                elif opcion == "2":
                    print("\n" + "═" * 50)
                    print(" ANÁLISIS CON VIRUSTOTAL ".center(50))
                    print("═" * 50)

                    if not verificar_archivo(archivo_urls, "Primero realice una búsqueda (Opción 1)"):
                        continue

                    print("\n⏳ Analizando con VirusTotal...")
                    analizador = AnalizadorVirusTotal(vt_api_key)
                    archivo_vt = analizador.analizar_urls(archivo_urls)

                    if verificar_archivo(archivo_vt, "No se generaron resultados de VirusTotal"):
                        print(f"\n✅ Resultados guardados en: {archivo_vt}")
                        with open(archivo_vt, 'r') as f:
                            data = json.load(f)
                            print("\nResumen de análisis:")
                            print(f"URLs analizadas: {len(data)}")
                            if data:
                                stats = data[0]['analisis']['data']['attributes']['last_analysis_stats']
                                print(f"\nPrimer resultado:")
                                print(f"URL: {data[0]['url']}")
                                print(f"Detecciones maliciosas: {stats.get('malicious', 0)}")
                                print(f"Detecciones sospechosas: {stats.get('suspicious', 0)}")

                elif opcion == "3":
                    print("\n" + "═" * 50)
                    print(" ANÁLISIS CON ABUSEIPDB ".center(50))
                    print("═" * 50)

                    if not verificar_archivo(archivo_urls, "Primero realice una búsqueda (Opción 1)"):
                        continue

                    print("\n⏳ Analizando con AbuseIPDB...")
                    try:
                        analizador = AnalizadorAbuseIPDB(abuse_api_key)
                        archivo_abuse = analizador.analizar_urls(archivo_urls)

                        if not os.path.exists(archivo_abuse):
                            raise FileNotFoundError("No se generó el archivo de resultados")

                        with open(archivo_abuse, 'r') as f:
                            data = json.load(f)
                            if not data:
                                raise ValueError("El archivo no contiene datos")

                        print(f"\n✅ Resultados guardados en: {archivo_abuse}")
                        with open(archivo_abuse, 'r') as f:
                            data = json.load(f)
                            print("\n🔍 Diagnóstico:")
                            print(f"URLs analizadas: {len(data)}")
                            if data:
                                primer_resultado = data[0]['analisis']['data']
                                print("\nPrimer resultado:")
                                print(f"Dominio: {data[0]['dominio']}")
                                print(f"Puntaje abuso: {primer_resultado.get('abuseConfidenceScore', 'N/A')}")
                                print(f"Reportes totales: {primer_resultado.get('totalReports', 'N/A')}")
                                print(f"ISP: {primer_resultado.get('isp', 'N/A')}")

                    except Exception as e:
                        print(f"\n❌ Error en AbuseIPDB: {str(e)}")
                        print("Posibles causas:")
                        print("- API key incorrecta o sin créditos")
                        print("- El dominio no está en la base de datos de AbuseIPDB")
                        print("- Problemas de conexión a internet")

                elif opcion == "4":
                    print("\n" + "═" * 50)
                    print(" GENERAR REPORTE ".center(50))
                    print("═" * 50)

                    if not all([
                        verificar_archivo(archivo_vt, "Complete el análisis VirusTotal (Opción 2)"),
                        verificar_archivo(archivo_abuse, "Complete el análisis AbuseIPDB (Opción 3)")
                    ]):
                        continue

                    print("\n⏳ Generando reporte combinado...")
                    generador = GeneradorReportes()
                    reporte = generador.generar_reporte_completo(archivo_vt, archivo_abuse)

                    if verificar_archivo(reporte, "No se pudo generar el reporte"):
                        print(f"\n✅ Reporte generado en: {reporte}")
                        with open(reporte, 'r') as f:
                            print("\nVista previa del reporte:")
                            print(f.read()[:500] + "...")

                elif opcion == "5":
                    print("\n¡Gracias por usar el sistema!")
                    break

                else:
                    print("\n⚠️ Opción no válida. Por favor ingrese 1-5")

            except Exception as e:
                logger.error(f"Error en opción {opcion}: {str(e)}")
                print(f"\n❌ Error inesperado: {str(e)}")

    except Exception as e:
        logger.critical(f"Error crítico: {str(e)}")
        print(f"\n❌ Error crítico: {str(e)}")
    finally:
        logger.info("Sistema terminado")


if __name__ == "__main__":
    main()
