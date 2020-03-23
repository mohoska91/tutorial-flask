import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.itemmodel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field is required")
    parser.add_argument('store_id', type=float, required=True, help="This store_id is required")

    @jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json, 200
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {"message": f"Item with name '{name}' already exists."}, 400
        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred during inserting the item."}, 500
        return item.json, 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted."}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(**data)
        else:
            item.price = data["price"]
        item.save_to_db()
        return item.json, 200


class Items(Resource):
    @jwt_required()
    def get(self):
        return {"items": [item.json for item in ItemModel.query.all()]}
