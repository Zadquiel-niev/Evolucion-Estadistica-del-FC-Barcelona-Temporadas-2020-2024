import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv = "matches_full_LaLiga.csv"
if not os.path.exists(csv):
    raise SystemExit("Coloca 'matches_full_LaLiga.csv' en la misma carpeta.")

# leer columnas xd
df = pd.read_csv(csv)
df.columns = [c.strip().lower() for c in df.columns]
if 'season' not in df.columns or 'result' not in df.columns:
    raise SystemExit("El CSV necesita tener al menos las columnas 'season' y 'result'.")

# detectar columna que contenga 'barcelona'
team_col = None
for c in df.columns:
    try:
        if df[c].astype(str).str.lower().str.contains('barcelona', na=False).any():
            team_col = c
            break
    except Exception:
        continue
if team_col:
    df_barca = df[df[team_col].astype(str).str.lower().str.contains('barcelona', na=False)].copy()
else:
    df_barca = df.copy()
    
# filtrar 
df_barca = df_barca[df_barca['season'].between(2020, 2024)]
df_barca['result'] = df_barca['result'].astype(str).str.strip().str.upper()

#conteo W/D/L por temporada
pivot = df_barca.pivot_table(index='season', columns='result', values='date', aggfunc='count', fill_value=0)
#orden W, D, L
for col in ['W', 'D', 'L']:
    if col not in pivot.columns:
        pivot[col] = 0
pivot = pivot[['W', 'D', 'L']].sort_index()

#(W = Ganados, D = Empatados, L = Perdidos)
seasons = list(pivot.index)
x = np.arange(len(seasons))
width = 0.25
colors = {'W':'#004d98', 'D':'#ffcc00', 'L':'#a50044'}
fig, ax = plt.subplots(figsize=(9,5))
ax.bar(x - width, pivot['L'].values, width=width, label='Ganados (W)', color=colors['L'])
ax.bar(x        , pivot['D'].values, width=width, label='Empatados (D)', color=colors['D'])
ax.bar(x + width, pivot['W'].values, width=width, label='Perdidos (L)', color=colors['W'])
ax.set_title("Resultados del FC Barcelona por temporada (2020–2024)")
ax.set_xlabel("Temporada")
ax.set_ylabel("Cantidad de partidos")
ax.set_xticks(x)
ax.set_xticklabels(seasons)
ax.legend()
plt.tight_layout()
plt.savefig("results_by_season_barcelona.png", dpi=200)
plt.show()

# Interpretación 
print("Interpretación:")
print("El gráfico muestra la cantidad de partidos ganados, empatados y perdidos por temporada (2020–2024).")
print("Se espera ver un aumento de victorias y una reducción de derrotas en las temporadas recientes,")
print("lo cual confirmaría la recuperación del equipo tras las temporadas más complicadas.")