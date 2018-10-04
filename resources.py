from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource, abort
from werkzeug.security import check_password_hash

from auth import self_or_admin, user_exists
from models import User
from serialization import UserSchema, LoginSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserResource(Resource):
    def get(self, name):
        user = User.get_user(name)
        if not user:
            abort(404)
        return user_schema.dump(user).data

    @jwt_required
    @user_exists
    @self_or_admin
    def put(self, name):
        data = user_schema.load(request.get_json()).data
        User.update_user(name, **data)
        return user_schema.dump(User.get_user(name))

    @jwt_required
    @user_exists
    @self_or_admin
    def delete(self, name):
        User.delete_user(name)
        return get_jwt_identity()


class UsersResource(Resource):
    def get(self):
        return users_schema.dump(User.get_all_users_list()).data

    def post(self):
        loaded = user_schema.load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        return user_schema.dump(User.add_user(**loaded.data))


class LoginResource(Resource):
    def post(self):
        loaded = LoginSchema().load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        user = User.get_user(loaded.data['name'])
        if not check_password_hash(user.password, loaded.data['password']):
            abort(401, message='Incorrect password')
        return create_access_token(identity=loaded.data['name'])
