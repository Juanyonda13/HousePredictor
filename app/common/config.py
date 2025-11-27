from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PATH = BASE_DIR / "templates"
STATIC_PATH = BASE_DIR / "static"
DATA_PATH = BASE_DIR / "data/SaratogaHouses.csv"
ARTIFACTS_PATH = BASE_DIR / "model/artifacts"

