from flask import Blueprint, render_template

from app.controllers.stats_controller import StatsController


web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/mapa")
def mapa():
    casas_json = StatsController.dataset_sample_json()
    return render_template("mapa.html", casas=casas_json)


@web_bp.route("/analisis-estadistico")
def analisis_estadistico():
    return render_template("analisis_estadistico.html")

