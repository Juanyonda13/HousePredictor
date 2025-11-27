from __future__ import annotations

from typing import Any, Dict, List

from flask import current_app


class PredictionController:
    @staticmethod
    def predict(datos: Dict[str, Any], incluir_paso_a_paso: bool) -> Dict[str, Any]:
        model_service = current_app.extensions["model_service"]
        if not datos:
            raise ValueError("No se recibieron datos")
        return model_service.predecir(datos, incluir_paso_a_paso=incluir_paso_a_paso)

    @staticmethod
    def compare(lista_casas: List[Dict[str, Any]]) -> Dict[str, Any]:
        model_service = current_app.extensions["model_service"]
        if not isinstance(lista_casas, list):
            raise ValueError("Se esperaba una lista de casas")
        return model_service.comparar_casas(lista_casas)

    @staticmethod
    def status() -> Dict[str, Any]:
        model_service = current_app.extensions["model_service"]
        return model_service.estado_modelos()

    @staticmethod
    def sample_data() -> Dict[str, Any]:
        model_service = current_app.extensions["model_service"]
        return model_service.datos_ejemplo()

    @staticmethod
    def model_info() -> Dict[str, Any]:
        model_service = current_app.extensions["model_service"]
        return model_service.informacion_modelos()

