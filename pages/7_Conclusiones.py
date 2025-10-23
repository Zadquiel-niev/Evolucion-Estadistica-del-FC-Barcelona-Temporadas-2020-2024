import streamlit as st
import utils
import pandas as pd


st.title("Conclusiones")
st.markdown("---")

# Cargar datos para metricas finales
df = utils.load_and_clean_data()
if not df.empty:
    barca_data = utils.filter_barcelona_data(df)
    barca_data, cols = utils.prepare_barcelona_data(barca_data)

st.markdown("""
### Resumen de Hallazgos Principales

A continuacion se presentan las conclusiones principales del analisis estadistico del FC Barcelona en el periodo 2020-2024:
""")

if not df.empty and not barca_data.empty:
    # Calcular metricas clave
    posesion_promedio = barca_data[cols['poss']].mean() if 'poss' in cols else 0
    goles_promedio = barca_data[cols['gf']].mean() if 'gf' in cols else 0
    goles_contra_promedio = barca_data[cols['ga']].mean() if 'ga' in cols else 0

    # Crear tabla de conclusiones
    conclusiones_data = {
        'Aspecto': [
            "Modelo de Juego",
            "Efectividad Ofensiva",
            "Solidez Defensiva",
            "Consistencia",
            "Adaptabilidad Tactica"
        ],
        'Hallazgo': [
            "Mantenimiento del modelo de posesion alta" if posesion_promedio > 60 else "Cambio en el estilo de juego",
            "Alta efectividad en creacion de oportunidades" if goles_promedio > 1.8 else "Oportunidades limitadas",
            "Defensa solida y organizada" if goles_contra_promedio < 1.0 else "Debilidades defensivas",
            "Rendimiento estable a lo largo del periodo",
            "Uso variado de formaciones segun el contexto"
        ],
        'Recomendacion': [
            "Continuar con el modelo de posesion como base",
            "Mejorar la conversion de oportunidades",
            "Mantener la organizacion defensiva",
            "Trabajar en la consistencia visitante",
            "Optimizar formaciones mas efectivas"
        ]
    }

    conclusiones_df = pd.DataFrame(conclusiones_data)
    st.table(conclusiones_df)

st.markdown("""
### Interpretacion General

1. **Identidad de Juego**: El Barcelona mantuvo su estilo de posesion alta durante todo el periodo, confirmando su adhesion al modelo de juego caracteristico.

2. **Evolucion Defensiva**: Se observa una mejora notable en la efectividad defensiva, especialmente en las temporadas mas recientes.

3. **Adaptabilidad Tactica**: El equipo demostro flexibilidad en el uso de diferentes formaciones, adaptandose a las circunstancias de cada partido.

4. **Consistencia Ofensiva**: Mantuvieron una produccion de goles relativamente estable, con picos de efectividad en temporadas especificas.

5. **Rendimiento por Localia**: Se identificaron diferencias en el desempeño segun la condicion de local o visitante.

### Recomendaciones Estrategicas

- **Mantener la identidad**: Continuar con el modelo de posesion alta como base del juego
- **Optimizar formaciones**: Priorizar las formaciones que han demostrado mayor efectividad
- **Mejorar rendimiento visitante**: Trabajar en la consistencia en partidos fuera de casa
- **Seguimiento continuo**: Implementar un sistema de monitorizacion permanente de metricas clave
- **Analisis de rivales**: Incorporar analisis especificos por rival para optimizar estrategias

### Trabajo Futuro

- **Ampliar el alcance**: Incluir analisis de competiciones internacionales
- **Metricas avanzadas**: Incorporar metricas como presion, transiciones y xG chain
- **Analisis de jugadores**: Evaluar el impacto individual en el rendimiento colectivo
- **Prediccion de rendimiento**: Desarrollar modelos predictivos basados en datos historicos

### Limitaciones del Estudio

- El analisis se limita exclusivamente a partidos de La Liga
- No se consideraron variables contextuales como lesiones o situaciones climaticas
- El periodo analizado podria extenderse para identificar tendencias a mas largo plazo
""")

st.markdown("---")
st.caption("Analisis Estadistico FC Barcelona | Conclusiones")
