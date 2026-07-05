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
        # Se utilizan dos ".sum()" para que uno sume los nulos de las columnas y luego el segundo sum  suma todos para un correcto uso en el if
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
        filtro_numerico = self.__DF.select_dtypes(['number']) # Se filtran solo los datos numéricos
        m_correlacion = filtro_numerico.corr()
        print("Matriz de Correlacion")
        return m_correlacion

    # Países con mas goles marcados
    def goles_favor(self):
        goles_local = self.__DF.groupby('home_team')['home_score'].sum()
        goles_visita = self.__DF.groupby('away_team')['away_score'].sum()
        # Los paréntesis cuadrados "[]" permiten acceder a los valores de las columnas, estos son los que se suman
        goles_totales = goles_local.add(goles_visita, fill_value=0)
        goles_totales = goles_totales.sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales)
        goles_totales = goles_totales.astype(int).sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales, columns= ["Goles Anotados"])
        # Se reinician los índices y se indican los nuevos nombres
        resultados = goles_totales.reset_index(name='Goles Anotados')
        resultados.columns = ['Selección', 'Goles Anotados']
        return resultados.head(n=10)

    # Equipos con mas goles recibidos
    def goles_contra(self):
        recibidos_visita = self.__DF.groupby('away_team')['home_score'].sum()
        recibidos_local = self.__DF.groupby('home_team')['away_score'].sum()

        goles_totales = recibidos_local.add(recibidos_visita, fill_value=0)
        goles_totales = goles_totales.sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales)

        goles_totales = goles_totales.astype(int).sort_values(ascending=False)
        resultados = pd.DataFrame(goles_totales, columns= ["Goles Recibidos"])
        resultados = goles_totales.reset_index(name='Goles Recibidos')
        resultados.columns = ['Selección', 'Goles Recibidos']

        return resultados.head(n=10)

    # Equipos con mas victorias
    def victorias(self):
        # El ".size()" cuenta cuántas victorias obtuvo cada equipo
        df_gana_local = self.__DF[self.__DF['home_score'] > self.__DF['away_score']]
        victorias_local = df_gana_local.groupby('home_team').size()
        df_gana_visita = self.__DF[self.__DF['away_score'] > self.__DF['home_score']]
        victorias_visita = df_gana_visita.groupby('away_team').size()
        victorias_totales = victorias_local.add(victorias_visita, fill_value=0)
        # Se convierten en enteros ya que ".add" los convierte en flotantes (float)

        victorias_totales = victorias_totales.astype(int).sort_values(ascending=False)
        resultados = pd.DataFrame(victorias_totales, columns= ["Cantidad de Victorias"])
        resultados = victorias_totales.reset_index(name='Cantidad de Victorias')
        resultados.columns = ['Selección', 'Cantidad de Victorias']

        return resultados.head(n=10)

    # Equipos con mas derrotas
    def derrotas(self):
        df_derrota_local = self.__DF[self.__DF['home_score'] < self.__DF['away_score']]
        derrotas_local = df_derrota_local.groupby('home_team').size()
        df_derrota_visita = self.__DF[self.__DF['away_score'] < self.__DF['home_score']]
        derrotas_visita = df_derrota_visita.groupby('away_team').size()
        derrotas_totales = derrotas_local.add(derrotas_visita, fill_value=0)

        derrotas_totales = derrotas_totales.astype(int).sort_values(ascending=False)
        resultados = pd.DataFrame(derrotas_totales, columns=["Cantidad de Derrotas"])
        resultados = derrotas_totales.reset_index(name='Cantidad de Derrotas')
        resultados.columns = ['Selección', 'Cantidad de Derrotas']

        return resultados.head(n=10)

    # Equipos con mas empates
    def empates(self):
        df_empate_local = self.__DF[self.__DF['home_score'] == self.__DF['away_score']]
        empates_local = df_empate_local.groupby('home_team').size()
        df_empate_visita = self.__DF[self.__DF['away_score'] == self.__DF['home_score']]
        empates_visita = df_empate_visita.groupby('away_team').size()
        empates_totales = empates_local.add(empates_visita, fill_value=0)

        empates_totales = empates_totales.astype(int).sort_values(ascending=False)
        resultados = pd.DataFrame(empates_totales, columns=["Cantidad de Empates"])
        resultados = empates_totales.reset_index(name='Cantidad de Empates')
        resultados.columns = ['Selección', 'Cantidad de Empates']

        return resultados.head(n=10)






