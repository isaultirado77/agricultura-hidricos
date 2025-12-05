# extract.py

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse, unquote
import logging
import zipfile

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from scripts.config import RAW_DIR, setup_logger


# logger
logger = logging.getLogger(__name__)

# paths
agricultura_dir = RAW_DIR / "agricultura"
agricultura_dir.mkdir(exist_ok=True)

hidricos_dir = RAW_DIR / "hidricos"
hidricos_dir.mkdir(exist_ok=True)

mpios_dir = RAW_DIR / "mpios"
mpios_dir.mkdir(exist_ok=True)

# urls
agricultura_url= r"https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora"
hidricos_url = r"https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos"
municipios_url = r"https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173/26_sonora.zip" 


def get_download_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all("a", class_="resource-url-analytics")

    return [a.get('href') for a in atags if a]


def download_file(url, dest_dir, chunk_size=5*1024*1024):
    """
    Descarga un archivo desde una URL mostrando una barra de progreso con tqdm.
    """
    if not url.startswith("http"):
        logger.warning(f"URL inválida ignorada: {url}")
        return None

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()

            total_size = int(r.headers.get('content-length', 0))

            parsed = urlparse(url)
            filename = Path(unquote(parsed.path)).name
            file_path = dest_dir / filename
            
            with open(file_path, 'wb') as f, tqdm(
                total=total_size if total_size > 0 else None,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=file_path.name
            ) as bar:
                
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
        
        return file_path

    except Exception as e:
        logger.exception(f'Error al descargar: {e}')
        raise


def download_files_concurrently(urls, dest_dir, max_workers=5):
    """
    Descarga archivos de una lista de URLs de forma concurrente usando ThreadPoolExecutor.
    """
    downloaded_files = []

    dest_dir.mkdir(parents=True, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_file, url, dest_dir)
            for url in urls
        ]
        
        for future in futures:
            result = future.result()
            if result:
                downloaded_files.append(result)

    return downloaded_files


def unzip_file(zip_path, output_path=None):
    if not output_path:
        output_path = zip_path.parent / zip_path.stem

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(path=output_path)
        return output_path

    except zipfile.BadZipFile:
        logger.exception(f'ZIP corrupto: {zip_path}')
        raise


def extract_data():
    start = datetime.now()
    logger.info("Iniciando extracción de datos...")
    try:
        agricultura_urls = get_download_urls(agricultura_url)
        agricultura_path = download_files_concurrently(agricultura_urls, agricultura_dir)
        
        hidricos_urls = get_download_urls(hidricos_url)
        hidricos_path = download_files_concurrently(hidricos_urls, hidricos_dir)

        mpios_zip = download_file(municipios_url, mpios_dir)
        mpios_path = unzip_file(mpios_zip, )

        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f'Extracción completada en {elapsed:.2f} s')
        
        return {
            'agricultura': agricultura_path, 
            'hidricos': hidricos_path, 
            'mpios': mpios_path
        }

    except Exception:
        logger.exception("Fallo durante la extracción")


if __name__ == '__main__':
    logger = setup_logger()
    extract_data()
