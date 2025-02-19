from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserController:
    @staticmethod
    @jwt_required()
    def get_users():
        users = User.query.all()
        return [{"id": u.id, "username": u.username, "role": u.role} for u in users], 200

    @staticmethod
    @jwt_required()
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "username": user.username, "role": user.role}, 200

    @staticmethod
    @jwt_required()
    def update_user(user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        if "username" in data:
            user.username = data["username"]
        if "password" in data:
            user.password = generate_password_hash(data["password"])
        if "role" in data:
            user.role = data["role"]

        db.session.commit()
        return {"message": "User updated successfully"}, 200

    @staticmethod
    @jwt_required()
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
