# grafico2_xg_xga.py (con más separación en los textos de los ejes)
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("FC Barcelona — Goles esperados (xG) a favor vs en contra (2020–2024)")
# Colores blaugrana
BLUE = "#004d98"
MAROON = "#a50044"
# Archivo CSV
csv_file = "matches_full_LaLiga.csv"
if not os.path.exists(csv_file):
    st.error("No se encontró el archivo 'matches_full_LaLiga.csv'. Ponlo en la misma carpeta y vuelve a ejecutar.")
    st.stop()
# Leer datos
df = pd.read_csv(csv_file)
df.columns = [c.strip() for c in df.columns]
for c in df.select_dtypes(include='object').columns:
    df[c] = df[c].astype(str).str.strip()
# Convertir columnas necesarias
for col in ['xg', 'xga', 'season']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
# Filtrar FC Barcelona
if 'team' not in df.columns:
    st.error("El CSV no tiene la columna 'team'. Revisa el archivo.")
    st.stop()
barca = df[df['team'].str.lower() == 'barcelona']
barca = barca[barca['season'].isin([2020, 2021, 2022, 2023, 2024])]
if barca.empty:
    st.warning("No hay datos del Barcelona entre 2020 y 2024.")
    st.stop()
    
#temporada(promedio)
summary = barca.groupby('season', as_index=False).agg({
    'xg': 'mean',
    'xga': 'mean'
}).rename(columns={'xg': 'Goles esperados a favor (xG)', 'xga': 'Goles esperados en contra (xGA)'})

# Gráfico interactivo con Plotly qlq a ver
fig = px.line(
    summary,
    x='season',
    y=['Goles esperados a favor (xG)', 'Goles esperados en contra (xGA)'],
    markers=True,
    title="Goles esperados a favor vs en contra — FC Barcelona (2020–2024)",
    labels={'value': 'Goles esperados promedio por partido', 'season': 'Temporada (año de inicio)'},
    color_discrete_sequence=[BLUE, MAROON]
)
# Estilo visuales xd
fig.update_layout(
    legend_title_text="Tipo de métrica",
    plot_bgcolor="#f7f9fc",
    paper_bgcolor="#ffffff",
    font=dict(size=14, color=BLUE),
    title_font=dict(size=20, color=BLUE),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(color=BLUE)
    ),
    xaxis=dict(
        title_font=dict(color=BLUE, size=14),
        tickfont=dict(color=BLUE),
        automargin=True,
        title_standoff=20  # 🔹 más espacio entre título y eje X
    ),
    yaxis=dict(
        title_font=dict(color=BLUE, size=14),
        tickfont=dict(color=BLUE),
        automargin=True,
        title_standoff=15  # 🔹 más espacio entre título y eje Y
    )
)
st.plotly_chart(fig, use_container_width=True)
#interpretación
st.markdown("""
**Interpretación:**  
Durante las temporadas **2020 a 2024**, el FC Barcelona ha mantenido una relación positiva entre los *goles esperados a favor (xG)* 
y los *goles esperados en contra (xGA)*.  
El promedio de **xG ronda los 1.8–2.0 goles esperados por partido**, mientras que los **xGA se mantienen cerca de 1.2**, 
lo que refleja una **alta capacidad ofensiva y una defensa sólida**.  
Esta brecha favorable demuestra que, incluso en temporadas menos dominantes, el equipo conserva una estructura defensiva fuerte 
y genera suficientes oportunidades de gol para mantenerse competitivo.
""")
