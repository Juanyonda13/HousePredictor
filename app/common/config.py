from __future__ import annotations

from pathlib import Path

# BASE_DIR apunta a la raíz del proyecto (3 niveles arriba desde app/common/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_PATH = BASE_DIR / "templates"
STATIC_PATH = BASE_DIR / "static"
DATA_PATH = BASE_DIR / "data/SaratogaHouses.csv"
ARTIFACTS_PATH = BASE_DIR / "model/artifacts"

