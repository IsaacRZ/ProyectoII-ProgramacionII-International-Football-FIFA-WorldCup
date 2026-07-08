# Paquetes utilizados
import matplotlib.pyplot as plt
import pandas as pd
from fontTools.merge import layout

from src.eda import EDA

class Visualizador:
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
    def diferencia_goles_positivos(self):
        invocador = EDA.ProcesadorEDA(self.__DF)
        invocador = invocador.diferencia_goles()
        # Se invoca la clase "ProcesadorEDA" y la función "diferencia_goles"

        positivo = invocador.sort_values(by= 'Diferencia Goles', ascending=False).head(n = 5)
        # Se obtienen los 5 países con mejor diferencia de goles

        positivo = positivo.fillna(0)
        # En caso de que hayan datos nulos se sustituyen por un 0

        datos_grafico = positivo[['Selección', 'Goles Anotados', 'Goles Recibidos', 'Diferencia Goles']]
        datos_grafico = datos_grafico.set_index('Selección')
        # Se agregan los datos en una variable para el gráfico y se usa 'Selección' como índice

        fig, ax = plt.subplots(layout='constrained')
        datos_grafico.plot(kind='bar', ax=ax, width=0.8, color=['#FFEF5F', '#48A111', '#1C4D8D'])
        # Se agregan los colores para cada barra

        for container in ax.containers:
            ax.bar_label(container, padding=3)
        # Se añaden las etiquetas numéricas encima de cada barra

        ax.set_title('Top 5 Países con Mejor Diferencia de Goles en Mundiales')
        ax.set_ylabel('Cantidad de Goles')
        ax.legend(loc='upper right', ncol=3)
        ax.set_ylim(0, 300)
        plt.xticks(rotation=0)

        return plt.show()

    def diferencia_goles_negativos(self):
        invocador = EDA.ProcesadorEDA(self.__DF)
        invocador = invocador.diferencia_goles()
        # Se invoca la clase "ProcesadorEDA" y la función "diferencia_goles"

        negativo = invocador.sort_values(by= 'Diferencia Goles', ascending=True).head(n=5)
        # Se obtienen los 5 países con mejor diferencia de goles

        negativo = negativo.fillna(0)
        # En caso de que no hayan datos nulos se sustituyen por un 0

        datos_grafico = negativo[['Selección', 'Goles Anotados', 'Goles Recibidos', 'Diferencia Goles']]
        datos_grafico = datos_grafico.set_index('Selección')
        # Se agregan los datos en una variable para el gráfico y se usa 'Selección' como índice

        fig, ax = plt.subplots(layout='constrained')
        datos_grafico.plot(kind='bar', ax=ax, width=0.8, color=['#F0E9C2', '#021A54', '#A82323'])
        # Se agregan los colores para cada barra

        ax.axhline(0, color='black', linewidth=1.2, linestyle='-')
        # Línea que divide los valores positivos y negativos

        for container in ax.containers:
            ax.bar_label(container, padding=3, labels=[f'{int(v):}' if v != 0 else '' for v in container.datavalues])
        # Las etiquetas se vuelven dinámicas, si posee valores negativos estos se van abajo

        ax.set_title('Top 5 Países con Peor Diferencia de Goles en Mundiales')
        ax.set_ylabel('Cantidad de Goles')
        ax.legend(loc='upper right', ncol=3)
        ax.set_ylim(-80, 150)
        plt.xticks(rotation=0)

        return plt.show()
