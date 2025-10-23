import streamlit as st

st.title("Objetivos")
st.markdown("---")

st.markdown("""
### Objetivo General

Evaluar la evolucion tactica y de rendimiento ofensivo del Futbol Club Barcelona durante las temporadas 2020 a 2024, mediante el analisis estadistico y la visualizacion de metricas avanzadas.

### Objetivos Especificos

1. **Cuantificar tendencias anuales**
   Analizar la evolucion de metricas clave (Goles a Favor, Goles en Contra, Posesion) para determinar la direccion del modelo de juego.

2. **Establecer relaciones entre posesion y eficiencia**
   Examinar la correlacion entre el porcentaje de posesion y la creacion de oportunidades (xG, xGA) a nivel de partido.

3. **Evaluar la efectividad de las formaciones tacticas**
   Determinar si existe diferencia significativa en los puntos obtenidos segun la formacion tactica utilizada.

4. **Analizar el rendimiento por localia**
   Comparar el desempeño del equipo en condicion de local versus visitante.

5. **Identificar patrones de consistencia ofensiva**
   Evaluar la variabilidad en la produccion de goles a lo largo del periodo analizado.

### Alcance del Analisis

- **Temporadas**: 2020, 2021, 2022, 2023, 2024
- **Competencia**: Liga Espanola (LaLiga)
- **Metricas principales**: GF, GA, Poss, xG, xGA, Resultados, Formaciones
- **Enfoque**: Analisis descriptivo y comparativo

### Limitaciones

- El analisis se limita a datos de La Liga
- No se consideran competiciones internacionales
- Variables contextuales como lesiones no estan incluidas
""")

st.markdown("---")
st.caption("Analisis Estadistico FC Barcelona | Objetivos")
