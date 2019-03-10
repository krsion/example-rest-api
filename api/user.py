from flask import request
from flask_jwt_extended import jwt_required, get_raw_jwt
from flask_restful import Resource, abort
from marshmallow import fields
from pony.orm import PrimaryKey, Required, Set, db_session
from werkzeug.security import generate_password_hash

from . import db, api, ma


class User(db.Entity):
    name = PrimaryKey(str, auto=True)
    password = Required(str)
    posts = Set('Post')

    @staticmethod
    def get_user(name):
        return User.get(name=name)

    @staticmethod
    def get_all_users_list():
        return User.select()

    @staticmethod
    def add_user(**kwargs):
        kwargs['password'] = generate_password_hash(kwargs['password'])
        return User(**kwargs)

    @staticmethod
    def update_user(name, **kwargs):
        user = User.get(name=name)
        kwargs['password'] = generate_password_hash(kwargs['password'])
        user.set(**kwargs)

    @staticmethod
    def delete_user(name):
        User.get(name=name).delete()


class UserSchema(ma.Schema):
    name = fields.String(required=True)
    password = fields.String()
    posts = fields.Nested('PostSchema', many=True, exclude=('author',))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('userresource', name='<name>'),
        'collection': ma.URLFor('usersresource'),
        #'posts': ma.URLFor('postsresource', name='<name>')
    })

    class Meta:
        ordered = True


from .auth import user_exists, self_or_admin


class UserResource(Resource):
    @db_session
    def get(self, name):
        user = User.get_user(name)
        if not user:
            abort(404)
        return UserSchema(exclude=['password']).dump(user).data

    @db_session
    @jwt_required
    def put(self, name):
        if not user_exists(name):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        data = UserSchema().load(request.get_json()).data
        User.update_user(name, **data)
        return UserSchema(exclude=['password']).dump(User.get_user(name))

    @db_session
    @jwt_required
    def delete(self, name):
        if not user_exists(name):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        User.delete_user(name)
        return {}, 204


class UsersResource(Resource):
    @db_session
    def get(self):
        return UserSchema(many=True, exclude=['password']).dump(User.get_all_users_list()).data

    @db_session
    def post(self):
        loaded = UserSchema().load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        User.add_user(**loaded.data)
        return '', 201, {'location': api.url_for(UserResource, name=loaded.data['name'])}
