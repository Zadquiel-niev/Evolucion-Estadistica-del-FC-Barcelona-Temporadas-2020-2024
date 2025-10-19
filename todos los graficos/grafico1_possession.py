import utils

def generar_possession():
    df = utils.load_and_clean_data()
    barca = utils.filter_barcelona_data(df)
    barca = utils.convert_numeric_columns(barca, ['poss', 'season'])

    # Calculos específicos del gráfico
    summary = (
        barca.groupby('season', as_index=False)['poss']
        .mean()
        .rename(columns={'poss': 'Posesión promedio (%)'})
    )

    # Crear figura
    fig = utils.px.line(
        summary,
        x='season',
        y='Posesión promedio (%)',
        markers=True,
        title="Evolución de la posesión promedio (FC Barcelona 2020–2024)",
        labels={'season': 'Temporada', 'Posesión promedio (%)': 'Posesión promedio (%)'}
    )

    fig.update_traces(
        line=dict(color=utils.BLUE, width=3),
        marker=dict(color=utils.BLUE, size=8)
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1),
        hovermode='x unified'
    )

    # Interpretación
    interpretacion = """
    **Interpretación:**
    Entre las temporadas **2020 y 2024**, el FC Barcelona ha mostrado una **tendencia descendente en la posesión promedio del balón**,
    pasando de cerca del **66–67%** a alrededor del **64%** por partido.
    Este descenso refleja una **pérdida parcial del estilo de juego histórico del club**, basado en la **filosofía del *Tiki Taka*** y el control constante del balón.
    No obstante, a pesar de esta disminución, el equipo **mantiene uno de los promedios de posesión más altos de LaLiga**,
    lo que evidencia que su identidad táctica aún conserva raíces en el dominio del balón.
    """

    return fig, interpretacion

# Por si acaso
if __name__ == "__main__":
    fig, interpretacion = generar_possession()
    fig.write_image("grafico1_possession.png")
    print(interpretacion)
