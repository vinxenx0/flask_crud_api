from flask_bootstrap import Bootstrap5
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flasgger import Swagger
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask_login import LoginManager

migrate = Migrate()

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()
bootstrap = Bootstrap5()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    bootstrap = Bootstrap5(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_views.login"  # Redirigir si no está autenticado


    with app.app_context():
        #print("🔄 Creando tablas en la base de datos...")
        db.create_all()
        #print("✅ Tablas creadas correctamente.")
        #print(app.config["SQLALCHEMY_DATABASE_URI"])

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Cargar usuario desde la DB
 
    from app.routes import auth_routes, user_routes, item_routes
    from app.views import auth_views, user_views
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(item_routes.bp)
    app.register_blueprint(auth_views.auth_views) 
    app.register_blueprint(user_views.user_views)
    
    return app