from src.eda import EDA
from src.visualizacion import Visualizador as vl
from src.ingesta import CargadorDatos as cd
from gestor.GestorPartidos import GestorPartidos


cargador = cd.CargadorDatos(
    url_source="https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
    raw_path="data/raw",
    processed_path="data/processed"
)

df_para_eda = cargador.ejecutar()

gestor = GestorPartidos(df_para_eda)

df = vl.Visualizador(gestor)


df.grafico_diferencia_goles()
df.goles_por_mundial()
df.mejores_cinco_selecciones()
df.campeon_sede_otro()
df.subcampeones()
