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
        mask = (self._df['home_team'] == equipo) | (self._df['away_team'] == equipo)
        return self._df[mask].copy() 

    def get_por_anio(self, anio: int) -> pd.DataFrame:
        resultado = self._df['date'].dt.year == anio
        return self._df[resultado].copy()

    def get_por_sede(self, pais: str) -> pd.DataFrame:
        resultado = self._df['country'] == pais
        return self._df[resultado].copy()

    def ventaja_local(self) -> dict:
        partidos_no_neutrales = (
            self._df[self._df['neutral'] == False]       # Exclusión de neutral == False (verdadera ventaja local) 
            .dropna(subset=['home_score', 'away_score'])
            .copy()
            )         
        ganados_local = (partidos_no_neutrales['home_score'] > partidos_no_neutrales['away_score']).sum()
        perdidos_local = (partidos_no_neutrales['home_score'] < partidos_no_neutrales['away_score']).sum()
        empates = (partidos_no_neutrales['home_score'] == partidos_no_neutrales['away_score']).sum()
        total = partidos_no_neutrales.shape[0]
        porcentaje = round(ganados_local / total * 100, 2)
        porcentaje_perdida = round(perdidos_local / total * 100, 2)
        porcentaje_empates = round(empates / total * 100, 2)
        columnas_relevantes = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'city', 'country']

        return {
            'porcentaje_victorias_local': porcentaje,
            'porcentaje_perdidas_local': porcentaje_perdida,
            'porcentaje_empates_local': porcentaje_empates,
            'total_partidos_local': int(total),
            'detalle': partidos_no_neutrales[columnas_relevantes].copy(),
        }

    def promedio_goles_por_partido(self) -> float:
        partidos_validos = self._df.dropna(subset=['home_score', 'away_score']).copy()
        goles_totales = partidos_validos['home_score'] + partidos_validos['away_score']
        return round(goles_totales.mean(), 2)
    
    def partido_mas_goles_por_partido(self) -> dict:
        partidos_validos = self._df.dropna(subset=['home_score', 'away_score']).copy()
        partidos_validos['total_score'] = partidos_validos['home_score'] + partidos_validos['away_score']
        idmax = partidos_validos['total_score'].idxmax()
        return partidos_validos.loc[idmax].to_dict()
    
    def get_por_equipo(self, equipo: str) -> pd.DataFrame:
        partidos =  self.get_por_equipo(equipo)
        

