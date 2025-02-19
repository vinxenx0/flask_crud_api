from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flasgger import Swagger
from config import DevelopmentConfig

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    with app.app_context():
        db.create_all()  # 👈 Crear las tablas si no existen
 
    from app.routes import auth_routes, user_routes, item_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(item_routes.bp)

    return app