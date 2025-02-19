from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required, current_user
from app import db
from app.models.item import Item

class ItemController:
    @staticmethod
    @jwt_required(optional=True)
    def get_items():
        if not get_jwt_identity() and not current_user.is_authenticated:
            if request.accept_mimetypes.best == "application/json":
                return {"message": "Unauthorized"}, 401
            return redirect(url_for("auth_views.login"))  # 🔄 Redirección solo para Web

        items = Item.query.all()
        if request.accept_mimetypes.best == "application/json":
            return [{"id": i.id, "name": i.name, "description": i.description} for i in items], 200
        return render_template("items.html", items=items)  # 🎨 Para frontend


    @staticmethod
    @jwt_required(optional=True)
    @login_required
    def create_item():
        if request.method == "POST":  # 🎨 HTML Form
            name = request.form.get("name")
            description = request.form.get("description")
        else:  # API JSON
            data = request.get_json()
            name = data.get("name")
            description = data.get("description")

        if not name or not description:
            return {"message": "Both 'name' and 'description' are required"}, 400

        item = Item(name=name, description=description, user_id=current_user.id)

        db.session.add(item)
        db.session.commit()

        if request.accept_mimetypes.best == "application/json":
            return {"message": "Item created", "id": item.id}, 201

        flash("Ítem creado con éxito", "success")
        return redirect(url_for("user_views.dashboard"))

    @staticmethod
    @jwt_required(optional=True)
    @login_required
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"message": "Item not found"}, 404 if request.is_json else redirect(url_for("dashboard_views.dashboard"))

        db.session.delete(item)
        db.session.commit()

        if request.accept_mimetypes.best == "application/json":
            return {"message": "Item deleted"}, 200

        flash("Ítem eliminado con éxito", "success")
        return redirect(url_for("user_views.dashboard"))
