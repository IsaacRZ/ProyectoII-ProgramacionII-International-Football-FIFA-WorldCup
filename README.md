# Proyecto-II Programacion II International Football FIFA WorldCup

### Integrantes:
###  Isaac Rodriguez Zuñiga
###  Sebastian Calvo

# Descripción General del Proyecto

### Dataset

El dataset utilizado es: https://github.com/martj42/international_results el cual se filtra por la columna 'tournament' para copiar en un nuevo dataframe unicamente los partidos con la descripción 'Fifa World Cup'

### Contenido del dataset: Columnas - Variables importantes
Columnas y sus tipos de datos:

| # | Column | Non-Null Count | Dtype | Descripción |
| --- | --- | --- | --- | --- |
| - | id | 119 non-null | bool | id original del raw_results.csv |
| 0 | date | 119 non-null | datetime64[us] | fecha del partido (YYYY-MM-DD) |
| 1 | home_team | 119 non-null | str | equipo local |
| 2 | away_team | 119 non-null | str | equipo visitante |
| 3 | home_score | 118 non-null | float64 | goles del equipo local |
| 4 | away_score | 118 non-null | float64 | goles del equipo visitante |
| 5 | tournament | 119 non-null | str | torneo (filtrar por "FIFA World Cup") |
| 6 | city | 119 non-null | str | ciudad sede del partido |
| 7 | country | 119 non-null | str | país sede del partido |
| 8 | neutral | 119 non-null | bool | indica si el partido se jugó en cancha neutral (True/False) |
| 9 | clave_partido | 119 non-null | str | Clave especifica del partido (date_hometeam_awayteam) |

# Conda 

1. Crear: ´conda env create -f env.yml´
2. Activar: ´conda activate FifaWc´ 
3. Desactivar ´conda deactivate´

