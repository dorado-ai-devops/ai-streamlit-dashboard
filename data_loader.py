import os
import json
import pandas as pd

GATEWAY_DIR = "/mnt/data/gateway"
MCP_DIR = "/mnt/data/mcp"

def load_data():
    records = []


    if not os.path.exists(GATEWAY_DIR):
        return pd.DataFrame()

    for filename in os.listdir(GATEWAY_DIR):
        if not filename.endswith(".json") or "_" not in filename:
            continue

        timestamp, tipo_raw = filename.split("_", 1)
        tipo = tipo_raw.replace(".json", "")

        try:
            with open(os.path.join(GATEWAY_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            continue

        prompt = data.get("prompt", "")
        response = data.get("response", "")
        input_text = data.get("input", "")


    for filename in os.listdir(GATEWAY_DIR):
        if not filename.endswith(".json"):
            continue
        timestamp, tipo_raw = filename.split("_", 1)
        tipo = tipo_raw.replace(".json", "")
        with open(os.path.join(GATEWAY_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
        prompt = data.get("prompt", "")
        response = data.get("response", "")
        input_text = data.get("input", "")



    return pd.DataFrame(records)



