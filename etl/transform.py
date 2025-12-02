# transform.py

import warnings
from datetime import datetime
import logging

import pandas as pd
import geopandas as gpd

from scripts.config import RAW_DIR, PROCESSED_DIR, setup_logger

# configs
warnings.filterwarnings('ignore')

# logger
logger = logging.getLogger(__name__)

# paths
agricultura_dir = RAW_DIR / "agricultura"
hidricos_dir = RAW_DIR / "hidricos"
mpios_dir = RAW_DIR / "mpios"

agricultura_processed_dir = PROCESSED_DIR / "agricultura"
agricultura_processed_dir.mkdir(exist_ok=True)

hidricos_processed_dir = PROCESSED_DIR / "hidricos"
hidricos_processed_dir.mkdir(exist_ok=True)

mpios_processed_dir = PROCESSED_DIR / "mpios"
mpios_processed_dir.mkdir(exist_ok=True)

# auxliars
AGR_COLUMNS_MAP = {
    "ano": "anio",
    "cierreyavan": "tipo_registro",            # cierre / avance
    "ciclo": "ciclo_productivo",
    "cddr": "clave_ddr",
    "nddr": "distrito_ddr",
    "cmun": "clave_municipio",
    "nmun": "municipio",
    "cvecul": "clave_cultivo",
    "cultivo": "cultivo",
    "supsem": "superficie_sembrada_ha",
    "supcose": "superficie_cosechada_ha",
    "supsini": "superficie_siniestrada_ha",
    "prodton": "produccion_ton",
    "rendmnto": "rendimiento_ton_ha",
    "pmr": "precio_medio_rural",
    "valprod": "valor_produccion_miles_mxn"
}


def normalize_str(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.lower()
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    return df


def df_todict(df: pd.DataFrame, col1: str, col2: str) -> dict:
    return df.set_index(col1)[col2].to_dict()


def transform_agricultura_data(): 
    filename_template = "agricultura-sonora-*.xlsx"

    data_paths = list(agricultura_dir.glob(filename_template))

    if not data_paths: 
        logger.warning(f'No se encontraron datos en {agricultura_dir /filename_template}')
        return
    
    dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)

    agriculutra = pd.concat(dfs)
    agriculutra = normalize_str(agriculutra)
    agriculutra = agriculutra.rename(columns=AGR_COLUMNS_MAP)
    agriculutra['distrito_ddr'] = agriculutra['distrito_ddr'].str.replace('ddr ', '')

    # Guardamos datos
    file_path = agricultura_processed_dir / "agricultura_processed.csv"
    agriculutra.to_csv(file_path)

    logger.info(f'Datos de agricultura procesados en: {file_path}')

    return file_path


def transform_presas_data(): 
    catalogo_path = hidricos_dir / "catalogo.xlsx"
    presas = pd.read_excel(catalogo_path, sheet_name='Catálogo_estatal')

    presas = normalize_str(presas)

    file_path = hidricos_processed_dir / "presas_processed.csv"
    presas.to_csv(file_path)
    logger.info(f'Datos de presas procesados en: {file_path}')

    return file_path


def transform_hidricos_data():
    filename_template = "hidrico_sonora_*.xlsx"

    data_paths = list(hidricos_dir.glob(filename_template))
    dfs = list(pd.read_excel(path, sheet_name='Hoja1') for path in data_paths)
    hidricos = pd.concat(dfs)

    hidricos.columns = ['clave', 'fecha', 'almacenamiento_hm3']
    hidricos['clave'] = hidricos.clave.str.lower()

    file_path = hidricos_processed_dir / "hidricos_processed.csv"
    hidricos.to_csv(file_path)
    logger.info(f'Datos de hídricos procesados en: {file_path}')
    
    return file_path


def transform_mpios_data(): 
    mpios_shp = mpios_dir / "26_sonora" / "conjunto_de_datos" / "26mun.shp"
    gdf = gpd.read_file(mpios_shp)
    
    gdf.columns = gdf.columns.str.lower()
    gdf['nomgeo'] = gdf['nomgeo'].str.lower()
    gdf = gdf.drop(columns='cve_ent')

    file_path  = mpios_processed_dir / "mpios_processed.geojson"
    gdf.to_file(file_path, driver='GeoJSON')
    logger.info(f'Datos de georreferenciados procesados en: {file_path}')
    
    return file_path


def transform_data(): 
    start = datetime.now()
    logger.info("Iniciando transformación de datos...")
    
    try: 
        agricultura_path = transform_agricultura_data()
        hidtricos_path = transform_hidricos_data()
        presas_path = transform_presas_data()
        mpios_path = transform_mpios_data()

        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f'Transformación completada en {elapsed:.2f} s')
        return {
            'agricultura': agricultura_path,
            'hidricos': hidtricos_path, 
            'presas': presas_path, 
            'mpios': mpios_path, 
            }

    except Exception as e:
        logger.exception(f"Fallo durante la extracción: {e}")
    


def main():
    transform_data()

if __name__ == '__main__':
    logger = setup_logger()
    main()
    