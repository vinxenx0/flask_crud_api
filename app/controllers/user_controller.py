from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserController:
    """ Controlador unificado para API y Web """

    @staticmethod
    @jwt_required(optional=True)
    def get_users():
        if not get_jwt_identity() and not current_user.is_authenticated:
            if request.accept_mimetypes.best == "application/json":
                return {"message": "Unauthorized"}, 401
            return redirect(url_for("auth_views.login"))  # 🔄 Redirección solo en Web

        users = User.query.all()
        if request.accept_mimetypes.best == "application/json":
            return [{"id": u.id, "username": u.username, "role": u.role} for u in users], 200
        return render_template("users.html", users=users)  # 🎨 Para frontend


    @staticmethod
    @jwt_required(optional=True)
    @login_required
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            if request.accept_mimetypes.best == "application/json":
                return {"message": "User not found"}, 404
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("user_views.dashboard"))

        if request.accept_mimetypes.best == "application/json":
            return {"id": user.id, "username": user.username, "role": user.role}, 200
        return render_template("edit_user.html", user=user)  # 🎨 Para frontend

    @staticmethod
    @jwt_required(optional=True)
    @login_required
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404 if request.is_json else redirect(url_for("dashboard_views.dashboard"))

        if request.method == "POST":  # 🎨 Desde formulario HTML
            user.username = request.form.get("username", user.username)
            user.password = generate_password_hash(request.form.get("password", user.password))
            user.role = request.form.get("role", user.role)
        else:  # API JSON
            data = request.get_json()
            if "username" in data:
                user.username = data["username"]
            if "password" in data:
                user.password = generate_password_hash(data["password"])
            if "role" in data:
                user.role = data["role"]

        db.session.commit()

        if request.accept_mimetypes.best == "application/json":
            return {"message": "User updated successfully"}, 200

        flash("Usuario actualizado con éxito", "success")
        return redirect(url_for("user_views.dashboard"))

    @staticmethod
    @jwt_required(optional=True)
    @login_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404 if request.is_json else redirect(url_for("dashboard_views.dashboard"))

        db.session.delete(user)
        db.session.commit()

        if request.accept_mimetypes.best == "application/json":
            return {"message": "User deleted"}, 200

        flash("Usuario eliminado con éxito", "success")
        return redirect(url_for("user_views.dashboard"))
    
