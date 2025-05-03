import json
import os
from datetime import datetime
import logging

def configurar_log():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logs/reportes.log'
    )
    return logging.getLogger(__name__)

class GeneradorReportes:
    def __init__(self):
        self.logger = configurar_log()
        os.makedirs('salidas', exist_ok=True)

    def generar_reporte_completo(self, archivo_vt, archivo_abuse):
        """Genera un reporte combinado verificando datos"""
        try:
            self.logger.info(f"Iniciando generación de reporte con {archivo_vt} y {archivo_abuse}")
            
            # Verificar existencia de archivos
            if not all([os.path.exists(archivo_vt), os.path.exists(archivo_abuse)]):
                raise FileNotFoundError("Archivos de análisis no encontrados")
            
            # Leer datos con verificación
            datos_vt = self._leer_y_validar(archivo_vt, "VirusTotal")
            datos_abuse = self._leer_y_validar(archivo_abuse, "AbuseIPDB")
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"salidas/reporte_completo_{timestamp}.txt"
            
            # Generar contenido del reporte
            contenido = self._generar_contenido(datos_vt, datos_abuse)
            
            # Escribir archivo
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            self.logger.info(f"Reporte generado correctamente en {archivo_salida}")
            return archivo_salida
            
        except Exception as e:
            self.logger.error(f"Error generando reporte: {str(e)}")
            raise

    def _leer_y_validar(self, archivo, tipo):
        """Lee y valida los archivos de análisis"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            if not isinstance(datos, list):
                raise ValueError(f"Formato inválido en {tipo}: no es una lista")
                
            if not datos:
                raise ValueError(f"Datos vacíos en {tipo}")
                
            return datos
            
        except json.JSONDecodeError:
            raise ValueError(f"Archivo {tipo} no es un JSON válido")
        except Exception as e:
            raise ValueError(f"Error leyendo {tipo}: {str(e)}")

    def _generar_contenido(self, datos_vt, datos_abuse):
        """Genera el contenido completo del reporte"""
        try:
            contenido = []
            
            # Cabecera
            contenido.append("═"*50)
            contenido.append(" INFORME DE SEGURIDAD WEB ".center(50))
            contenido.append("═"*50)
            contenido.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Sección VirusTotal
            contenido.append("\n" + "═"*50)
            contenido.append(" VIRUSTOTAL ".center(50))
            contenido.append("═"*50 + "\n")
            
            for i, item in enumerate(datos_vt, 1):
                stats = item.get('analisis', {}).get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                contenido.append(f"\nURL {i}: {item.get('url', 'N/A')}")
                contenido.append(f" - Maliciosas: {stats.get('malicious', 0)}")
                contenido.append(f" - Sospechosas: {stats.get('suspicious', 0)}")
                contenido.append(f" - Inofensivas: {stats.get('harmless', 0)}")
            
            # Sección AbuseIPDB
            contenido.append("\n\n" + "═"*50)
            contenido.append(" ABUSEIPDB ".center(50))
            contenido.append("═"*50 + "\n")
            
            for i, item in enumerate(datos_abuse, 1):
                datos = item.get('analisis', {}).get('data', {})
                contenido.append(f"\nDominio {i}: {item.get('dominio', 'N/A')}")
                contenido.append(f" - Puntaje Abuso: {datos.get('abuseConfidenceScore', 'N/A')}/100")
                contenido.append(f" - Reportes Totales: {datos.get('totalReports', 'N/A')}")
                contenido.append(f" - ISP: {datos.get('isp', 'N/A')}")
            
            # Resumen
            contenido.append("\n\n" + "═"*50)
            contenido.append(" RESUMEN ".center(50))
            contenido.append("═"*50 + "\n")
            
            maliciosas = sum(1 for item in datos_vt if item.get('analisis', {}).get('data', {}).get('attributes', {}).get('last_analysis_stats', {}).get('malicious', 0) > 0)
            contenido.append(f"\nURLs maliciosas detectadas: {maliciosas}/{len(datos_vt)}")
            contenido.append(f"Dominios sospechosos: {sum(1 for item in datos_abuse if item.get('analisis', {}).get('data', {}).get('abuseConfidenceScore', 0) > 50)}/{len(datos_abuse)}")
            
            return "\n".join(contenido)
            
        except Exception as e:
            raise ValueError(f"Error generando contenido: {str(e)}")
