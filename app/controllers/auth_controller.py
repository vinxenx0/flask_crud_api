from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from app.utils.token_manager import generate_token

class AuthController:
    @staticmethod
    def register():
        if request.is_json:  # 📌 Para API
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return {"message": "Invalid or missing JSON data"}, 400
            if "username" not in data or "password" not in data:
                return {"message": "Username and password are required"}, 400

            existing_user = User.query.filter_by(username=data["username"]).first()
            if existing_user:
                return {"message": "Username already exists"}, 409

            hashed_password = generate_password_hash(data["password"])
            user = User(username=data["username"], password=hashed_password, role=data.get("role", "user"))
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully"}, 201

        # 📌 Para Web (Formulario HTML)
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            role = request.form.get("role", "user")

            if not username or not password:
                flash("El usuario y la contraseña son obligatorios", "danger")
                return redirect(url_for("auth_views.register"))

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("El usuario ya existe", "danger")
                return redirect(url_for("auth_views.register"))

            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password, role=role)
            db.session.add(user)
            db.session.commit()

            flash("Usuario registrado con éxito", "success")
            return redirect(url_for("auth_views.login"))

        return render_template("register.html")  # 🎨 Formulario de registro

    @staticmethod
    def login():
        if request.is_json:
            data = request.get_json()
            user = User.query.filter_by(username=data["username"]).first()

            if user and check_password_hash(user.password, data["password"]):
                token = generate_token(user)
                return {"token": token}, 200  # 👈 Siempre usar jsonify()

            return {"message": "Invalid credentials"}, 401

        # 🎨 Si es web, usa sesión en lugar de JWT
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login exitoso", "success")
            return redirect(url_for("dashboard_views.dashboard"))

        flash("Usuario o contraseña incorrectos", "danger")
        return redirect(url_for("auth_views.login"))
