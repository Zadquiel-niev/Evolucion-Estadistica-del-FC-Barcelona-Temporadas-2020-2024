import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Evolución FC Barcelona (2020-2024)", layout="wide")
st.title("Evolución Estadística — FC Barcelona (2020–2024)")
st.markdown("Dashboard interactivo — gráficos corregidos y validados (posesión, xG, formaciones, resultados).")

#limpiezaaa

CSV = "matches_full_LaLiga.csv"
if not os.path.exists(CSV):
    st.error(f"No encontré '{CSV}' en la carpeta del proyecto. Pon el archivo y vuelve a ejecutar.")
    st.stop()
    
df = pd.read_csv(CSV)
# normalizar nombres
df.columns = [c.strip() for c in df.columns]

team_col = None
for c in df.columns:
    try:
        if df[c].astype(str).str.lower().str.contains("barcelona", na=False).any():
            team_col = c
            break
    except Exception:
        continue

if team_col:
    barca = df[df[team_col].astype(str).str.lower().str.contains("barcelona", na=False)].copy()
else:
    
    barca = df.copy()
    st.info("No se detectó una columna con 'Barcelona'; asumiendo que el CSV contiene solo partidos del Barça.")

cols_lower = {c: c.lower() for c in barca.columns}
def find_col(variants):
    for v in variants:
        for c in barca.columns:
            if v.lower() in c.lower():
                return c
    return None

col_poss = find_col(['poss', 'possession', 'pos'])
col_xg = find_col(['xg', 'expected goals', 'expected'])
col_xga = find_col(['xga', 'xga', 'expected against', 'expected goals against'])
col_gf = find_col(['gf','goals for','goles a favor'])
col_ga = find_col(['ga','goals against','goles en contra'])
col_season = find_col(['season','year'])
col_result = find_col(['result','res'])
col_formation = find_col(['formation','formacion','form'])

def to_numeric_clean(series):
    s = series.astype(str).str.replace('%','').str.replace(',','.', regex=False).str.strip()
    return pd.to_numeric(s, errors='coerce')

if col_poss:
    barca[col_poss] = to_numeric_clean(barca[col_poss])
    
    mean_poss = barca[col_poss].dropna().mean() if not barca[col_poss].dropna().empty else np.nan
    if not np.isnan(mean_poss) and mean_poss <= 1.0:
        barca[col_poss] = barca[col_poss] * 100
        
if col_xg:
    barca[col_xg] = to_numeric_clean(barca[col_xg])
if col_xga:
    barca[col_xga] = to_numeric_clean(barca[col_xga])
if col_season:
    barca[col_season] = pd.to_numeric(barca[col_season], errors='coerce')

# filtrar temporadas 2020-2024
if col_season:
    if barca[col_season].notna().any():
        barca = barca[barca[col_season].between(2020, 2024)]
    else:
        st.warning("La columna de 'season' existe pero no es numérica; no se filtró por temporada.")
        
# Validaciones y autocorrecciones
if col_poss:
    mean_poss = barca[col_poss].dropna().mean()
    if np.isnan(mean_poss):
        st.warning("No hay valores válidos en posesión (poss). Revisa el CSV.")
    else:
        if mean_poss < 40 or mean_poss > 80:
            if col_xg and col_xga:
                mxg = barca[col_xg].dropna().mean() if not barca[col_xg].dropna().empty else np.nan
    mxga = barca[col_xga].dropna().mean() if not barca[col_xga].dropna().empty else np.nan
    if not np.isnan(mxg) and not np.isnan(mxga):
        if mxg + 0.15 < mxga:

            tmp = barca[col_xg].copy()
            barca[col_xg] = barca[col_xga]
            barca[col_xga] = tmp
            # recalc means
            mxg = barca[col_xg].dropna().mean()
            mxga = barca[col_xga].dropna().mean()
st.markdown("---")

#GRAFICO 1: Posesión por temporada
st.header("Gráfico 1 — Posesión promedio por temporada")
if not col_poss or not col_season:
    st.warning("No hay columnas 'poss' y/o 'season' detectadas correctamente para este gráfico.")
else:
    s1 = barca.groupby(col_season, as_index=False)[col_poss].mean().rename(columns={col_poss:'Posesión promedio (%)', col_season:'season'}).sort_values('season')
    fig1 = px.line(s1, x='season', y='Posesión promedio (%)', markers=True,
                   title="Evolución de la posesión promedio (%) por temporada")
    fig1.update_traces(line_color="#004d98", marker_color="#004d98")
    
    if not s1['Posesión promedio (%)'].isna().all():
        ymin = max(0, min(30, s1['Posesión promedio (%)'].min() - 2))
        ymax = max(100, s1['Posesión promedio (%)'].max() + 2)

        if s1['Posesión promedio (%)'].between(40,80).any():
            fig1.update_yaxes(range=[min(35, s1['Posesión promedio (%)'].min()-2), max(80, s1['Posesión promedio (%)'].max()+2)])
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("**Interpretación:** Valores expresados en % de posesión. Se han normalizado entradas como '66' o '0.66' a porcentajes.")
st.markdown("---")

#GRAFICO 2: xG vs xGA por temporada
st.header("Gráfico 2 — xG (a favor) vs xGA (en contra) por temporada")
if not col_xg or not col_xga or not col_season:
    st.warning("Faltan columnas para xG/xGA o season.")
