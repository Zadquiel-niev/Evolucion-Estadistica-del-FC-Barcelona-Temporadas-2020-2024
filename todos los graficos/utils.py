import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import streamlit as st

# Configuración de colores
BLUE = "#004d98"
MAROON = "#a50044"
YELLOW = "#ffcc00"

def load_and_clean_data():
    csv_file = "matches_full_LaLiga.csv"
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"No se encontró '{csv_file}'")

    df = pd.read_csv(csv_file)
    df.columns = [c.strip() for c in df.columns]

    # Limpieza básica
    for c in df.select_dtypes(include='object').columns:
        df[c] = df[c].astype(str).str.strip()

    return df

def filter_barcelona_data(df, seasons=[2020, 2021, 2022, 2023, 2024]):
    team_col = None
    for c in df.columns:
        try:
            if df[c].astype(str).str.lower().str.contains('barcelona', na=False).any():
                team_col = c
                break
        except Exception:
            continue

    if team_col:
        barca = df[df[team_col].astype(str).str.lower().str.contains('barcelona', na=False)].copy()
    else:
        # Por si acaso buscar en columna 'team'
        barca = df[df['team'].str.lower() == 'barcelona'].copy()

    # Filtrar temporadas
    barca = barca[barca['season'].isin(seasons)]

    return barca

def convert_numeric_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
