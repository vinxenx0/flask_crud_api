from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.item import Item

class ItemController:
    @staticmethod
    @jwt_required()
    def get_items():
        items = Item.query.all()
        return [{"id": i.id, "name": i.name, "description": i.description} for i in items], 200

    @staticmethod
    @jwt_required()
    def get_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"message": "Item not found"}, 404
        return {"id": item.id, "name": item.name, "description": item.description}, 200

    @staticmethod
    @jwt_required()
    def create_item():
        data = request.get_json(silent=True)
        print("DEBUG request.get_json():", data)  # 👈 Verifica qué JSON está llegando realmente

        if not data or not isinstance(data, dict):
            return {"message": "Invalid or missing JSON data"}, 400

        if "name" not in data or "description" not in data:
            return {"message": "Both 'name' and 'description' are required"}, 400

        user_id = int(get_jwt_identity())  # 👈 Convertir `user_id` a entero

        item = Item(name=data["name"], description=data["description"], user_id=user_id)

        db.session.add(item)
        db.session.commit()

        return {"message": "Item created", "id": item.id}, 201  # ✅ Devolver también el `id`




    @staticmethod
    @jwt_required()
    def update_item(item_id):
        data = request.get_json()
        item = Item.query.get(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        if "name" in data:
            item.name = data["name"]
        if "description" in data:
            item.description = data["description"]

        db.session.commit()
        return {"message": "Item updated successfully"}, 200

    @staticmethod
    @jwt_required()
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200