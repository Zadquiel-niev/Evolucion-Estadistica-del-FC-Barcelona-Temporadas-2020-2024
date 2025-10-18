import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer datos
datos = pd.read_csv("matches_full_LaLiga.csv")
datos.columns = [c.strip() for c in datos.columns]

# Filtrar Barcelona
barca = datos[datos['team'].str.contains('barcelona', case=False, na=False)]
barca = barca[barca['season'].between(2020, 2024)]

# Gráfico 
plt.figure(figsize=(10, 6))
plt.scatter(barca['poss'], barca['xg'], color='blue', alpha=0.6)

# Añadir línea de tendencia
if len(barca) > 1:  # Solo si hay suficientes 
    z = np.polyfit(barca['poss'], barca['xg'], 1)
    p = np.poly1d(z)
    plt.plot(barca['poss'], p(barca['poss']), "r-", linewidth=2,)
    plt.legend()

plt.xlabel('Posesión (%)')
plt.ylabel('Goles Esperados (xG)')
plt.title('Barcelona: Posesión vs xG (2020-2024)')
plt.grid(True)
plt.show()

# Interpretación
print("\n" + "="*80)
print("INTERPRETACIÓN:")
print("="*80)
print("Bueno, como podemos notar no hay tanta correlación. es decir entre")
print("más posesión del balón tiene el Barcelona tiene más chance de Gol, o sea,")
print("tiene más oportunidad de Gol Sí, pero no es una regla. O sea, no es juro")
print("que entre tenga mas posición del balón, ajuro va a tener más goles. No,")
print("no va a tener más chance, no es ajuro como podemos observarlo. Es depende")
print("probablemente depende del partido, depende de los jugadores que estén en")
print("cancha, depende de muchas cosas, pero hay una correlación. Sí baja, sí,")
print("pero la hay. Entonces podemos decir que entre más posición tiene el")
print("Fútbol Club Barcelona el balón, se podría decir que tiene un poquito más")
print("oportunidades de Gol, no 100% más pero si algo.")
print("="*80)