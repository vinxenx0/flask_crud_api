from flask import Blueprint
from flask_restful import Api, Resource
from app.controllers.auth_controller import AuthController

bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(bp)

class Register(Resource):
    def post(self):
        return AuthController.register()

class Login(Resource):
    def post(self):
        return AuthController.login()

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
