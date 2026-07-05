# Llamado de librerías
import pandas as pd


# Definición de la clase
class ProcesadorEDA:
    def __init__(self, DF):
        self.__DF = DF
        self.__filas = DF.shape[0]
        self.__columnas = DF.shape[1]

    @property
    def DF(self):
        return self.__DF

    @property
    def columnas(self):
        return self.__columnas

    @property
    def filas(self):
        return self.__filas

    # Verifica el tipo de dato que posee las columnas (int, char, boolean, etc)
    def verificadorDatos(self):
        return print(self.__DF.info())

    # Obtención de nombres de las columnas
    def nombreColumnas(self):
        return print(self.__DF.columns)

    """
    # En duda si dejarlo o no
    # Vista de primeros 15 elementos
    def primerosDatos(self):
        pd.set_option('display.max_rows', self.__columnas)
        return print(self.__DF.head(n = 15))

    # Vista de últimos 15 elementos
    def ultimososDatos(self):
        pd.set_option('display.max_rows', self.__columnas)
        return print(self.__DF.tail(n = 15))
    """

    # Cambia los datos a formato fecha (date)
    def tipoFecha(self):
        if self.__DF.columns[0] == 'date':
            self.__DF['date'] = pd.to_datetime(self.__DF['date'])
            return print(self.__DF.info())

    # Revisión de Nulos
    def nulos(self):
        revision_nulos = self.__DF.isnull().sum().sum()
        if revision_nulos > 0:
            print("Hay elementos nulos")
            filas_con_nulos = self.__DF[self.__DF.isnull().any(axis=1)]
            return filas_con_nulos
        else:
            print("No hay elementos nulos")
            return False

    # Eliminación de Nulos
    def dropNulos(self):
        self.__DF = self.__DF.dropna()
        revision_nulos = self.__DF.isnull().sum().sum()
        if revision_nulos > 0:
            return True
        else:
            print("No hay elementos nulos")
            return False

    # Matriz de Correlación
    def correlacion(self):
        filtro_numerico = self.__DF.select_dtypes(['number'])
        m_correlacion = filtro_numerico.corr()
        print("Matriz de Correlacion")
        return m_correlacion

    # Países con mas goles marcados
    def goles_favor(self):
        goles_local = self.__DF.groupby('home_team')['home_score'].sum()
        goles_visita = self.__DF.groupby('away_team')['away_score'].sum()
        goles_totales = goles_local.add(goles_visita, fill_value=0)
        goles_totales = goles_totales.sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales)
        return resultados.head(n = 10)

    # Equipos con mas goles recibidos
    def goles_contra(self):
        recibidos_visita = self.__DF.groupby('away_team')['home_score'].sum()
        recibidos_local = self.__DF.groupby('home_team')['away_score'].sum()
        goles_totales = recibidos_local.add(recibidos_visita, fill_value=0)
        goles_totales = goles_totales.sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales)
        return resultados.head(n = 10)




