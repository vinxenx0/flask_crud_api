from flask import Blueprint
from flask_restful import Api, Resource
from app.controllers.user_controller import UserController

bp = Blueprint("user", __name__, url_prefix="/users")
api = Api(bp)

class UserList(Resource):
    def get(self):
        return UserController.get_users()

class UserDetail(Resource):
    def get(self, user_id):
        return UserController.get_user(user_id)

    def put(self, user_id):
        return UserController.update_user(user_id)

    def delete(self, user_id):
        return UserController.delete_user(user_id)

api.add_resource(UserList, "/")
api.add_resource(UserDetail, "/<int:user_id>")
