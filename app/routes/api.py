from flask import Blueprint, jsonify, request

from app.controllers.prediction_controller import PredictionController
from app.controllers.stats_controller import StatsController
from app.common.decorators import handle_api_errors


api_bp = Blueprint("api", __name__)


@api_bp.route("/predecir", methods=["POST"])
@handle_api_errors
def api_predecir():
    datos = request.get_json()
    paso_a_paso = request.args.get("paso_a_paso", "false").lower() == "true"
    response = PredictionController.predict(datos, incluir_paso_a_paso=paso_a_paso)
    return jsonify(response)


@api_bp.route("/status-modelos", methods=["GET"])
def api_status_modelos():
    return jsonify(PredictionController.status())


@api_bp.route("/datos-ejemplo", methods=["GET"])
def api_datos_ejemplo():
    return jsonify(PredictionController.sample_data())


@api_bp.route("/estadisticas", methods=["GET"])
def api_estadisticas():
    return jsonify(StatsController.dataset_stats())


@api_bp.route("/modelo-info", methods=["GET"])
def api_modelo_info():
    info = PredictionController.model_info()
    return jsonify(info)


@api_bp.route("/analisis-estadistico", methods=["GET"])
@handle_api_errors
def api_analisis_estadistico():
    return jsonify(StatsController.academic_analysis())


@api_bp.route("/comparar", methods=["POST"])
@handle_api_errors
def api_comparar():
    lista_casas = request.get_json()
    resultado = PredictionController.compare(lista_casas)
    return jsonify(resultado)


