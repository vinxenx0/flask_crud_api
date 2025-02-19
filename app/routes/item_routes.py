from flask import Blueprint
from flask_restful import Api, Resource
from app.controllers.item_controller import ItemController

bp = Blueprint("item", __name__, url_prefix="/items")
api = Api(bp)

class ItemList(Resource):
    def get(self):
        return ItemController.get_items()

    def post(self):
        return ItemController.create_item()

class ItemDetail(Resource):
    def get(self, item_id):
        return ItemController.get_item(item_id)

    def put(self, item_id):
        return ItemController.update_item(item_id)

    def delete(self, item_id):
        return ItemController.delete_item(item_id)

api.add_resource(ItemList, "/")
api.add_resource(ItemDetail, "/<int:item_id>")
