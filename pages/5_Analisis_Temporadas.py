import streamlit as st
import utils
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Analisis por Temporadas")
st.markdown("---")


# Cargar datos
df = utils.load_and_clean_data()
if df.empty:
    st.error("No se pudieron cargar los datos")
    st.stop()

barca_data = utils.filter_barcelona_data(df)

if barca_data.empty:
    st.error("No se encontraron datos del FC Barcelona")
    st.stop()

# Preparar datos para analisis
barca_data, cols = utils.prepare_barcelona_data(barca_data)

# Calcular metricas por temporada
if 'season' in cols and 'gf' in cols and 'ga' in cols and 'poss' in cols:
    season_col = cols['season']
    gf_col = cols['gf']
    ga_col = cols['ga']
    poss_col = cols['poss']

    # Tabla de rendimiento general
    st.subheader("Rendimiento General por Temporada")

    rendimiento = barca_data.groupby(season_col).agg({
        gf_col: ['count', 'sum', 'mean'],
        ga_col: ['sum', 'mean'],
        'result': lambda x: (x == 'W').sum()
    }).round(2)

    # Reestructurar el DataFrame
    rendimiento.columns = ['Partidos', 'GF_Total', 'GF_Promedio', 'GC_Total', 'GC_Promedio', 'Victorias']
    rendimiento = rendimiento.reset_index()

    # Calcular metricas adicionales
    rendimiento['Empates'] = rendimiento['Partidos'] - rendimiento['Victorias'] - (rendimiento['Partidos'] - rendimiento['Victorias'] - (rendimiento['GF_Total'] - rendimiento['GC_Total']) / 3)
    rendimiento['Derrotas'] = rendimiento['Partidos'] - rendimiento['Victorias'] - rendimiento['Empates']
    rendimiento['Puntos'] = (rendimiento['Victorias'] * 3) + rendimiento['Empates']
    rendimiento['Efectividad'] = (rendimiento['Puntos'] / (rendimiento['Partidos'] * 3) * 100).round(1)
    rendimiento['Diferencia_Goles'] = rendimiento['GF_Total'] - rendimiento['GC_Total']

    # Mostrar tabla
    st.dataframe(rendimiento, use_container_width=True)

    #Efectividad Ofensiva y Defensiva
    st.subheader("Efectividad Ofensiva y Defensiva por Temporada")

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de eficiencia ofensiva (Goles vs xG)
        if 'xg' in cols:
            xg_data = barca_data.groupby(season_col).agg({
                gf_col: 'mean',
                cols['xg']: 'mean'
            }).reset_index()

            fig_eficiencia = utils.go.Figure()
            fig_eficiencia.add_trace(utils.go.Bar(
                name='Goles Reales',
                x=xg_data[season_col],
                y=xg_data[gf_col],
                marker_color=utils.BLUE
            ))
            fig_eficiencia.add_trace(utils.go.Bar(
                name='xG Esperado',
                x=xg_data[season_col],
                y=xg_data[cols['xg']],
                marker_color=utils.MAROON
            ))

            fig_eficiencia.update_layout(
                title='Eficiencia Ofensiva: Goles Reales vs Esperados',
                barmode='group',
                xaxis_title="Temporada",
                yaxis_title="Goles por Partido"
            )
            st.plotly_chart(fig_eficiencia, use_container_width=True)

    with col2:
        # Gráfico de eficiencia defensiva (Goles vs xGA)
        if 'xga' in cols:
            xga_data = barca_data.groupby(season_col).agg({
                ga_col: 'mean',
                cols['xga']: 'mean'
            }).reset_index()

            fig_defensa = utils.go.Figure()
            fig_defensa.add_trace(utils.go.Bar(
                name='Goles Recibidos',
                x=xga_data[season_col],
                y=xga_data[ga_col],
                marker_color=utils.MAROON
            ))
            fig_defensa.add_trace(utils.go.Bar(
                name='xGA Esperado',
                x=xga_data[season_col],
                y=xga_data[cols['xga']],
                marker_color=utils.YELLOW
            ))

            fig_defensa.update_layout(
                title='Eficiencia Defensiva: Goles Recibidos vs Esperados',
                barmode='group',
                xaxis_title="Temporada",
                yaxis_title="Goles por Partido"
            )
            st.plotly_chart(fig_defensa, use_container_width=True)

    # Gráfico de evolución de puntos y efectividad
    st.subheader("Evolución de Puntos y Efectividad")

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de puntos por temporada
        fig_puntos = utils.px.line(
            rendimiento,
            x=season_col,
            y=['Puntos'],
            title='Puntos Totales por Temporada',
            labels={'value': 'Puntos', 'variable': 'Metrica'}
        )
        fig_puntos.update_traces(line=dict(color=utils.BLUE, width=3))
        st.plotly_chart(fig_puntos, use_container_width=True)

    with col2:
        # Gráfico de efectividad
        fig_efectividad = utils.px.line(
            rendimiento,
            x=season_col,
            y=['Efectividad'],
            title='Porcentaje de Efectividad por Temporada',
            labels={'value': 'Efectividad (%)', 'variable': 'Metrica'}
        )
        fig_efectividad.update_traces(line=dict(color=utils.MAROON, width=3))
        st.plotly_chart(fig_efectividad, use_container_width=True)

    # Análisis de rendimiento por localía
    st.subheader("Rendimiento por Localía")

    if 'venue' in cols:
        localia_data = barca_data.groupby([season_col, cols['venue']]).agg({
            gf_col: ['mean', 'count'],
            ga_col: 'mean',
            'result': lambda x: (x == 'W').sum()
        }).round(2)

        # Reestructurar datos para gráfico
        localia_stats = []
        for temporada in barca_data[season_col].unique():
            for localia in ['Home', 'Away']:
                temp_data = barca_data[(barca_data[season_col] == temporada) &
                                     (barca_data[cols['venue']] == localia)]
                if not temp_data.empty:
                    victorias = len(temp_data[temp_data[cols['result']] == 'W'])
                    empates = len(temp_data[temp_data[cols['result']] == 'D'])
                    derrotas = len(temp_data[temp_data[cols['result']] == 'L'])
                    puntos = (victorias * 3) + empates

                    localia_stats.append({
                        'Temporada': temporada,
                        'Localia': localia,
                        'Partidos': len(temp_data),
                        'Victorias': victorias,
                        'Empates': empates,
                        'Derrotas': derrotas,
                        'Puntos': puntos,
                        'Efectividad': (puntos / (len(temp_data) * 3) * 100) if len(temp_data) > 0 else 0
                    })

        if localia_stats:
            df_localia = pd.DataFrame(localia_stats)

            fig_localia = utils.px.bar(
                df_localia,
                x='Temporada',
                y='Efectividad',
                color='Localia',
                title='Efectividad por Localía y Temporada',
                barmode='group',
                color_discrete_map={'Home': utils.BLUE, 'Away': utils.MAROON}
            )
            st.plotly_chart(fig_localia, use_container_width=True)

else:
    st.error("No se encontraron las columnas necesarias para el analisis")

st.markdown("---")
st.caption("Analisis Estadistico FC Barcelona | Analisis por Temporadas")
