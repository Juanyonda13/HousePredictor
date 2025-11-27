from pathlib import Path

from flask import Flask, render_template

from .routes.api import api_bp
from .routes.web import web_bp
from .services.model_service import ModelService
from .services.stats_service import StatsService


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config["SECRET_KEY"] = "tu-clave-secreta-aqui"

    # Services (comparten el mismo ciclo de vida que la app)
    app.extensions["model_service"] = ModelService()
    app.extensions["stats_service"] = StatsService()

    # Blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Error handlers
    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return {"error": "Error interno del servidor"}, 500

    return app

