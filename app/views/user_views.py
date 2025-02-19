from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.item import Item
from app import db
from werkzeug.security import generate_password_hash

user_views = Blueprint("user_views", __name__)

@user_views.route("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for("auth_views.login"))

    items = Item.query.filter_by(user_id=user_id).all()
    users = User.query.all() if user.role == "admin" else None

    return render_template("dashboard.html", user=user, items=items, users=users)

@user_views.route("/user/update", methods=["POST"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    new_username = request.form.get("username")
    new_password = request.form.get("password")

    if new_username:
        user.username = new_username
    if new_password:
        user.password = generate_password_hash(new_password)

    db.session.commit()
    flash("Perfil actualizado", "success")
    return redirect(url_for("user_views.dashboard"))

@user_views.route("/user/delete", methods=["POST"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    
    flash("Cuenta eliminada", "danger")
    return redirect(url_for("auth_views.login"))

@user_views.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@jwt_required()
def admin_delete_user(user_id):
    current_user = User.query.get(get_jwt_identity())

    if current_user.role != "admin":
        flash("Acceso denegado", "danger")
        return redirect(url_for("user_views.dashboard"))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado", "success")
    
    return redirect(url_for("user_views.dashboard"))
