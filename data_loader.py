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

        # Buscar MCP asociado
        mcp_file = f"{timestamp}_mcp.json"
        mcp_path = os.path.join(MCP_DIR, mcp_file)
        if os.path.exists(mcp_path):
            with open(mcp_path, "r", encoding="utf-8") as mcp_f:
                mcp_data = json.load(mcp_f)
            summary = mcp_data.get("summary", "")
            tags = ", ".join(mcp_data.get("tags", []))
        else:
            summary = ""
            tags = ""

        records.append({
            "timestamp": timestamp,
            "type": tipo,
            "input": input_text,
            "prompt": prompt,
            "response": response,
            "summary": summary,
            "tags": tags
        })

    return pd.DataFrame(records)
