import logging
import os

def configurar_log():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logs/procesamiento.log'
    )
    return logging.getLogger(__name__)

def leer_urls(archivo_entrada):
    logger = configurar_log()
    try:
        if not os.path.exists(archivo_entrada):
            raise FileNotFoundError(f"Archivo no encontrado: {archivo_entrada}")

        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
