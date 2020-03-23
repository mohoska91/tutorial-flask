import os

from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt import JWT
from flask_restful import Api

from db import db
from resources.item import Item, Items
from resources.store import Store, StoreList
from security import authenticate, identity
from resources.user import UserRegister

items = []


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "a very secure key"

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)


@jwt.auth_response_handler
def customize_aut_response(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api = Api(app)
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
