import utils
import grafico1_possession
import grafico2_xg_xga
import grafico3_poss_vs_xg
import grafico4_promedio_de_puntos
import grafico5_results

# Configuración de página
utils.st.set_page_config(
    page_title="Análisis FC Barcelona",
    page_icon="⚽",
    layout="wide"
)

# Título principal
utils.st.title("⚽ Análisis Estadístico FC Barcelona (2020-2024)")
utils.st.markdown("---")

# Lista de gráficos con sus módulos y funciones específicas
graficos_config = [
    {
        "titulo": "1. Evolución de la Posesión por Temporada",
        "descripcion": "Análisis de la evolución del promedio de posesión del FC Barcelona",
        "modulo": grafico1_possession,
        "funcion": "generar_possession"
    },
    {
        "titulo": "2. Goles Esperados (xG) vs Goles Esperados en Contra (xGA)",
        "descripcion": "Comparación entre goles esperados a favor y en contra",
        "modulo": grafico2_xg_xga,
        "funcion": "generar_xg_xga"
    },
    {
        "titulo": "3. Relación entre Posesión y Oportunidades de Gol",
        "descripcion": "Correlación entre posesión y goles esperados (xG)",
        "modulo": grafico3_poss_vs_xg,
        "funcion": "generar_poss_vs_xg"
    },
    {
        "titulo": "4. Efectividad por Formación Táctica",
        "descripcion": "Puntos promedio obtenidos por cada formación",
        "modulo": grafico4_promedio_de_puntos,
        "funcion": "generar_puntos_formacion"
    },
    {
        "titulo": "5. Resultados por Temporada",
        "descripcion": "Distribución de victorias, empates y derrotas por temporada",
        "modulo": grafico5_results,
        "funcion": "generar_resultados"
    }
]

# Mostrar todos los gráficos
for config in graficos_config:
    utils.st.header(config["titulo"])
    utils.st.caption(config["descripcion"])

    try:
        # Obtener la función del módulo
        funcion_grafico = getattr(config["modulo"], config["funcion"])

        # Generar el gráfico
        fig, interpretacion = funcion_grafico()

        # Mostrar el gráfico según el tipo
        if hasattr(fig, 'write_image'):  # Es figura de Plotly
            utils.st.plotly_chart(fig, use_container_width=True)
        else:  # Es figura de matplotlib
            utils.st.pyplot(fig)

        # Mostrar interpretación
        utils.st.markdown("### 📊 Interpretación")
        utils.st.write(interpretacion)

    except Exception as e:
        utils.st.error(f"Error generando {config['titulo']}: {str(e)}")

    utils.st.markdown("---")

# Nota final
utils.st.markdown("**📈 Métodología:** Análisis basado en datos de LaLiga 2020-2024")
utils.st.markdown("*Visualización creada con Streamlit*")
