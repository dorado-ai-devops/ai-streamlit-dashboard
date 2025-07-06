import streamlit as st
import pandas as pd
import os
import json

# Configuración inicial
st.set_page_config(page_title="AI DevOps Dashboard", layout="wide")
st.title("📊 DevOps IA Dashboard")
st.markdown("Visualiza las interacciones de los LLMs con los logs, Helm Charts y generacion de pipelines.")
st.markdown("---")

# Rutas
BASE_DIR = os.environ.get("BASE_DIR", "/mnt/data")
MCP_DIR = os.path.join(BASE_DIR, "mcp")
GATEWAY_DIR = os.path.join(BASE_DIR, "gateway")

# Función para leer los contenidos
def leer_contenido(path):
    if not path:
        return ""
    real_path = path.replace("/app/outputs/", GATEWAY_DIR + "/")
    if not os.path.exists(real_path):
        return ""
    try:
        with open(real_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

# Cargar datos
@st.cache_data
def load_data():
    records = []
    if not os.path.exists(MCP_DIR):
        return pd.DataFrame()
    for filename in os.listdir(MCP_DIR):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(MCP_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if "type" not in data or "timestamp" not in data:
            continue
        records.append({
            "timestamp": data.get("timestamp", ""),
            "type": data.get("type", ""),
            "microservice": data.get("microservice", ""),
            "summary": data.get("summary", ""),
            "tags": ", ".join(data.get("tags", [])),
            "prompt": leer_contenido(data.get("prompt_path")),
            "response": leer_contenido(data.get("response_path")),
            "input": leer_contenido(data.get("input_path", ""))
        })
    return pd.DataFrame(records)

df = load_data()

if df.empty:
    st.warning("No se han encontrado datos para mostrar.")
    st.stop()

# Filtros
st.sidebar.header("Filtros")
microservices = st.sidebar.multiselect(
    "Filtrar por microservicio",
    options=sorted(df["microservice"].dropna().unique()),
    default=list(df["microservice"].dropna().unique())
)
types = st.sidebar.multiselect(
    "Filtrar por tipo",
    options=sorted(df["type"].dropna().unique()),
    default=list(df["type"].dropna().unique())
)

df_filtered = df[
    df["microservice"].isin(microservices) & df["type"].isin(types)
]

# Tabla
st.markdown("### Registros encontrados")
st.dataframe(df_filtered[["timestamp", "type", "microservice", "summary", "tags"]], use_container_width=True)

# Detalle
st.markdown("### Detalle de ejecución")
if not df_filtered.empty:
    row = st.selectbox(
        "Selecciona una fila",
        df_filtered.index,
        format_func=lambda i: f"{df_filtered.loc[i]['timestamp']} | {df_filtered.loc[i]['microservice']} | {df_filtered.loc[i]['summary'][:50]}..."
    )
    selected = df_filtered.loc[row]

    with st.expander("🔍 Input"):
        st.text(selected["input"])

    with st.expander("📤 Prompt enviado"):
        st.text(selected["prompt"])

    with st.expander("📥 Respuesta del modelo"):
        st.text(selected["response"])

    st.download_button(
        label="📥 Descargar resultado",
        data=selected.to_csv().encode("utf-8"),
        file_name=f"registro_{selected['timestamp']}.csv",
        mime="text/csv"
    )
else:
    st.info("No hay registros que coincidan con el filtro seleccionado.")
