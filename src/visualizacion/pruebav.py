from src.eda import EDA
from src.visualizacion import Visualizador as vl
import ingesta.CargadorDatos as cd

if __name__ == "__main__":
    cargador = cd.CargadorDatos(
        url_source="https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
        raw_path="data/raw",
        processed_path="data/processed",
    )

    # Esta variable ya tiene los datos limpios y listos en memoria
    df_para_eda = cargador.ejecutar()

    # Creación de objeto
    df = vl.Visualizador(df_para_eda)

    print(df.diferencia_goles_positivos())
    print(df.diferencia_goles_negativos())

