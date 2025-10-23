import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
import statsmodels.api as sm

# Configuracion de colores
BLUE = "#004D98"
MAROON = "#A50044"
YELLOW = "#FFCC00"

def load_and_clean_data():
    try:
        df = pd.read_csv('matches_full_la_liga.csv')

        # Limpiar nombres de columnas (quitar espacios al inicio y final)
        df.columns = df.columns.str.strip()

        # Limpiar formaciones
        if 'formation' in df.columns:
            df['formation'] = df['formation'].astype(str).str.replace('◆', '', regex=False)

        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

def filter_barcelona_data(df):
    if df.empty:
        return df

    # Verificar que las columnas necesarias existan
    required_cols = ['team', 'season']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Columnas faltantes: {missing_cols}")
        return pd.DataFrame()

    # Filtrar Barcelona
    barca_data = df[
        (df['team'] == 'Barcelona') &
        (df['season'].between(2020, 2024))
    ].copy()

    return barca_data

def prepare_barcelona_data(barca):
    """Preparar datos del Barcelona para analisis"""
    if barca.empty:
        return barca, {}

    # Columnas esperadas
    expected_cols = {
        'poss': ['poss', 'possession', 'pos'],
        'xg': ['xg', 'expected goals', 'expected'],
        'xga': ['xga', 'expected against', 'expected goals against'],
        'gf': ['gf', 'goals for', 'goles a favor', 'fthg'],
        'ga': ['ga', 'goals against', 'goles en contra', 'ftag'],
        'season': ['season', 'year', 'temporada'],
        'result': ['result', 'res', 'resultado'],
        'formation': ['formation', 'formacion', 'form'],
        'venue': ['venue', 'home_away', 'local', 'location', 'estadio']
    }

    # Encontrar columnas reales
    found_cols = {}
    for key, variants in expected_cols.items():
        for variant in variants:
            for col in barca.columns:
                if variant.lower() in col.lower():
                    found_cols[key] = col
                    break
            if key in found_cols:
                break

    # Convertir columnas a numerico
    numeric_cols = ['poss', 'xg', 'xga', 'gf', 'ga', 'season']
    for col in numeric_cols:
        if col in found_cols and found_cols[col] in barca.columns:
            barca[found_cols[col]] = pd.to_numeric(barca[found_cols[col]], errors='coerce')

    return barca, found_cols

# Exportar librerias para uso en los graficos
pd = pd
np = np
px = px
go = go
make_subplots = make_subplots
stats = stats
sm = sm
