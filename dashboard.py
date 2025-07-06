import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="AI DevOps Dashboard", layout="wide")
st.title("📊 DevOps IA Dashboard")
st.markdown("Visualiza interacciones de IA con logs, Helm Charts y pipelines.")

# Cargar los datos
df = load_data()

# Filtros por tipo
tipo = st.sidebar.multiselect("Filtrar por tipo", options=df["type"].unique(), default=df["type"].unique())
df_filtered = df[df["type"].isin(tipo)]

# Tabla principal
st.dataframe(df_filtered[["timestamp", "type", "summary", "tags"]], use_container_width=True)

# Vista detallada
st.markdown("### Detalle de ejecución")
row = st.selectbox("Selecciona una fila", df_filtered.index)
selected = df_filtered.loc[row]

st.code(selected["input"], language="bash")
st.markdown("**Prompt enviado:**")
st.code(selected["prompt"], language="markdown")
st.markdown("**Respuesta del modelo:**")
st.code(selected["response"], language="markdown")