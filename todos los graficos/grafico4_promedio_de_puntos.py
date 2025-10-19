import utils

def generar_puntos_formacion():
    df = utils.load_and_clean_data()
    barca = utils.filter_barcelona_data(df)
    barca = utils.convert_numeric_columns(barca, ['gf', 'ga'])

    # Calcular puntos
    barca['puntos'] = barca.apply(lambda x: 3 if x['gf'] > x['ga'] else (1 if x['gf'] == x['ga'] else 0), axis=1)

    # Agrupar por formacion
    formacion_media = barca.groupby("formation")["puntos"].mean().sort_values(ascending=False).reset_index()

    # Crear grafico de barras interactivo
    fig = utils.px.bar(
        formacion_media,
        x='formation',
        y='puntos',
        title="FC Barcelona - Promedio de puntos por formación (2020-2024)",
        labels={'formation': 'Formación', 'puntos': 'Puntos promedio'},
        color='puntos',
        color_continuous_scale=[utils.MAROON, utils.BLUE]
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        yaxis=dict(range=[0, 3])
    )

    # Encontrar la mejor y peor formacion
    mejor = formacion_media.iloc[0]
    peor = formacion_media.iloc[-1]

    interpretacion = f"""
    **Interpretación:**
    La formación que más puntos logró fue **'{mejor['formation']}'** con un promedio de **{mejor['puntos']:.2f} puntos** por partido.
    La formación menos efectiva fue **'{peor['formation']}'** con un promedio de **{peor['puntos']:.2f} puntos** por partido.
    Esto sugiere que la **táctica influye significativamente en el rendimiento**, aunque también depende del rival,
    localía y estado del equipo. La formación **4-3-3** tradicional del Barcelona sigue siendo de las más efectivas.
    """

    return fig, interpretacion

if __name__ == "__main__":
    fig, interpretacion = generar_puntos_formacion()
    fig.write_image("grafico4_promedio_de_puntos.png")
    print(interpretacion)
