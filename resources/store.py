from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.storemodel import StoreModel


class Store(Resource):
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json
        return {"message": "Store not found"}, 404

    @jwt_required
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store already exists."}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An arror occurd during creating store"}, 500

        return store.json, 201

    @jwt_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted."}, 200


class StoreList(Resource):
    @jwt_required
    def get(self):
        return {"stores": [item.json for item in StoreModel.find_all()]}
