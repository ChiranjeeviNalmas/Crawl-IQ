import json
import os
from datetime import datetime
from .logger import get_logger

log = get_logger("storage")
OUTPUT_DIR = "output"


def save(data: dict, filename: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"{filename}_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("Saved → %s  (links=%d)", path, len(data.get("links", [])))
    return path
