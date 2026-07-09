import logging
from pathlib import Path
from io import StringIO

import requests
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CargadorDatos:
    def __init__(self, url_source: str, raw_path: str, processed_path: str):
        self.url_source = url_source
        self.raw_path = Path(raw_path)
        self.processed_path = Path(processed_path)
        self.raw_path.mkdir(parents = True, exist_ok = True)
        self.processed_path.mkdir(parents = True, exist_ok = True)
        
    def descargar(self, forzar: bool = False) -> pd.DataFrame:
        ruta_cache = self.raw_path / "raw_results.csv"
        
        if ruta_cache.exists and not forzar:
            logger.info(f"Usando cache local: {ruta_cache}")
            return pd.read_csv(ruta_cache, index_col='id')

        logger.info(f"Descargando CSV desde {self.url_source}")
        response = requests.get(self.url_source, timeout=30)
        response.raise_for_status() # Check HTTP response error exc 404, 500, etc.

        df = pd.read_csv(StringIO(response.text))
        logger.info(f"Descarga completa, dimension de: {df.shape[0]} filas y {df.shape[1]} columnas")
        return df
    
    def filtrar_mundial(self, df: pd.DataFrame) -> pd.DataFrame:
        df_mundial = df[df["tournament"] == "FIFA World Cup"].copy()
        logger.info(f"Filtro aplicado para 'FIFA World Cup': {df_mundial.shape[0]} filas")
        return df_mundial
    
    def validar(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("DataFrame filtrado está vacío. ")
        
        columnas_esperadas = {'date', 'home_team', 'away_team', 'home_score', 'away_score'}
        columnas_faltantes = columnas_esperadas - set(df.columns)
        if columnas_faltantes:
            raise ValueError(f"Faltan columnas esperadas: {columnas_faltantes}")

        nulos = df[['home_score', 'away_score']].isna().sum().sum()     # Subconjunto de datos: 2 columnas [[]] 
        if nulos > 0:
            logger.warning(f"Se encontraron {nulos} valores nulos en marcadores")

        return df
    
    def enriquecer(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['clave_partido'] = (
            df['date'].astype(str) + '_' +
            df['home_team'] + '_' +
            df['away_team']
        )
        return df
            

    def guardar(self, df_raw: pd.DataFrame, df_processed: pd.DataFrame):
        """
        Nota: Por especificación del proyecto el archivo raw y processed se almacenan en la ruta: 'data/raw'
        processed_path queda reservado para uso posterior
        """
        raw_file_path = self.raw_path / "raw_results.csv"
        processed_file_path = self.raw_path / "partidos-mundial.csv"

        df_raw.to_csv(raw_file_path, index=True, index_label="id")
        df_processed.to_csv(processed_file_path, index=True, index_label="id")

        logger.info(f"Guardado raw en: {raw_file_path}")
        logger.info(f"Guardado processed en: {processed_file_path}")
    
    def ejecutar(self):
        df_raw = self.descargar()
        df_processed = self.filtrar_mundial(df_raw)
        df_enriched = self.enriquecer(df_processed)
        df_valid = self.validar(df_enriched)
        self.guardar(df_raw, df_valid)
        return df_valid