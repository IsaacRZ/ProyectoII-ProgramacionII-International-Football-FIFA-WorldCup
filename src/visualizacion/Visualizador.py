# Paquetes utilizados
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
from src.eda import EDA

class Visualizador:
    def __init__(self, DF):
        self._DF = DF
        self._filas = self._DF.df.shape[0]
        self._columnas = self._DF.df.shape[1]

    @property
    def DF(self):
        return self._DF

    @property
    def columnas(self):
        return self._columnas

    @property
    def filas(self):
        return self._filas

    def grafico_diferencia_goles(self):
        invocador = EDA.ProcesadorEDA(self._DF)
        tabla_goles = invocador.diferencia_goles().fillna(0)
        # Invocador sirve para llamar a la clase ProcesadorEDA

        top_negativo = tabla_goles.sort_values(by='Diferencia Goles', ascending=False).tail(5)
        top_positivo = tabla_goles.sort_values(by='Diferencia Goles', ascending=True).tail(5)
        # Se extrae en ambos tail para una mejor representación en el gráfico

        df_tornado = pd.concat([top_negativo, top_positivo]).reset_index(drop=True)
        # Se invierte el orden gracias al "reset_index" para que vaya del puesto 1 al puesto 5

        fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
        y_pos = np.arange(len(df_tornado))
        colores = ['#E74C3C' if x < 0 else '#48A111' for x in df_tornado['Diferencia Goles']]
        barras = ax.barh(y_pos, df_tornado['Diferencia Goles'], color= colores)
        # Posicionamos los 10 países en el lienzo y le damos colores

        ax.axvline(0, color='black', linewidth=1.5, linestyle='-')
        # Línea que divide las barras

        for barra in barras:
            width = barra.get_width()
            if width < 0:
                ax.text(width - 4, barra.get_y() + barra.get_height() / 2, f'{int(width)}',
                        va='center', ha='right', color='black', fontweight='bold')
            else:
                ax.text(width + 4, barra.get_y() + barra.get_height() / 2, f'+{int(width)}',
                        va='center', ha='left', color='black', fontweight='bold')
        # Aquí se asignan etiquetas de los ejes

        ax.set_title('Las 5 Selecciones con Mejores y Peores Diferencias de Goles',
                     fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Diferencia de Goles')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(df_tornado['Selección'], fontsize=10, fontweight='bold')
        # Nombre de las selecciones en el eje y

        limite_max = max(abs(df_tornado['Diferencia Goles'].min()), abs(df_tornado['Diferencia Goles'].max())) + 25
        ax.set_xlim(-limite_max, limite_max)
        # Límite de simetría en los ejes x

        ax.spines[['top', 'right', 'left']].set_visible(False)
        ax.tick_params(left=False)

        return plt.show()

    def goles_por_mundial(self):
        invocador = EDA.ProcesadorEDA(self._DF)
        goles_mundiales = invocador.goles_mundial().sort_values(by = 'Año', ascending = True)

        valores_x = goles_mundiales['Año']
        valores_y = goles_mundiales['Goles Anotados']
        # Se obtienen los valores del eje x y del eje y

        fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')

        ax.plot(valores_x, valores_y, color="#48A111", marker='o', linewidth=2, markersize=6)

        ax.set_title('Goles Marcados en los Mundiales', fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel('Cantidad de Goles', fontsize=11)
        ax.set_xlabel('Edición del Mundial (Año)', fontsize=11)

        for x, y in zip(valores_x, valores_y):
            ax.text(
                x,
                y + 4,
                f'{int(y)}',
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold',
                color='#2C3E50'
            )

        ax.set_xticks(valores_x)
        plt.xticks(rotation=45)

        ax.set_ylim(min(valores_y) - 10, max(valores_y) + 20)
        # Se amplía el rango de límite de altura

        ax.grid(True, linestyle='--', alpha=0.5)
        return plt.show()

    def mejores_cinco_selecciones(self):
        invocador = EDA.ProcesadorEDA(self._DF)
        ranking_completo = invocador.ranking_mundial()
        top5 = ranking_completo.head(5).copy()

        columnas_radar = ['Cantidad de Victorias', 'Cantidad de Empates', 'Cantidad de Derrotas','Goles Anotados','Goles Recibidos', 'Diferencia Goles','Puntos']
        categorias = ['Victorias', 'Empates', 'Derrotas','Gol Anotado','Gol Recibido', 'Dif. Goles','Puntos']
        # Recibe el nombre de las columnas y se les asigna un nombre mas corto

        num_variables = len(categorias)

        angulos = np.linspace(0, 2 * np.pi, num_variables, endpoint=False).tolist()
        # Se calculan los ángulos de cada eje en círculo

        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), layout='constrained')
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=11, fontweight='bold')
        colores = ['#FFBF00', '#F62440', '#9CD5FF', '#2CA02C', '#1B4EF5']
        # Mostrar el nombre de las selecciones y asignarles un color a cada una

        for i, (idx, fila) in enumerate(top5.iterrows()):
            pais = fila['Selección']
            puntos_pais = fila['Puntos']

            # Extraemos los valores de las columnas seleccionadas para el país actual
            valores = fila[columnas_radar].values.tolist()

            valores += valores[:1]
            # Se cierrra el bucle duplicando el valor

            ax.plot(angulos, valores, color=colores[i], linewidth=2, label=f"{pais} ({puntos_pais} pts)")
            # Rellenamos el área con un color translúcido (alpha) para que se solapen elegantemente
            ax.fill(angulos, valores, color=colores[i], alpha=0.15)
            # Se dibuja la línea del país

        ax.set_title('Top 5 Histórico de los Mundiales', fontsize=14, fontweight='bold', pad=20)

        ax.legend(title = 'Puntos Totales',loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10, shadow=True)

        ax.grid(color='#AAAAAA', linestyle='--', linewidth=0.5)
        # Estilo de las líneas de la telaraña

        return plt.show()

