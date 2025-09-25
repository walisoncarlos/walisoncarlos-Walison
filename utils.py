import pandas as pd, json, os
from pathlib import Path

MEM_FILE = Path("memory.json")

def load_csv(path_or_buffer):
    if hasattr(path_or_buffer, "read"):
        return pd.read_csv(path_or_buffer)
    return pd.read_csv(path_or_buffer)

def save_memory(obj):
    data = {}
    if MEM_FILE.exists():
        try:
            data = json.loads(MEM_FILE.read_text())
        except:
            data = {}
    data.update(obj)
    MEM_FILE.write_text(json.dumps(data, indent=2))

def load_memory():
    if not MEM_FILE.exists():
        return {}
    try:
        return json.loads(MEM_FILE.read_text())
    except:
        return {}