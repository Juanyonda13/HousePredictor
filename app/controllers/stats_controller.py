from __future__ import annotations

from flask import current_app


class StatsController:
    @staticmethod
    def dataset_stats():
        stats_service = current_app.extensions["stats_service"]
        stats = stats_service.obtener_estadisticas_dataset()
        if "error" in stats:
            raise FileNotFoundError(stats["error"])
        return stats

    @staticmethod
    def dataset_sample_json():
        stats_service = current_app.extensions["stats_service"]
        return stats_service.obtener_muestra_casas()

    @staticmethod
    def academic_analysis():
        stats_service = current_app.extensions["stats_service"]
        resultado = stats_service.generar_analisis_estadistico()
        if resultado.get("error"):
            raise FileNotFoundError(resultado["error"])
        return resultado

