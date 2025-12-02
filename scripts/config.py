# config.py

import sys
from pathlib import Path

from loguru import logger

# dirs
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INTERIM_DIR = BASE_DIR / "interim"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "log"

DIRS = [DATA_DIR, RAW_DIR, INTERIM_DIR, PROCESSED_DIR, LOG_DIR]


def setup_logger(log_dir=LOG_DIR): 
    log_dir.mkdir(exist_ok=True)
    logger.remove()

    # Formato estándar para consola y archivos
    LOG_FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss} | {level} | "
        "{file}:{function}:{line} | {message}"
    )

    # Consola
    logger.add(
        sys.stderr,
        level="INFO",
        format=LOG_FORMAT
    )

    # Archivo INFO
    logger.add(
        log_dir / "info.log",
        rotation="10 MB",
        retention="15 days",
        compression="zip",
        level="INFO",
        format=LOG_FORMAT,
    )

    # Archivo ERROR
    logger.add(
        log_dir / "errors.log",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        level="ERROR",
        format=LOG_FORMAT + " | {exception}",
    )

    return logger
