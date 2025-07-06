import streamlit as st
import pandas as pd
import os
import json
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Configuración inicial
st.set_page_config(page_title="AI DevOps Dashboard", layout="wide")
st.title("📊 DevOps IA Dashboard")
st.markdown("Visualiza las interacciones de los LLMs con logs, Helm Charts y generación de pipelines.")
st.markdown("---")

# Rutas base
BASE_DIR = os.environ.get("BASE_DIR", "/mnt/data")
MCP_DIR = os.path.join(BASE_DIR, "mcp")
GATEWAY_DIR = os.path.join(BASE_DIR, "gateway")

# Leer archivos de texto
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

# Cargar registros
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

# Filtros laterales
st.sidebar.header("Filtros")
microservices = st.sidebar.multiselect(
    "Filtrar por microservicio",
    sorted(df["microservice"].dropna().unique()),
    default=list(df["microservice"].dropna().unique())
)
types = st.sidebar.multiselect(
    "Filtrar por tipo",
    sorted(df["type"].dropna().unique()),
    default=list(df["type"].dropna().unique())
)

df_filtered = df[
    df["microservice"].isin(microservices) & df["type"].isin(types)
]

# AgGrid: configuración completa
st.markdown("### Registros encontrados")
gb = GridOptionsBuilder.from_dataframe(df_filtered)

# Ocultar columnas que no deben mostrarse pero sí usarse en detalle
gb.configure_columns(["input", "prompt", "response"], hide=True)

gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_default_column(groupable=False, editable=False, filter=True, resizable=True)
gb.configure_selection('single', use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    df_filtered,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme="streamlit",
    fit_columns_on_grid_load=True
)

# Mostrar detalles si hay selección
selected_rows = grid_response.get('selected_rows', [])
if selected_rows:
    selected = selected_rows[0]

    st.markdown("### Detalle de ejecución seleccionado")

    with st.expander("🔍 Input"):
        st.code(selected.get("input", ""), language="bash")

    with st.expander("📤 Prompt enviado"):
        st.code(selected.get("prompt", ""), language="markdown")

    with st.expander("📥 Respuesta del modelo"):
        st.code(selected.get("response", ""), language="markdown")

    st.download_button(
        label="📥 Descargar resultado",
        data=pd.DataFrame([selected]).to_csv(index=False).encode("utf-8"),
        file_name=f"registro_{selected.get('timestamp', 'registro')}.csv",
        mime="text/csv"
    )
else:
    st.info("Selecciona un registro en la tabla para ver los detalles.")
