import os
import json
import pandas as pd

BASE_DIR = os.environ.get("BASE_DIR", "/mnt/data")
MCP_DIR = os.path.join(BASE_DIR, "mcp")

def leer_contenido(path):
    if not path or not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
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
            "summary": data.get("summary", ""),
            "tags": ", ".join(data.get("tags", [])),
            "prompt": leer_contenido(data.get("prompt_path")),
            "response": leer_contenido(data.get("response_path")),
            "input": leer_contenido(data.get("input_path", ""))
        })

    return pd.DataFrame(records)
