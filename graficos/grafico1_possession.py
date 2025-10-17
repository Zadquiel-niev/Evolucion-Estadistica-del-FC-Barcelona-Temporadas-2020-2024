import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Configuración general 
st.set_page_config(page_title="Gráfico 1 — Posesión por temporada", layout="centered")
st.title("📊 FC Barcelona — Promedio de posesión por temporada (2020–2024)")

#Cargar CSV
csv_path = "matches_full_LaLiga.csv"
if not os.path.exists(csv_path):
    st.error(f"No se encontró el archivo `{csv_path}` en el directorio del proyecto.")
    st.stop()

df = pd.read_csv(csv_path)

# Limpieza 
df.columns = [c.strip() for c in df.columns]
for c in df.select_dtypes(include='object').columns:
    df[c] = df[c].astype(str).str.strip()

for c in ['poss', 'season']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

#Filtrando datos de Barcelona y temporadas 2020-2024
barca = df[df['team'].str.lower() == 'barcelona']
barca = barca[barca['season'].isin([2020, 2021, 2022, 2023, 2024])]

#Temporadas Agrupadas
summary = (
    barca.groupby('season', as_index=False)['poss']
    .mean()
    .rename(columns={'poss': 'Posesión promedio (%)'})
)
#Grafico
fig = px.line(
    summary,
    x='season', y='Posesión promedio (%)',
    markers=True,
    title="Evolución de la posesión promedio por temporada (FC Barcelona 2020–2024)",
    labels={'season': 'Temporada (año de inicio)', 'Posesión promedio (%)': 'Posesión promedio (%)'}
)
fig.update_traces(line_color="#004d98", marker_color="#004c98")

st.plotly_chart(fig, use_container_width=True, key="grafico1")

#Descripción e interpretación
st.markdown("""
**Interpretación:**  
Entre las temporadas **2020 y 2024**, el FC Barcelona ha mostrado una **tendencia descendente en la posesión promedio del balón**, 
pasando de cerca del **66–67%** a alrededor del **64%** por partido.  
Este descenso refleja una **pérdida parcial del estilo de juego histórico del club**, basado en la **filosofía del *Tiki Taka*** y el control constante del balón.  
No obstante, a pesar de esta disminución, el equipo **mantiene uno de los promedios de posesión más altos de LaLiga**, 
lo que evidencia que su identidad táctica aún conserva raíces en el dominio del balón.
""")
