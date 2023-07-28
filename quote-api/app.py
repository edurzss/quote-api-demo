import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv, find_dotenv

from resources.quotes import bp as quotes_bp

load_dotenv(find_dotenv(), override=True)

def create_app():
    app = Flask(__name__)
    # API data
    app.config["API_TITLE"] = "Quote API" 
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/v1"
    # Swaqgger UI docs
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" 
    # Connect flask_smorest extension to the Flask app
    api = Api(app)

    # Register blueprints
    api.register_blueprint(quotes_bp)
    return app