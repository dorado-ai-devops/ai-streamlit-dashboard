import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="AI DevOps Dashboard", layout="wide")
st.title("📊 DevOps IA Dashboard")
st.markdown("Visualiza interacciones de IA con logs, Helm Charts y pipelines.")

# Cargar los datos
df = load_data()

if df.empty:
    st.warning("No se han encontrado datos para mostrar.")
    st.stop()

# Filtro principal por microservicio
microservices = st.sidebar.multiselect(
    "Filtrar por microservicio",
    options=sorted(df["microservice"].unique()),
    default=list(df["microservice"].unique())
)

df_filtered = df[df["microservice"].isin(microservices)]

# Tabla principal
st.markdown("### Registros encontrados")
st.dataframe(
    df_filtered[["timestamp", "type", "microservice", "summary", "tags"]],
    use_container_width=True
)

# Vista detallada
st.markdown("### Detalle de ejecución")

if not df_filtered.empty:
    row = st.selectbox(
        "Selecciona una fila",
        df_filtered.index,
        format_func=lambda i: f"{df_filtered.loc[i]['timestamp']} | {df_filtered.loc[i]['microservice']} | {df_filtered.loc[i]['summary'][:50]}..."
    )

    selected = df_filtered.loc[row]

    st.markdown("**Input:**")
    st.code(selected["input"], language="bash")

    st.markdown("**Prompt enviado:**")
    st.code(selected["prompt"], language="markdown")

    st.markdown("**Respuesta del modelo:**")
    st.code(selected["response"], language="markdown")
else:
    st.info("No hay registros que coincidan con el filtro seleccionado.")
