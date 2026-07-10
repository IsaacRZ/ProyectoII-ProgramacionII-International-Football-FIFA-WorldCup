import sys
from pathlib import Path

import pandas as pd
import numpy as np
import EDA
import ingesta.CargadorDatos as cd

sys.path.append(str(Path.cwd().parent / "src"))

from ingesta.CargadorDatos import CargadorDatos
from gestor.GestorPartidos import GestorPartidos

# Invocar último código de "CargadorDatos para llamar al archivo
if __name__ == "__main__":
    cargador = cd.CargadorDatos(
    url_source="https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
    raw_path="../data/raw",
    processed_path="../data/processed",
    )

    # Esta variable ya tiene los datos limpios y listos en memoria
    df_para_eda = cargador.ejecutar()

    # Creación de objeto
    df = EDA.ProcesadorEDA(df_para_eda)


    # Verificación de que el objeto haya cargado correctamente
    print(df.columnas)
    print(df.filas)
    # print(df.primerosDatos())
    # print(df.ultimososDatos())
    print(df.correlacion())
    print(df.goles_favor())
    print(df.goles_contra())
    print(df.diferencia_goles())
    print(df.victorias())
    print(df.derrotas())
    print(df.empates())
    print(df.mas_gol_mundial())
    print(df.menos_gol_mundial())
    print(df.veces_sede())
    print(df.ranking_mundial())