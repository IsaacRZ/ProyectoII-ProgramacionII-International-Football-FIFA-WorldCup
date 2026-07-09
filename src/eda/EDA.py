# Llamado de librerías
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path.cwd().parent / "src"))

from ingesta.CargadorDatos import CargadorDatos
from gestor.GestorPartidos import GestorPartidos

# Definición de la clase
class ProcesadorEDA:
    def __init__(self, gestor: GestorPartidos):
        self._gestor = gestor
        self._df = gestor.df
        self._filas = self._df.shape[0]
        self._columnas = self._df.shape[1]

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()

    @property
    def columnas(self) -> int:
        return self._columnas

    @property
    def filas(self) -> int:
        return self._filas

    """
    # En duda si dejarlo o no
    # Vista de primeros 15 elementos
    def primerosDatos(self):
        pd.set_option('display.max_rows', self.__columnas)
        return print(self._df.head(n = 15))

    # Vista de últimos 15 elementos
    def ultimososDatos(self):
        pd.set_option('display.max_rows', self.__columnas)
        return print(self._df.tail(n = 15))
    """

    # Matriz de Correlación
    def correlacion(self):
        filtro_numerico = self._df.select_dtypes(['number']) # Se filtran solo los datos numéricos
        m_correlacion = filtro_numerico.corr()
        print("Matriz de Correlacion")
        return m_correlacion


    # Países con mas goles marcados
    def goles_favor(self):
        goles_local = self._df.groupby('home_team')['home_score'].sum()
        goles_visita = self._df.groupby('away_team')['away_score'].sum()
        # Los paréntesis cuadrados "[]" permiten acceder a los valores de las columnas, estos son los que se suman

        goles_totales = goles_local.add(goles_visita, fill_value=0)
        goles_totales = goles_totales.astype(int).sort_values(ascending=False)
        # Se suman los goles y se transforman en enteros para mejor legibilidad

        resultados = goles_totales.reset_index(name='Goles Anotados')
        resultados.columns = ['Selección', 'Goles Anotados']
        # Se reinician los índices para agregar nuevos y se sustituye "index" por "Selección"

        return resultados


    # Equipos con mas goles recibidos
    def goles_contra(self):
        recibidos_visita = self._df.groupby('away_team')['home_score'].sum()
        recibidos_local = self._df.groupby('home_team')['away_score'].sum()
        # Se comparan los goles con los equipos en este caso los contrarios (gol visita al equipo local y viceversa)

        goles_totales = recibidos_local.add(recibidos_visita, fill_value=0)
        goles_totales = goles_totales.sort_values(ascending=False)
        goles_totales = goles_totales.astype(int).sort_values(ascending=False)
        # Se suman los goles y se transforman en enteros para mejor legibilidad

        resultados = goles_totales.reset_index(name='Goles Recibidos')
        resultados.columns = ['Selección', 'Goles Recibidos']
        # Se reinician los índices para agregar nuevos y se sustituye "index" por "Selección"

        return resultados


    def diferencia_goles(self):
        goles_favor = self.goles_favor()
        goles_contra = self.goles_contra()
        # Llama la función anteriormente creadas y los guarda en una variable

        goles_favor = pd.DataFrame(goles_favor).sort_values(by='Selección', ascending=False)
        goles_contra = pd.DataFrame(goles_contra).sort_values(by='Selección', ascending=False)
        # Se agregan ambas tablas y se ordenan por orden alfabético

        tabla_goles = pd.merge(goles_favor, goles_contra, on='Selección', how='outer')
        tabla_goles = tabla_goles.fillna(0)
        tabla_goles['Diferencia Goles'] = tabla_goles['Goles Anotados'] - tabla_goles['Goles Recibidos']
        # Se realiza la resto entre ambas tablas de goles para obtener la diferencia de gol

        columnas_num = ['Goles Anotados', 'Goles Recibidos', 'Diferencia Goles']
        tabla_goles[columnas_num] = tabla_goles[columnas_num].astype(int)
        tabla_goles = tabla_goles.sort_values(by='Diferencia Goles', ascending=False)
        # Las columnas se cambian a numéricas para mejor legibilidad

        return tabla_goles


    # Equipos con mas victorias
    def victorias(self):
        df_gana_local = self._df[self._df['home_score'] > self._df['away_score']]
        # El ".size()" cuenta cuántas victorias obtuvo cada equipo
        victorias_local = df_gana_local.groupby('home_team').size()
        df_gana_visita = self._df[self._df['away_score'] > self._df['home_score']]
        # Compara los goles de visita y local y si son diferentes los guarda en una variable

        victorias_visita = df_gana_visita.groupby('away_team').size()
        victorias_totales = victorias_local.add(victorias_visita, fill_value=0)
        victorias_totales = victorias_totales.astype(int).sort_values(ascending=False)
        # Se convierten en enteros ya que ".add" los convierte en flotantes (float)
        # Se suman las victorias locales y visitantes y se transforman en enteros ya que no requieren decimales

        resultados = pd.DataFrame(victorias_totales, columns= ["Cantidad de Victorias"])
        resultados = victorias_totales.reset_index(name='Cantidad de Victorias')
        resultados.columns = ['Selección', 'Cantidad de Victorias']

        return resultados


    # Equipos con mas derrotas
    def derrotas(self):
        df_derrota_local = self._df[self._df['home_score'] < self._df['away_score']]
        derrotas_local = df_derrota_local.groupby('home_team').size()
        df_derrota_visita = self._df[self._df['away_score'] < self._df['home_score']]
        # Compara los goles de visita y local y si son diferentes los guarda en una variable

        derrotas_visita = df_derrota_visita.groupby('away_team').size()
        derrotas_totales = derrotas_local.add(derrotas_visita, fill_value=0)
        derrotas_totales = derrotas_totales.astype(int).sort_values(ascending=False)
        # Se suman las derrotas locales y visitantes y se transforman en enteros ya que no requieren decimales

        resultados = pd.DataFrame(derrotas_totales, columns=["Cantidad de Derrotas"])
        resultados = derrotas_totales.reset_index(name='Cantidad de Derrotas')
        resultados.columns = ['Selección', 'Cantidad de Derrotas']

        return resultados


    # Equipos con mas empates
    def empates(self):
        df_empate_local = self._df[self._df['home_score'] == self._df['away_score']]
        empates_local = df_empate_local.groupby('home_team').size()
        df_empate_visita = self._df[self._df['away_score'] == self._df['home_score']]
        # Compara los goles de visita y local y si son iguales los guarda en una variable

        empates_visita = df_empate_visita.groupby('away_team').size()
        empates_totales = empates_local.add(empates_visita, fill_value=0)
        empates_totales = empates_totales.astype(int).sort_values(ascending=False)
        # Se suman los empates locales y visitantes y se transforman en enteros ya que no requieren decimales

        resultados = pd.DataFrame(empates_totales, columns=["Cantidad de Empates"])
        resultados = empates_totales.reset_index(name='Cantidad de Empates')
        resultados.columns = ['Selección', 'Cantidad de Empates']
        # Se resetean los índices y se agrega junto a la selección correspondiente

        return resultados


    # Mundial con mas goles
    def mas_gol_mundial(self):
        sede = self._df.copy()
        sede['Año'] = sede['date'].dt.year
        # "lambda" realiza la función de devolver los años con mas de una sede en un mismo lugar
        sede['Sede'] = sede.groupby('Año')['country'].transform(lambda x: ' / '.join(sorted(x.unique())))
        # Esto permite evitar usar una función aparte, ya que "lambda" funciona como un operario temporal

        goles_totales = sede.groupby(['Sede', 'Año'])[['home_score', 'away_score']].sum()
        goles_totales['Goles Anotados'] = goles_totales['home_score'] + goles_totales['away_score']
        goles_ordenados = goles_totales['Goles Anotados'].astype(int).sort_values(ascending=False)
        # Se suman los goles de los equipos locales y visitantes y se agrupan a los mundiales correspondientes

        resultados = goles_ordenados.reset_index(name='Goles Anotados')
        resultados.columns = ['Sede(s)', 'Año', 'Goles Anotados']
        # Se resetean los índices y se agrega el nuevo "Goles Anotados" junto a la sede y al año

        return resultados.head(n = 11)


    # Mundial con menos goles
    def menos_gol_mundial(self):
        sede = self._df.copy()
        sede['Año'] = sede['date'].dt.year
        sede['Sede'] = sede.groupby('Año')['country'].transform(lambda x: ' / '.join(sorted(x.unique())))
        # Se filtra la sede y en caso de ser varias se pone como una misma gracias a "lambda"

        goles_totales = sede.groupby(['Sede', 'Año'])[['home_score', 'away_score']].sum()
        goles_totales['Goles Anotados'] = goles_totales['home_score'] + goles_totales['away_score']
        goles_ordenados = goles_totales['Goles Anotados'].astype(int).sort_values(ascending=True)
        # Se suman los goles de los equipos locales y visitantes y se agrupan a los mundiales correspondientes

        resultados = goles_ordenados.reset_index(name='Goles Anotados')
        resultados.columns = ['Sede(s)', 'Año', 'Goles Anotados']
        # Se resetean los índices y se agrega el nuevo "Goles Anotados" junto a la sede y al año

        return resultados.head(n = 11)


    # País que mas veces a sido sede, año en que fue y equipo campeón
    def veces_sede(self):
        sede = self._df.copy()
        sede['Año'] = sede['date'].dt.year
        indices_finales = sede.groupby('Año')['date'].idxmax()

        # Se filtra el dataset para buscar el último partido disputado (razón por la que se excluye 2026)
        finales = sede.loc[indices_finales].copy()
        finales = finales[finales['Año'] != 2026]

        # Función para obtener el campeón según los goles del último partido, gracias a finales
        def obtener_campeon(fila):
            if fila['home_score'] > fila['away_score']:
                return fila['home_team']
            else:
                return fila['away_team']

        finales['Campeón'] = finales.apply(obtener_campeon, axis=1)
        diccionario_campeones = finales.set_index('Año')['Campeón'].to_dict()
        sedes_unicas = sede[['Año', 'country']].drop_duplicates()

        # El campeón es agregado al año correspondiente
        sedes_unicas['Campeón'] = sedes_unicas['Año'].map(diccionario_campeones)

        # 2026 se deja nulo y se cambia por "Por Definir" para evitar conflictos de inserción con ".join"
        sedes_unicas['Campeón'] = sedes_unicas['Campeón'].fillna('Por Definir')

        # Se agrupan los datos que se van a mostrar
        resultados = sedes_unicas.groupby('country').agg(
            Veces_Sede=('Año', 'count'),
            # Si no dice "Por Definir" este agregua al campeón, así evitamos un campeón en 2026
            Campeones_Sede=('Campeón', lambda x: ', '.join([c for c in x.unique() if c != 'Por Definir'])),
            # Se transforma en str para que no de error
            Anho_Sede=('Año', lambda x: ', '.join(sorted(x.unique().astype(str))))
        ).reset_index()

        # Se cambia el orden de las tablas para mayor legibilidad
        resultados.columns = ['País Sede', 'Veces Sede', 'Campeón(es) Coronado(s)', 'Año(s)']
        resultados = resultados.sort_values(by='Veces Sede', ascending=False)

        return resultados


    def ranking_mundial(self):
        diferencia_goles = self.diferencia_goles()
        victorias = self.victorias()
        derrotas = self.derrotas()
        empates = self.empates()
        # Llaman las funciones necesarias para trabajar

        ranking = pd.merge(victorias, empates, on='Selección', how='outer') \
                     .merge(derrotas, on='Selección', how='outer') \
                     .merge(diferencia_goles, on='Selección', how='outer')

        ranking = ranking.fillna(0)
        ranking['Puntos'] = (ranking['Cantidad de Victorias'] * 3) + (ranking['Cantidad de Empates'] * 1)
        enteros = ['Cantidad de Victorias', 'Cantidad de Derrotas', 'Cantidad de Empates',
                   'Goles Anotados', 'Goles Recibidos', 'Diferencia Goles', 'Puntos']
        ranking[enteros] = ranking[enteros].astype(int)
        ranking = ranking.sort_values(by='Puntos', ascending=False)
        ranking = ranking.reset_index(drop=True)

        return ranking