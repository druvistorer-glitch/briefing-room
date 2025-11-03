import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DAILY_DIR = DATA_DIR / "daily"
SUMMARIES_DIR = DATA_DIR / "summaries"
TEMPLATES_DIR = ROOT / "templates"

for d in [DATA_DIR, DAILY_DIR, SUMMARIES_DIR, TEMPLATES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def today_str():
    return datetime.utcnow().strftime("%Y-%m-%d")

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
