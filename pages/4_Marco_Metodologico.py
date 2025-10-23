import streamlit as st


st.title("Marco Metodologico - FC Barcelona")
st.markdown("---")

st.markdown("""
### Fuente de Datos

- **Dataset**: matches_full_la_liga.csv
- **Periodo**: Temporadas 2020-2021 hasta 2024-2025
- **Registros**: 4,319 partidos de La Liga
- **Variables**:
  - *Resultados*: goles (gf, ga), resultado (result)
  - *Rendimiento*: posesion (poss), tiros (sh), tiros a puerta (sot), expected goals (xg, xga)
  - *Contexto*: formacion (formation), asistencia (attendance), localia (venue)

### Proceso de Trabajo

#### Fase 1: Preparacion de Datos
- Filtracion y limpieza de registros del FC Barcelona
- Normalizacion de variables y tratamiento de valores missing
- Validacion de consistencia de datos

#### Fase 2: Analisis Descriptivo
- Calculo de medidas de tendencia central y dispersion
- Analisis de distribuciones y frecuencias
- Identificacion de patrones y tendencias temporales

#### Fase 3: Visualizacion Avanzada
- Creacion de graficos interactivos para representar hallazgos
- Desarrollo de dashboards para exploracion de datos
- Generacion de tablas resumen y reportes

#### Fase 4: Conclusiones
- Sintesis de resultados obtenidos
- Respuesta a objetivos planteados
- Elaboracion de recomendaciones basadas en datos

### Variables de Analisis

#### Variables Cuantitativas
- **Goles a Favor (GF)**: Numero de goles marcados por partido
- **Goles en Contra (GA)**: Numero de goles recibidos por partido
- **Posesion (POSS)**: Porcentaje de tiempo con control del balon
- **Expected Goals (xG)**: Calidad de oportunidades de gol creadas
- **Expected Goals Against (xGA)**: Calidad de oportunidades concedidas

#### Variables Cualitativas
- **Resultado**: Victoria (W), Empate (D), Derrota (L)
- **Formacion**: Esquema tactico utilizado (4-3-3, 3-5-2, etc.)
- **Localia**: Condicion de local (Home) o visitante (Away)
- **Temporada**: Año de la competicion

### Herramientas Tecnologicas

- **Python**: Lenguaje de programacion principal
- **Pandas**: Procesamiento y analisis de datos
- **Plotly**: Visualizaciones interactivas
- **Streamlit**: Desarrollo de aplicacion web
- **Estadistica Descriptiva**: Analisis exploratorio de datos
""")

st.markdown("---")
st.caption("Analisis Estadistico FC Barcelona | Marco Metodologico")
