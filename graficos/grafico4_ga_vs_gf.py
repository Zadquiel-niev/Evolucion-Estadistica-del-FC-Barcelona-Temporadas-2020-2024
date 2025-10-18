import pandas as pd
import matplotlib.pyplot as plt

print("=== Gráfico 4: Puntos promedio por formación ===")
df = pd.read_csv("matches_full_LaLiga.csv")

#Limpiar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

#Filtrar xd
barca = df[df["team"].str.contains("barcelona", case=False, na=False)]
barca["season"] = pd.to_numeric(barca["season"], errors="coerce")
barca = barca[(barca["season"] >= 2020) & (barca["season"] <= 2024)]

# 4. Calcular puntos (3 victoria, 1 empate, 0 derrota)
barca["gf"] = pd.to_numeric(barca["gf"], errors="coerce")
barca["ga"] = pd.to_numeric(barca["ga"], errors="coerce")
barca["puntos"] = barca.apply(lambda x: 3 if x["gf"] > x["ga"] else (1 if x["gf"] == x["ga"] else 0), axis=1)
formacion_media = barca.groupby("formation")["puntos"].mean().sort_values(ascending=False)

#Gráfico
plt.figure(figsize=(8,5))
formacion_media.plot(kind="bar", color="#004D98", edgecolor="#A50044")
plt.title("FC Barcelona - Promedio de puntos por formación (2020-2024)")
plt.ylabel("Puntos promedio")
plt.xlabel("Formación")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

#Interpretación
mejor = formacion_media.idxmax()
peor = formacion_media.idxmin()
print(f"\nInterpretación:")
print(f"La formación que más puntos logró fue '{mejor}' con un promedio de {formacion_media.max():.2f} puntos por partido.")
print(f"La formación menos efectiva fue '{peor}' con un promedio de {formacion_media.min():.2f} puntos por partido.")
print("Esto sugiere que la táctica influye en el rendimiento, aunque también dependen del rival, localía y estado del equipo.")
