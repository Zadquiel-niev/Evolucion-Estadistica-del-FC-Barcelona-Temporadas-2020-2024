import streamlit as st
import utils
import plotly.express as px
import scipy.stats as stats

st.set_page_config(
    page_title="Graficos Interactivos - FC Barcelona",
    layout="wide"
)

st.markdown('<div class="section-header">Graficos Interactivos</div>', unsafe_allow_html=True)

# Cargar datos
df = utils.load_and_clean_data()
if df.empty:
    st.error("No se pudieron cargar los datos")
    st.stop()

barca_data = utils.filter_barcelona_data(df)

if barca_data.empty:
    st.error("No se encontraron datos del FC Barcelona")
    st.stop()

# Preparar datos
barca_data, cols = utils.prepare_barcelona_data(barca_data)

# Gráfico 1: Evolución de la Posesión
st.subheader("1. Evolución de la Posesión por Temporada")
st.markdown("**Análisis de la evolución del promedio de posesión del FC Barcelona**")

if 'season' in cols and 'poss' in cols:
    possession_data = barca_data.groupby(cols['season'])[cols['poss']].mean().reset_index()
    possession_data.columns = ['temporada', 'posesion_promedio']

    fig = utils.px.line(
        possession_data,
        x='temporada',
        y='posesion_promedio',
        title="Evolución de la posesión promedio (FC Barcelona 2020-2024)",
        markers=True
    )
    fig.update_layout(yaxis_range=[50, 75])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretación:** Entre las temporadas **2020 y 2024**, el FC Barcelona ha mostrado una **tendencia descendente en la posesión promedio del balón**,
    pasando de cerca del **66-67% a alrededor del 64%** por partido. Este descenso refleja una **pérdida parcial del estilo de juego histórico del club**,
    basado en la **filosofía del Tiki Taka** y el control constante del balón. No obstante, a pesar de esta disminución, el equipo **mantiene uno de los promedios
    de posesión más altos de LaLiga**, lo que evidencia que su identidad táctica aún conserva raíces en el dominio del balón.
    """)

st.markdown("---")

# Gráfico 2: xG vs xGA
st.subheader("2. Goles Esperados (xG) vs Goles Esperados en Contra (xGA)")
st.markdown("**Comparación entre goles esperados a favor y en contra**")

if 'season' in cols and 'xg' in cols and 'xga' in cols:
    xg_data = barca_data.groupby(cols['season']).agg({
        cols['xg']: 'mean',
        cols['xga']: 'mean'
    }).reset_index()

    xg_data.columns = ['temporada', 'xg_promedio', 'xga_promedio']

    fig = utils.go.Figure()
    fig.add_trace(utils.go.Scatter(
        x=xg_data['temporada'], y=xg_data['xg_promedio'],
        mode='lines+markers', name='xG (a favor)',
        line=dict(color=utils.BLUE, width=3)
    ))
    fig.add_trace(utils.go.Scatter(
        x=xg_data['temporada'], y=xg_data['xga_promedio'],
        mode='lines+markers', name='xGA (en contra)',
        line=dict(color=utils.MAROON, width=3)
    ))

    fig.update_layout(
        title="Goles esperados a favor (xG) vs en contra (xGA) - FC Barcelona (2020-2024)",
        yaxis_range=[0.5, 2.5]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretación:** Durante las temporadas **2020 a 2024**, el FC Barcelona ha mantenido una relación positiva entre los _goles esperados a favor (xG)_
    y los _goles esperados en contra (xGA)._ El promedio de **xG ronda los 1.8-2.0 goles esperados por partido**, mientras que los **xGA se mantienen cerca de 1.2**,
    lo que refleja una **alta capacidad ofensiva y una defensa sólida**. Esta brecha favorable demuestra que, incluso en temporadas menos dominantes,
    el equipo conserva una estructura defensiva fuerte y genera suficientes oportunidades de gol para mantenerse competitivo.
    """)

st.markdown("---")

# Gráfico 3: Posesion vs xG
st.subheader("3. Relación entre Posesión y Oportunidades de Gol")
st.markdown("**Correlación entre posesión y goles esperados (xG)**")

