from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from app.common.config import ARTIFACTS_PATH
from model.domain.regresion_bayesiana import ModeloRegresionBayesiana
from model.domain.regresion_lineal import ModeloRegresionLineal


class ModelService:
    """Encapsula la lógica relacionada con los modelos estadísticos."""

    CAMPOS_NUMERICOS = [
        "metros_totales",
        "antiguedad",
        "precio_terreno",
        "metros_habitables",
        "universitarios",
        "dormitorios",
        "chimenea",
        "banyos",
        "habitaciones",
    ]

    def __init__(self) -> None:
        self.modelo_ols: Optional[ModeloRegresionLineal] = None
        self.modelo_bayes: Optional[ModeloRegresionBayesiana] = None
        self._cargar_modelos()

    # --------------------------------------------------------------------- #
    # Carga de modelos
    # --------------------------------------------------------------------- #
    def _cargar_modelos(self) -> None:
        self.modelo_ols = self._cargar_modelo_ols()
        self.modelo_bayes = self._cargar_modelo_bayes()

    def _cargar_modelo_ols(self) -> Optional[ModeloRegresionLineal]:
        try:
            modelo = ModeloRegresionLineal.cargar("model/artifacts/modelo_regresion_lineal.pkl")
            print("✅ Modelo de Regresión Lineal (OLS) cargado exitosamente")
            print(
                f"   R² = {modelo.modelo.rsquared:.4f} "
                f"({modelo.modelo.rsquared * 100:.2f}%)"
            )
            return modelo
        except FileNotFoundError:
            print("⚠️  Modelo OLS no encontrado. Ejecuta 'python3 analisis_estadistico.py' primero")
        return None

    def _cargar_modelo_bayes(self) -> Optional[ModeloRegresionBayesiana]:
        try:
            modelo = ModeloRegresionBayesiana.cargar("model/artifacts/modelo_regresion_bayesiana.pkl")
            print("✅ Modelo de Regresión Bayesiana cargado exitosamente")
            print(
                f"   R² = {modelo.modelo.rsquared:.4f} "
                f"({modelo.modelo.rsquared * 100:.2f}%)"
            )
            return modelo
        except FileNotFoundError:
            print("⚠️  Modelo Bayesiano no encontrado. Ejecuta 'python3 analisis_estadistico.py' primero")
            return None
        except Exception as exc:  # pragma: no cover - logging
            print(f"⚠️  Error cargando modelo bayesiano: {exc}")
            return None

    # --------------------------------------------------------------------- #
    # Utilidades
    # --------------------------------------------------------------------- #
    def has_any_model(self) -> bool:
        return self.modelo_ols is not None or self.modelo_bayes is not None

    @staticmethod
    def _coerce_numeric_fields(datos: Dict[str, Any]) -> Dict[str, Any]:
        parsed = datos.copy()
        for campo in ModelService.CAMPOS_NUMERICOS:
            if campo in parsed:
                parsed[campo] = float(parsed[campo])
        return parsed

    # --------------------------------------------------------------------- #
    # Casos de uso
    # --------------------------------------------------------------------- #
    def predecir(self, datos: Dict[str, Any], incluir_paso_a_paso: bool = False) -> Dict[str, Any]:
        datos = self._coerce_numeric_fields(datos)
        response: Dict[str, Any] = {"error": None, "modelos": {}}

        if self.modelo_ols:
            resultado_ols = self.modelo_ols.predecir(datos, incluir_paso_a_paso=incluir_paso_a_paso)
            response["modelos"]["ols"] = {
                "precio": resultado_ols["precio_estimado"],
                "ic_inferior": resultado_ols["ic_inferior_95"],
                "ic_superior": resultado_ols["ic_superior_95"],
                "modelo": resultado_ols["modelo"],
                "r2": resultado_ols["r2"],
                "tipo": "Frecuentista (OLS)",
                "intervalo_tipo": "Intervalo de Confianza",
            }
            if incluir_paso_a_paso and "paso_a_paso" in resultado_ols:
                response["modelos"]["ols"]["paso_a_paso"] = resultado_ols["paso_a_paso"]

        if self.modelo_bayes:
            resultado_bayes = self.modelo_bayes.predecir(
                datos, incluir_paso_a_paso=incluir_paso_a_paso
            )
            response["modelos"]["bayesiano"] = {
                "precio": resultado_bayes["precio_estimado"],
                "ic_inferior": resultado_bayes["ic_inferior_95"],
                "ic_superior": resultado_bayes["ic_superior_95"],
                "modelo": resultado_bayes["modelo"],
                "r2": resultado_bayes["r2"],
                "tipo": "Bayesiano (Teorema de Bayes)",
                "intervalo_tipo": resultado_bayes.get("tipo_intervalo", "Intervalo Creíble"),
            }
            if incluir_paso_a_paso and "paso_a_paso" in resultado_bayes:
                response["modelos"]["bayesiano"]["paso_a_paso"] = resultado_bayes["paso_a_paso"]

        if self.modelo_ols:
            principal = response["modelos"]["ols"]
        elif self.modelo_bayes:
            principal = response["modelos"]["bayesiano"]
        else:
            raise ValueError('Modelos no disponibles. Ejecuta "python3 analisis_estadistico.py" primero.')

        response.update(
            {
                "precio": principal["precio"],
                "ic_inferior": principal["ic_inferior"],
                "ic_superior": principal["ic_superior"],
                "modelo": principal["modelo"],
                "r2": principal["r2"],
            }
        )
        return response

    def estado_modelos(self) -> Dict[str, Any]:
        return {
            "ols": {
                "cargado": self.modelo_ols is not None,
                "trained": bool(self.modelo_ols and self.modelo_ols.trained),
                "variables": len(self.modelo_ols.variables) if self.modelo_ols else 0,
            },
            "bayesiano": {
                "cargado": self.modelo_bayes is not None,
                "trained": bool(self.modelo_bayes and self.modelo_bayes.trained),
                "variables": len(self.modelo_bayes.variables) if self.modelo_bayes else 0,
            },
        }

    def informacion_modelos(self) -> Dict[str, Any]:
        info: Dict[str, Any] = {"modelos": {}}

        if self.modelo_ols:
            info["modelos"]["ols"] = {
                "tipo_modelo": "Regresión Lineal Múltiple (OLS)",
                "metodologia": "Frecuentista (Estadística Clásica)",
                "framework": "statsmodels",
                "metricas": {
                    "r2": float(self.modelo_ols.modelo.rsquared),
                    "r2_ajustado": float(self.modelo_ols.modelo.rsquared_adj),
                    "rmse": float(np.sqrt(self.modelo_ols.modelo.mse_resid)),
                    "n_observaciones": int(self.modelo_ols.modelo.nobs),
                    "n_variables": len(self.modelo_ols.variables),
                },
                "variables": self.modelo_ols.variables,
            }

        if self.modelo_bayes:
            info["modelos"]["bayesiano"] = {
                "tipo_modelo": "Regresión Bayesiana",
                "metodologia": "Bayesiana (Teorema de Bayes)",
                "framework": "statsmodels (aproximación bayesiana)",
                "metricas": {
                    "r2": float(self.modelo_bayes.modelo.rsquared),
                    "r2_ajustado": float(self.modelo_bayes.modelo.rsquared_adj),
                    "rmse": float(np.sqrt(self.modelo_bayes.modelo.mse_resid)),
                    "n_observaciones": int(self.modelo_bayes.modelo.nobs),
                    "n_variables": len(self.modelo_bayes.variables),
                },
                "variables": self.modelo_bayes.variables,
                "prior": self.modelo_bayes.priors.get("tipo", "No informativo"),
            }

        if not info["modelos"]:
            return {"error": "Ningún modelo disponible"}

        return info

    def comparar_casas(self, lista_casas: List[Dict[str, Any]]) -> Dict[str, Any]:
        resultado = []

        for i, casa in enumerate(lista_casas, start=1):
            predicciones = {}
            if self.modelo_ols:
                pred_ols = self.modelo_ols.predecir(casa)
                predicciones["ols"] = {
                    "precio_predicho": float(pred_ols["precio_estimado"]),
                    "precio_formateado": f"${pred_ols['precio_estimado']:,.2f}",
                    "ic_inferior": float(pred_ols["ic_inferior_95"]),
                    "ic_superior": float(pred_ols["ic_superior_95"]),
                }
            if self.modelo_bayes:
                pred_bayes = self.modelo_bayes.predecir(casa)
                predicciones["bayesiano"] = {
                    "precio_predicho": float(pred_bayes["precio_estimado"]),
                    "precio_formateado": f"${pred_bayes['precio_estimado']:,.2f}",
                    "ic_inferior": float(pred_bayes["ic_inferior_95"]),
                    "ic_superior": float(pred_bayes["ic_superior_95"]),
                }

            resultado.append({"id": i, "casa": casa, "predicciones": predicciones})

        return {"total": len(resultado), "predicciones": resultado}

    @staticmethod
    def datos_ejemplo() -> Dict[str, Any]:
        return {
            "metros_totales": 0.49,
            "antiguedad": 15,
            "precio_terreno": 25000,
            "metros_habitables": 1592,
            "universitarios": 54,
            "dormitorios": 3,
            "chimenea": 1,
            "banyos": 1.5,
            "habitaciones": 8,
            "calefaccion": "hot air",
            "consumo_calefacion": "gas",
            "desague": "septic",
            "vistas_lago": "No",
            "nueva_construccion": "No",
            "aire_acondicionado": "No",
        }

