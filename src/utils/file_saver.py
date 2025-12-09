"""
Helper to persist JSON outputs into src/outputs/ with timestamped filenames.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_json_output(obj: Dict[str, Any], prefix: str = "output") -> str:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{prefix}_{ts}.json"
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    # Return relative path from repo root
    try:
        return str(path.relative_to(Path.cwd()))
    except Exception:
        return str(path)
