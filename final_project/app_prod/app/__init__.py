# app/__init__.py

import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()

def create_app():
    # Cargar variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    swagger = Swagger(app, config=app.config['SWAGGER'], template=app.config['SWAGGER_TEMPLATE'])

    # Importar modelos para que SQLAlchemy los registre
    from app import models

    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes.airlines import airlines_bp
    from app.routes.airports import airports_bp
    from app.routes.flights import flights_bp  # Si tienes rutas para vuelos

    app.register_blueprint(airlines_bp, url_prefix='/api/airlines')
    app.register_blueprint(airports_bp, url_prefix='/api/airports')
    app.register_blueprint(flights_bp, url_prefix='/api/flights')

    # Ruta principal
    @app.route('/')
    def index():
        """
        Página de Inicio
        ---
        responses:
          200:
            description: Página de inicio
        """
        return render_template('index.html')

    # Configurar logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Aplicación iniciada')

    return app
