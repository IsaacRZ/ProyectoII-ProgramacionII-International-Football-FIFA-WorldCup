from src.eda import EDA
from src.visualizacion import Visualizador as vl
from src.ingesta.CargadorDatos import CargadorDatos as cd
from src.gestor.GestorPartidos import GestorPartidos as gp


cargador = cd.CargadorDatos(
    url_source="https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
    raw_path="data/raw",
    processed_path="data/processed"
)

df_para_eda = cargador.ejecutar()

gestor = GestorPartidos(df_para_eda)

df = EDA.ProcesadorEDA(gestor)

print(df.columnas)
print(df.filas)
print(df.primerosDatos())
print(df.ultimososDatos())
print(df.outliers())
    #print(df.correlacion())
    #print(df.goles_favor())
    #print(df.goles_contra())
    #print(df.diferencia_goles())
    #print(df.victorias())
    #print(df.derrotas())
    #print(df.empates())
    #print(df.mas_gol_mundial())
    #print(df.menos_gol_mundial())
    #print(df.veces_sede())
    #print(df.ranking_mundial())