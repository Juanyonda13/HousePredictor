from __future__ import annotations

import json
from typing import Any, Dict

import pandas as pd

from app.common.config import DATA_PATH
from model.domain.analisis_distribuciones import AnalisisEstadistico


def _convertir_numpy_a_nativo(obj):
    """Convierte valores de NumPy a tipos nativos para JSON."""
    import numpy as np

    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _convertir_numpy_a_nativo(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_convertir_numpy_a_nativo(v) for v in obj]
    return obj


class StatsService:
    """Maneja operaciones basadas en el dataset SaratogaHouses."""

    def _cargar_dataset(self) -> pd.DataFrame:
        if not DATA_PATH.exists():
            raise FileNotFoundError("Datos no disponibles. Ejecuta el análisis estadístico primero.")
        return pd.read_csv(DATA_PATH)

    def obtener_muestra_casas(self, max_registros: int = 100) -> str:
        try:
            df = self._cargar_dataset()
        except FileNotFoundError:
            return json.dumps([])

        muestra = df.sample(n=min(max_registros, len(df)), random_state=42)
        return json.dumps(muestra.to_dict("records"))

    def obtener_estadisticas_dataset(self) -> Dict[str, Any]:
        try:
            df = self._cargar_dataset()
        except FileNotFoundError as exc:
            return {"error": str(exc)}

        return {
            "total_casas": len(df),
            "precio_promedio": float(df["precio"].mean()),
            "precio_min": float(df["precio"].min()),
            "precio_max": float(df["precio"].max()),
            "precio_mediana": float(df["precio"].median()),
            "metros_promedio": float(df["metros_totales"].mean()),
            "antiguedad_promedio": float(df["antiguedad"].mean()),
            "dormitorios_promedio": float(df["dormitorios"].mean()),
        }

    def generar_analisis_estadistico(self) -> Dict[str, Any]:
        try:
            analizador = AnalisisEstadistico()
            analizador.cargar_datos()
            analisis = analizador.generar_analisis_completo()
            analisis = _convertir_numpy_a_nativo(analisis)
            return {
                "error": None,
                "analisis": analisis,
                "nota": (
                    "Estos análisis se realizan SOLO para fines académicos/estudio y NO interfieren con la "
                    "predicción final del precio de las viviendas."
                ),
            }
        except FileNotFoundError as exc:
            return {"error": str(exc)}
        except Exception as exc:  # pragma: no cover - logging
            return {"error": f"Error al generar análisis: {exc}"}