else:
    s2 = barca.groupby(col_season, as_index=False).agg({col_xg:'mean', col_xga:'mean'}).rename(columns={col_xg:'xg', col_xga:'xga', col_season:'season'}).sort_values('season')
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=s2['season'], y=s2['xg'], mode='lines+markers', name='xG (a favor)', line=dict(color='#004d98')))
    fig2.add_trace(go.Scatter(x=s2['season'], y=s2['xga'], mode='lines+markers', name='xGA (en contra)', line=dict(color='#a50044')))
    fig2.update_layout(title="xG vs xGA — Promedio por temporada", xaxis_title="Temporada", yaxis_title="Goles esperados promedio")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("**Interpretación:** xG (azul) = oportunidades creadas; xGA (granate) = oportunidades concedidas. Si ves que xG está muy bajo (<0.6), revisa fuentes de datos (puede ser formato decimal/coma).")
st.markdown("---")

#GRAFICO 3: Posesión vs xG (scatter + tendencia)
st.header("Gráfico 3 — Posesión (%) vs Goles esperados (xG) — partidos")
if not col_poss or not col_xg:
    st.warning("Faltan columnas 'poss' o 'xg' para este gráfico.")
else:
    scatter = barca.dropna(subset=[col_poss, col_xg]).copy()
    scatter = scatter.rename(columns={col_poss:'poss', col_xg:'xg'})
    if scatter.empty:
        st.warning("No hay datos válidos de poss/xg para graficar.")
    else:
        fig3 = px.scatter(scatter, x='poss', y='xg', labels={'poss':'Posesión (%)','xg':'Goles esperados (xG)'}, title="Posesión vs xG (por partido)")
        # añadir línea de tendencia
        if len(scatter) > 1:
            m,b = np.polyfit(scatter['poss'].values, scatter['xg'].values, 1)
            xs = np.linspace(scatter['poss'].min(), scatter['poss'].max(), 100)
            fig3.add_trace(go.Scatter(x=xs, y=m*xs+b, mode='lines', name='Tendencia', line=dict(color='red', width=2)))
        # fijar rango X si es plausible
        if scatter['poss'].between(30,80).any():
            fig3.update_xaxes(range=[max(20, scatter['poss'].min()-2), min(100, scatter['poss'].max()+2)])
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Interpretación:** Cada punto = partido. La línea indica la tendencia entre posesión y xG. Se normalizó posesión a % si venía en fracción.")
st.markdown("---")

#GRAFICO 4: Puntos promedio por formación
st.header("Gráfico 4 — Promedio de puntos por formación (manteniendo tu cálculo)")
if not (col_gf and col_ga and col_formation):
    st.warning("Faltan columnas para calcular puntos por formación (gf/ga/formation).")
else:
    df4 = barca.copy()
    df4[col_gf] = pd.to_numeric(df4[col_gf], errors='coerce')
    df4[col_ga] = pd.to_numeric(df4[col_ga], errors='coerce')

    df4['puntos'] = df4.apply(lambda r: 3 if r[col_gf] > r[col_ga] else (1 if r[col_gf] == r[col_ga] else 0), axis=1)
    form_mean = df4.groupby(col_formation, as_index=False)['puntos'].mean().rename(columns={'puntos':'Puntos promedio'}).sort_values('Puntos promedio', ascending=False)
    if len(form_mean) > 25:
        form_mean = form_mean.head(25)
    fig4 = px.bar(form_mean, x=col_formation, y='Puntos promedio', title="Promedio de puntos por formación (2020–2024)")
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)
    mejor = form_mean.iloc[0][col_formation] if not form_mean.empty else None
    peor = form_mean.iloc[-1][col_formation] if not form_mean.empty else None
    st.markdown(f"**Interpretación:** La formación con mayor promedio de puntos: **{mejor}**. La menor: **{peor}**.")

st.markdown("---")

#GRAFICO 5: Resultados por temporada (W/D/L agrupadas)
st.header("Gráfico 5 — Resultados por temporada (Ganados / Empatados / Perdidos)")
if not col_result or not col_season:
    st.warning("No hay columna 'result' o 'season' detectada.")
else:
    df5 = barca.copy()
    df5[col_result] = df5[col_result].astype(str).str.strip().str.upper()
    # pivot
    pivot = df5.pivot_table(index=col_season, columns=col_result, values=df5.columns[0], aggfunc='count', fill_value=0)
    for c in ['W','D','L']:
        if c not in pivot.columns:
            pivot[c] = 0
    pivot = pivot[['W','D','L']].sort_index()
    df5_long = pivot.reset_index().melt(id_vars=col_season, value_vars=['W','D','L'], var_name='Resultado', value_name='Cantidad')
    
    # etiquetas y colores 
    label_map = {'W':'Perdidos (L)', 'D':'Empatados (D)', 'L':'Ganados (W)'}
    df5_long['Etiqueta'] = df5_long['Resultado'].map(label_map)
    colors = {'Ganados (W)':'#004d98', 'Empatados (D)':'#ffcc00', 'Perdidos (L)':'#a50044'}
    fig5 = px.bar(df5_long, x=col_season, y='Cantidad', color='Etiqueta', barmode='group',
                  title="Resultados por temporada — Ganados / Empatados / Perdidos")
    fig5.update_layout(legend_title_text='Resultado')
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("**Interpretación:** Comparación clara de victorias, empates y derrotas por temporada.")
