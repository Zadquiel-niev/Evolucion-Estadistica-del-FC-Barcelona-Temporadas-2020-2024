import utils

def generar_poss_vs_xg():
    df = utils.load_and_clean_data()
    barca = utils.filter_barcelona_data(df)
    barca = utils.convert_numeric_columns(barca, ['poss', 'xg'])


    fig = utils.px.scatter(
        barca,
        x='poss',
        y='xg',
        title='Barcelona: Posesión vs xG (2020-2024)',
        labels={'poss': 'Posesión (%)', 'xg': 'Goles Esperados (xG)'},
        opacity=0.7
    )


    if len(barca) > 1:
        z = utils.np.polyfit(barca['poss'], barca['xg'], 1)
        p = utils.np.poly1d(z)
        x_range = [barca['poss'].min(), barca['poss'].max()]
        y_range = p(x_range)

        fig.add_trace(
            utils.go.Scatter(
                x=x_range,
                y=y_range,
                mode='lines',
                name='Línea de tendencia',
                line=dict(color='red', width=3, dash='dash')
            )
        )

    fig.update_traces(
        marker=dict(color=utils.BLUE, size=8, line=dict(width=1, color='darkblue'))
    )

    fig.update_layout(
        showlegend=True,
        xaxis=dict(title='Posesión (%)'),
        yaxis=dict(title='Goles Esperados (xG)')
    )

    # Interpretacion
    interpretacion = """
    **Interpretación:**
    Bueno, como podemos notar no hay tanta correlación. Es decir, entre
    más posesión del balón tiene el Barcelona tiene más chance de Gol, o sea,
    tiene más oportunidad de Gol Sí, pero no es una regla. O sea, no es juro
    que entre tenga mas posición del balón, ajuro va a tener más goles. No,
    no va a tener más chance, no es ajuro como podemos observarlo. Es depende
    probablemente depende del partido, depende de los jugadores que estén en
    cancha, depende de muchas cosas, pero hay una correlación. Sí baja, sí,
    pero la hay. Entonces podemos decir que entre más posición tiene el
    Fútbol Club Barcelona el balón, se podría decir que tiene un poquito más
    oportunidades de Gol, no 100% más pero si algo.
    """

    return fig, interpretacion

if __name__ == "__main__":
    fig, interpretacion = generar_poss_vs_xg()
    fig.write_image("grafico3_poss_vs_xg.png")
    print(interpretacion)
