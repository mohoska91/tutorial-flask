import os

from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from db import db
from resources.item import Item, Items
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

items = []


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = "a very secure key"

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return {"is_admin": identity == 1}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "The token has expired!",
            "error": "token_expired"
        }
    ), 401

@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "The token is invalid!",
            "error": "invalid_expired"
        }
    ), 401

@jwt.unauthorized_loader
def invalid_token_callback():
    return jsonify(
        {
            "description": "Not authorized!",
            "error": "not_authorized"
        }
    ), 403


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify(
        {
            "description": "The token is not fresh!",
            "error": "not_fresh_token"
        }
    ), 401


@jwt.revoked_token_loader
def needs_fresh_token_callback():
    return jsonify(
        {
            "description": "The token is revoked!",
            "error": "revoked_token"
        }
    ), 401


@jwt.token_in_blacklist_loader
def check_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api = Api(app)
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
