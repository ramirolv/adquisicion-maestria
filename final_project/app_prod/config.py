# config.py

import os

class Config:
    # Cargar variables de entorno
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT', '3306')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Swagger
    SWAGGER = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # Incluir todas las reglas
                "model_filter": lambda tag: True,  # Incluir todos los modelos
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": "API de Gestión de Vuelos",
            "description": "Esta es la documentación de la API para gestionar aerolíneas, aeropuertos y vuelos.",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": [
            "http",
            "https"
        ],
    }
