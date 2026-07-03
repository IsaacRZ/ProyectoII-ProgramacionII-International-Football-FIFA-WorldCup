import pandas as pd

class GestorPartidos:
    """
    Gestor partidos es una clase de consulta o vista para lectura del dataset.

    """
    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()
    
    def get_partido_por_id(self, id_partido: int) -> dict | None:
        if id_partido not in self._df.index:
            return None
        return self._df.loc[id_partido].to_dict()

    def get_partido(self, clave_partido: str) -> dict | None:
        resultado = self._df[self._df['clave_partido'] == clave_partido]
        if resultado.empty:
            return None
        return resultado.iloc[0].to_dict()
    

    def get_por_equipo(self, equipo: str):
        mask = (['home_team'] == equipo) | (['away_team'] == equipo)
        return self._df[mask].copy() 

    def get_por_anio(self, anio):
        ...

    def get_por_sede(self, pais):
        ...

    def ventaja_local(self):
        ...   
    
