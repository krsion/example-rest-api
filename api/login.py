from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, abort
from marshmallow import fields
from pony.orm import db_session
from werkzeug.security import check_password_hash

from . import ma
from .user import User


class LoginSchema(ma.Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)


class LoginResource(Resource):
    @db_session
    def post(self):
        loaded = LoginSchema().load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        user = User.get_user(loaded.data['name'])
        if not check_password_hash(user.password, loaded.data['password']):
            abort(401, message='Incorrect password')
        return create_access_token(identity=user.name)
