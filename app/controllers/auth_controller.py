from flask import request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User
from app.utils.token_manager import generate_token

class AuthController:
    @staticmethod
    def register():
        data = request.get_json(silent=True)

        if not data or not isinstance(data, dict):
            return {"message": "Invalid or missing JSON data"}, 400  # ✅ Devolver dict, NO `jsonify()`

        if "username" not in data or "password" not in data:
            return {"message": "Username and password are required"}, 400

        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return {"message": "Username already exists"}, 409  # ✅ Respuesta en formato `dict`

        hashed_password = generate_password_hash(data["password"])
        user = User(username=data["username"], password=hashed_password, role=data.get("role", "user"))
        
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201  # ✅ Respuesta en formato `dict`




    @staticmethod
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            token = generate_token(user)
            return {"token": token}, 200  # 👈 Siempre usar jsonify()

        return {"message": "Invalid credentials"}, 401
