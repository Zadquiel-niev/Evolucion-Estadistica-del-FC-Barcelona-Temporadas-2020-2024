import utils

def generar_resultados():
    df = utils.load_and_clean_data()
    barca = utils.filter_barcelona_data(df)

    # Limpiar resultados
    barca['result'] = barca['result'].astype(str).str.strip().str.upper()

    # Conteo por temporada y resultado
    pivot = barca.pivot_table(index='season', columns='result',
                              values='date', aggfunc='count', fill_value=0)

    # Asegurar que tenemos W, D, L
    for col in ['W', 'D', 'L']:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[['W', 'D', 'L']].sort_index()

    # Preparar datos para grafico interactivo
    pivot_reset = pivot.reset_index().melt(
        id_vars='season',
        value_vars=['W', 'D', 'L'],
        var_name='resultado',
        value_name='cantidad'
    )

    # Crear grafico de barras agrupadas interactivo
    fig = utils.px.bar(
        pivot_reset,
        x='season',
        y='cantidad',
        color='resultado',
        title="Resultados del FC Barcelona por temporada (2020–2024)",
        labels={'season': 'Temporada', 'cantidad': 'Cantidad de partidos'},
        color_discrete_map={'W': utils.BLUE, 'D': utils.YELLOW, 'L': utils.MAROON},
        barmode='group'
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1),
        legend_title_text='Resultado'
    )

    # Interpretacion
    interpretacion = """
    **Interpretación:**
    El gráfico muestra la cantidad de partidos **ganados, empatados y perdidos** por temporada (2020–2024).
    Se observa una **mejora progresiva** en los resultados con **aumento de victorias** y **reducción de derrotas**
    en las temporadas más recientes, lo cual confirma la **recuperación competitiva del equipo** tras las temporadas más complicadas.
    La temporada **2023** muestra el mejor balance, indicando una efectividad creciente del proyecto deportivo.
    """

    return fig, interpretacion

if __name__ == "__main__":
    fig, interpretacion = generar_resultados()
    fig.write_image("grafico5_results.png")
    print(interpretacion)
