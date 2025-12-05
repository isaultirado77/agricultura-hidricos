# load.py

from pathlib import Path
from datetime import datetime
import logging

import duckdb

from scripts.config import PROCESSED_DIR, setup_logger


# logger
logger = logging.getLogger(__name__)

# paths
DB_PATH = PROCESSED_DIR / "sonora.duckdb"


def connect_db(): 
    """Establece conexión a la base DuckDB"""
    try: 
        logger.info(f'Conectando a la base de datos: {DB_PATH}')
        con = duckdb.connect(f'{DB_PATH}')
        return con
    except Exception:
        logger.exception('Error conectando a DuckDB')
        raise


def load_file(con, file):
    """
    Carga un archivo individual al DuckDB.
    Crea la tabla si no existe. 
    Inserta datos si ya existe. 
    """
    try: 
        # Considera todos como varchar
        source = (
            f"read_csv_auto('{file.as_posix()}', "
            f"all_varchar=True, sample_size=-1)"
        )
        
        actual_table = file.stem

        # Crear tabla si no existe
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {actual_table} AS
            SELECT * FROM {source} LIMIT 0;
            """
        )
        
        # Insertar datos
        con.execute(
            f"""
            INSERT INTO {actual_table}
            SELECT * FROM {source};
            """
        )
        
        logger.info(f'Archivo cargado correctamente: {file}')
    
    except Exception:
        logger.exception(f'Error cargando el archivo: {file}')


def load_dataset(con, dataset_name, dataset_path): 
    """Carga todos los archivos de un dataset específico."""
    logger.info(f'Iniciando carga del dataset: {dataset_name}')

    if not dataset_path.exists(): 
        logger.warning(f'No existe el directorio del dataset: {dataset_path}')
        return
    
    for file in dataset_path.iterdir(): 
        if file.is_file(): 
            load_file(con, file)

    logger.info(f'Dataset cargado: {dataset_name}')


def load_all():
    """
    Punto de entrada principal del script.
    Recorre todas las carpetas dentro de PROCESSED_DIR.
    Carga todo automáticamente.
    """
    logger.info('Iniciando proceso de LOAD...')
    start = datetime.now()

    con = connect_db()

    try: 
        for dataset_dir in PROCESSED_DIR.iterdir(): 
            if dataset_dir.is_dir(): 
                load_dataset(con, dataset_dir.name, dataset_dir)
        
        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f'LOAD finalizado en {elapsed:.2f} s')

    except Exception:
        logger.exception('Fallo en el proceso de LOAD')
        raise


if __name__ == '__main__': 
    logger = setup_logger()
    load_all()
