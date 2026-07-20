# Eliminar - Remover raw_results.csv
#from pathlib import Path
#
#ruta_corrupta = Path("../data/raw/raw_results.csv")
#ruta_corrupta.unlink()  # elimina el archivo dañado
#print("Archivo corrupto eliminado.")

## LIMPIAR raw_results.csv
#import pandas as pd
#
#df_sucio = pd.read_csv("../data/raw/raw_results.csv")
#df_limpio = df_sucio[['date', 'home_team', 'away_team', 'home_score', 'away_score',
#                       'tournament', 'city', 'country', 'neutral']].copy()
#df_limpio.to_csv("../data/raw/raw_results.csv", index=True, index_label='id')