if 'poss' in cols and 'xg' in cols:
    try:
        fig = utils.px.scatter(
            barca_data,
            x=cols['poss'],
            y=cols['xg'],
            title="Barcelona: Posesión vs xG (2020-2024)",
            labels={cols['poss']: 'Posesión (%)', cols['xg']: 'Goles Esperados (xG)'},
            trendline="ols"
        )
    except Exception as e:
        st.warning(f"No se pudo generar la línea de tendencia: {e}")
        fig = utils.px.scatter(
            barca_data,
            x=cols['poss'],
            y=cols['xg'],
            title="Barcelona: Posesión vs xG (2020-2024)",
            labels={cols['poss']: 'Posesión (%)', cols['xg']: 'Goles Esperados (xG)'}
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretación:** Como podemos notar no hay tanta correlación. Es decir, entre más posesión del balón tiene el Barcelona tiene más chance de gol,
    o sea, tiene más oportunidad de gol sí, pero no es una regla. No es seguro que entre más posesión del balón, seguro va a tener más goles.
    No va a tener más chance, no es seguro como podemos observarlo. Depende probablemente del partido, depende de los jugadores que estén en cancha,
    depende de muchas cosas, pero hay una correlación. Sí baja, sí, pero la hay. Entonces podemos decir que entre más posesión tiene el Fútbol Club Barcelona
    el balón, se podría decir que tiene un poquito más oportunidades de gol, no 100% más pero sí algo.
    """)

st.markdown("---")

# Gráfico 4: Formaciones - VERSIÓN FINAL SIMPLIFICADA
st.subheader("4. Efectividad por Formación Táctica")
st.markdown("**Puntos promedio obtenidos por cada formación**")

if 'formation' in barca_data.columns and 'gf' in cols and 'ga' in cols:
    # Calcular puntos
    barca_data['puntos'] = barca_data.apply(
        lambda x: 3 if x[cols['gf']] > x[cols['ga']] else (1 if x[cols['gf']] == x[cols['ga']] else 0),
        axis=1
    )
    barca_filtrado = barca_data[~barca_data['formation'].astype(str).str.startswith('200')].copy()

    formacion_stats = barca_filtrado.groupby('formation').agg({
        'puntos': ['mean', 'count']
    })

    # Reestructurar el DataFrame
    formacion_stats.columns = ['puntos_promedio', 'partidos']
    formacion_stats = formacion_stats.reset_index()

    # Ordenar por puntos promedio (de mayor a menor)
    formacion_stats = formacion_stats.sort_values('puntos_promedio', ascending=False)

    # Crear grafico de barras interactivo
    fig = utils.px.bar(
        formacion_stats,
        x='formation',
        y='puntos_promedio',
        title="FC Barcelona - Promedio de puntos por formación (2020-2024)",
        labels={'formation': 'Formación', 'puntos_promedio': 'Puntos promedio por partido'},
        color='puntos_promedio',
        color_continuous_scale=[utils.MAROON, utils.BLUE],
        hover_data=['partidos']
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        yaxis=dict(range=[0, 3])
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "Formación: %{x}",
            "Puntos promedio: %{y:.2f}",
            "Partidos: %{customdata[0]}",
            "<extra></extra>"
        ])
    )

    st.plotly_chart(fig, use_container_width=True)

    # Encontrar la mejor y peor formacion
    mejor = formacion_stats.iloc[0]
    peor = formacion_stats.iloc[-1]

    st.markdown(f"""
    **Interpretación:**

    - **Formación más efectiva**: **'{mejor['formation']}'** con **{mejor['puntos_promedio']:.2f} puntos** por partido ({mejor['partidos']} partidos)
    - **Formación menos efectiva**: **'{peor['formation']}'** con **{peor['puntos_promedio']:.2f} puntos** por partido ({peor['partidos']} partidos)

    **Análisis:**
    La táctica influye significativamente en el rendimiento del equipo. Las formaciones con mejor promedio de puntos
    suelen ser aquellas que mejor se adaptan al estilo de juego del Barcelona y a las características de los jugadores disponibles.
    La formación **4-3-3**, tradicional del club, generalmente muestra buenos resultados, pero es importante considerar
    el contexto de cada partido (rival, localía, estado del equipo).
    """)

st.markdown("---")

# Gráfico 5: Resultados por Temporada
st.subheader("5. Resultados por Temporada")
st.markdown("**Distribución de victorias, empates y derrotas por temporada**")

if 'season' in cols and 'result' in cols:
    resultados_data = []

    for temporada in sorted(barca_data[cols['season']].unique()):
        temp_data = barca_data[barca_data[cols['season']] == temporada]

        victorias = len(temp_data[temp_data[cols['result']] == 'W'])
        empates = len(temp_data[temp_data[cols['result']] == 'D'])
        derrotas = len(temp_data[temp_data[cols['result']] == 'L'])

        resultados_data.append({
            'temporada': temporada,
            'Victorias': victorias,
            'Empates': empates,
            'Derrotas': derrotas
        })

    df_resultados = utils.pd.DataFrame(resultados_data)

    fig = utils.go.Figure()

    # Añadir barras para cada tipo de resultado
    fig.add_trace(utils.go.Bar(
        name='Victorias',
        x=df_resultados['temporada'],
        y=df_resultados['Victorias'],
        marker_color=utils.BLUE,
        text=df_resultados['Victorias'],
        textposition='auto'
    ))
    fig.add_trace(utils.go.Bar(
        name='Empates',
        x=df_resultados['temporada'],
        y=df_resultados['Empates'],
        marker_color=utils.YELLOW,
        text=df_resultados['Empates'],
        textposition='auto'
    ))
    fig.add_trace(utils.go.Bar(
        name='Derrotas',
        x=df_resultados['temporada'],
        y=df_resultados['Derrotas'],
        marker_color=utils.MAROON,
        text=df_resultados['Derrotas'],
        textposition='auto'
    ))

    fig.update_layout(
        barmode='group',
        title="Resultados del FC Barcelona por temporada (2020-2024)",
        xaxis_title="Temporada",
        yaxis_title="Cantidad de Partidos",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretación:** El gráfico muestra la cantidad de partidos ganados, empatados y perdidos por temporada (2020-2024).
    Se observa una mejora progresiva en los resultados con aumento de victorias y reducción de derrotas en las temporadas más recientes,
    lo cual confirma la recuperación competitiva del equipo tras las temporadas más complicadas. La temporada 2023 muestra el mejor balance,
    indicando una efectividad creciente del proyecto deportivo.
    """)

st.markdown("---")
st.markdown("**Metodología: Análisis basado en datos de LaLiga 2020-2024**")
st.caption("Analisis Estadistico FC Barcelona | Graficos Interactivos")
