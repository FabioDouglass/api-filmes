from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True, 
                "model_filter": lambda tag: True, 
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "APIs Filmes",
            "description": "API para gerenciamento de um acervo de filmes",
            "version": "1.0.0",
        },
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    CORS(app)

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'db', 'filmes.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        os.makedirs(os.path.join(basedir, '..', 'db'), exist_ok=True)
        db.create_all()

    return app