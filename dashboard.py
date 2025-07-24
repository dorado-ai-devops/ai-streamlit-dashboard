import os
import json
from typing import List, Dict, Any

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# -----------------------------------
# Configuración inicial
# -----------------------------------
st.set_page_config(page_title="AI DevOps Dashboard", layout="wide")
st.title(" DevOps IA Dashboard")
st.markdown(
    "Visualiza las interacciones de los LLMs con logs, Helm Charts y generación de pipelines."
)
st.markdown("---")

# -----------------------------------
# Rutas base
# -----------------------------------
BASE_DIR = os.environ.get("BASE_DIR", "/mnt/data")
MCP_DIR = os.path.join(BASE_DIR, "mcp")
GATEWAY_DIR = os.path.join(BASE_DIR, "gateway")

# -----------------------------------
# Helpers
# -----------------------------------

def leer_contenido(path: str) -> str:
    """
    Devuelve el contenido de un archivo de texto.
    Acepta rutas absolutas o internas al contenedor.
    """
    if not path:
        return ""

    # Normaliza rutas que vienen del contenedor
    if path.startswith("/app/outputs/"):
        path = path.replace("/app/outputs/", f"{GATEWAY_DIR}/")

    if not os.path.exists(path):
        return ""

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Carga todos los registros JSON generados por los microservicios.
    """
    if not os.path.exists(MCP_DIR):
        return pd.DataFrame()

    records: List[Dict[str, Any]] = []
    for filename in os.listdir(MCP_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(MCP_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        # Campos mínimos obligatorios
        if "type" not in data or "timestamp" not in data:
            continue

        records.append(
            {
                "timestamp": data.get("timestamp", ""),
                "type": data.get("type", ""),
                "microservice": data.get("microservice", ""),
                "summary": data.get("summary", ""),
                "tags": ", ".join(data.get("tags", [])),
                "prompt": leer_contenido(data.get("prompt_path")),
                "response": leer_contenido(data.get("response_path")),
                "input": leer_contenido(data.get("input_path", "")),
            }
        )

    return pd.DataFrame(records)


def normalize_selected_rows(selection) -> List[Dict[str, Any]]:
    """Convierte la selección de AgGrid a una lista de dicts homogénea."""
    if selection is None:
        return []
    if isinstance(selection, pd.DataFrame):
        return selection.to_dict(orient="records")
    if isinstance(selection, list):
        return selection
    return []


# -----------------------------------
# Carga de datos
# -----------------------------------
df = load_data()

if df.empty:
    st.warning("No se han encontrado datos para mostrar.")
    st.stop()

# -----------------------------------
# Filtros laterales
# -----------------------------------
st.sidebar.header("Filtros")

microservices = st.sidebar.multiselect(
    "Filtrar por microservicio",
    sorted(df["microservice"].dropna().unique()),
    default=list(df["microservice"].dropna().unique()),
)

types = st.sidebar.multiselect(
    "Filtrar por tipo",
    sorted(df["type"].dropna().unique()),
    default=list(df["type"].dropna().unique()),
)

df_filtered = df[
    df["microservice"].isin(microservices) & df["type"].isin(types)
].sort_values("timestamp", ascending=False)

# -----------------------------------
# AgGrid: configuración
# -----------------------------------
st.markdown(f"### Registros encontrados ({len(df_filtered)})")

gb = GridOptionsBuilder.from_dataframe(df_filtered)
gb.configure_columns(["input", "prompt", "response"], hide=True)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_default_column(
    groupable=False, editable=False, filter=True, resizable=True
)
gb.configure_selection("single", use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    df_filtered,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme="streamlit",
    fit_columns_on_grid_load=True,
    height=350,
)

# -----------------------------------
# Detalle de la fila seleccionada
# -----------------------------------
selected_rows = normalize_selected_rows(grid_response.get("selected_rows"))
if len(selected_rows) > 0:
    selected = selected_rows[0]

    st.markdown("### Detalle de ejecución seleccionado")

    cols = st.columns(3)
    cols[0].metric("Fecha", selected.get("timestamp"))
    cols[1].metric("Tipo", selected.get("type"))
    cols[2].metric("Servicio", selected.get("microservice"))

    with st.expander(" Input"):
        st.code(selected.get("input", ""), language="bash")

    with st.expander(" Prompt enviado"):
        st.code(selected.get("prompt", ""), language="markdown")

    with st.expander(" Respuesta del modelo"):
        st.code(selected.get("response", ""), language="markdown")

    st.download_button(
        label=" Descargar registro CSV",
        data=pd.DataFrame([selected]).to_csv(index=False).encode("utf-8"),
        file_name=f"registro_{selected.get('timestamp', 'registro')}.csv",
        mime="text/csv",
    )
else:
    st.info("Selecciona un registro en la tabla para ver los detalles.")
