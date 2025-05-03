"""
Módulo AbuseIPDB - Versión 4.1 (Corrección de datos vacíos)
"""

import requests
import json
import os
from urllib.parse import urlparse
from datetime import datetime
import logging

def configurar_log():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logs/abuseipdb.log'
    )
    return logging.getLogger(__name__)

class AnalizadorAbuseIPDB:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2/check"
        self.headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }
        self.logger = configurar_log()
        os.makedirs('salidas', exist_ok=True)

    def analizar_urls(self, archivo_urls):
        """Versión corregida con mejor manejo de respuestas"""
        try:
            # Verificación más estricta del archivo de entrada
            if not os.path.exists(archivo_urls):
                raise FileNotFoundError(f"Archivo {archivo_urls} no encontrado")
            
            with open(archivo_urls, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and line.startswith('http')]
            
            if not urls:
                raise ValueError("El archivo no contiene URLs válidas")

            resultados = []
            for url in urls[:5]:  # Analizar solo las primeras 5 URLs
                try:
                    dominio = self._extraer_dominio(url)
                    if not dominio:
                        continue
                    
                    params = {
                        "ipAddress": dominio,
                        "maxAgeInDays": "90",
                        "verbose": True
                    }
                    
                    response = requests.get(
                        self.base_url,
                        headers=self.headers,
                        params=params,
                        timeout=10
                    )
                    
                    # Verificación más completa de la respuesta
                    if response.status_code != 200:
                        raise ValueError(f"Código de estado: {response.status_code}")
                        
                    data = response.json()
                    
                    if not isinstance(data, dict) or 'data' not in data:
                        raise ValueError("Formato de respuesta inválido")
                    
                    # Validar datos mínimos requeridos
                    if not all(k in data['data'] for k in ['abuseConfidenceScore', 'totalReports']):
                        raise ValueError("Faltan campos esenciales en la respuesta")
                    
                    resultados.append({
                        "url": url,
                        "dominio": dominio,
                        "analisis": data
                    })
                    self.logger.info(f"Dominio analizado: {dominio} - Puntaje: {data['data']['abuseConfidenceScore']}")
                    
                except Exception as e:
                    self.logger.warning(f"Error analizando {url}: {str(e)}")
                    continue

            if not resultados:
                raise ValueError("No se pudo analizar ninguna URL")
            
            return self._guardar_resultados(resultados)

        except Exception as e:
            self.logger.error(f"Error en análisis: {str(e)}")
            raise

    def _extraer_dominio(self, url):
        """Extracción de dominio más robusta"""
        try:
            # Eliminar protocolo y rutas
            dominio = url.split('//')[-1].split('/')[0]
            # Eliminar puerto si existe
            dominio = dominio.split(':')[0]
            # Validar dominio básico
            if '.' not in dominio or len(dominio) < 4:
                raise ValueError("Dominio no válido")
            return dominio
        except Exception as e:
            self.logger.warning(f"Error extrayendo dominio de {url}: {str(e)}")
            return None

    def _guardar_resultados(self, resultados):
        """Guardado con verificación de datos"""
        try:
            if not resultados:
                raise ValueError("No hay datos para guardar")
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_salida = f"salidas/abuseipdb_{timestamp}.json"
            
            with open(archivo_salida, 'w') as f:
                json.dump(resultados, f, indent=4, ensure_ascii=False)
            
            # Verificar que el archivo no esté vacío
            if os.path.getsize(archivo_salida) == 0:
                raise ValueError("El archivo de resultados está vacío")
            
            return archivo_salida
            
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {str(e)}")
            raise