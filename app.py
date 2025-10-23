import streamlit as st

st.set_page_config(
    page_title="Análisis FC Barcelona 2020-2024",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        color: #004D98;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #004D98;
        border-bottom: 2px solid #A50044;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚽ ANÁLISIS ESTADÍSTICO FC BARCELONA (2020-2024)</div>', unsafe_allow_html=True)

st.markdown("""
### Autores: Jose Aguirre y Zadquiel Nieves

Esta aplicación presenta un análisis completo del rendimiento del FC Barcelona durante las temporadas 2020-2024.

**Características principales:**
- Análisis de tendencias ofensivas y defensivas
- Evaluación de posesión y efectividad
- Comparación de rendimiento por localía
- Análisis de formaciones tácticas
- Visualizaciones interactivas

**Metodología:**
- Fuente de datos: matches_full_la_liga.csv
- Período analizado: Temporadas 2020-2024
- Tecnologías: Python, Pandas, Plotly, Streamlit

### Cómo usar esta aplicación

Utiliza la barra lateral para navegar entre las diferentes secciones del análisis.
""")

st.markdown("---")

# Métricas rápidas en la página principal
try:
    import utils
    df = utils.load_and_clean_data()
    if not df.empty:
        barca_data = utils.filter_barcelona_data(df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_partidos = len(barca_data)
            st.metric("Partidos Analizados", total_partidos)

        with col2:
            temporadas = barca_data['season'].nunique()
            st.metric("Temporadas", temporadas)

        with col3:
            posesion_promedio = barca_data['poss'].mean()
            st.metric("Posesión Promedio", f"{posesion_promedio:.1f}%")

        with col4:
            goles_promedio = barca_data['gf'].mean()
            st.metric("Goles/Partido", f"{goles_promedio:.2f}")

except Exception as e:
    st.info("Cargando datos...")

st.markdown("---")
st.caption("Análisis Estadístico FC Barcelona | 2020-2024")
