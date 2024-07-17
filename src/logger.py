import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Configura un logger con un manejador de archivo y un manejador de consola."""
    # Crea un logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Crea un formateador que puede ser usado por ambos manejadores
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Crea un manejador de archivo para registrar los mensajes en un archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Crea un manejador de consola para registrar los mensajes en la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Añade los manejadores al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Configuración del logger
logger = setup_logger('mi_logger', 'mi_log.log')

# Ejemplos de uso del logger
logger.debug('Este es un mensaje de depuración.')
logger.info('Este es un mensaje informativo.')
logger.warning('Este es un mensaje de advertencia.')
logger.error('Este es un mensaje de error.')
logger.critical('Este es un mensaje crítico.')
