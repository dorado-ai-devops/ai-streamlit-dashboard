import os
import json
import pandas as pd

# Base del volumen montado en el contenedor
BASE_DIR = os.environ.get("BASE_DIR", "/mnt/data")
MCP_DIR = os.path.join(BASE_DIR, "mcp")
GATEWAY_DIR = os.path.join(BASE_DIR, "gateway")

def leer_contenido(path):
    if not path:
        return ""

    # Reescribe el path virtual usado en los JSON para que apunte al volumen real
    real_path = path.replace("/app/outputs/", GATEWAY_DIR + "/")

    if not os.path.exists(real_path):
        return ""

    try:
        with open(real_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

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
