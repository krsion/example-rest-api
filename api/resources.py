from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource, abort
from pony.orm import db_session
from werkzeug.security import check_password_hash

from . import api
from .auth import self_or_admin, user_exists
from .models import User, Post
from .serialization import UserSchema, LoginSchema, PostSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class UserResource(Resource):
    @db_session
    def get(self, name):
        user = User.get_user(name)
        if not user:
            abort(404)
        return user_schema.dump(user).data

    @db_session
    @jwt_required
    def put(self, name):
        if not user_exists(name):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        data = user_schema.load(request.get_json()).data
        User.update_user(name, **data)
        return user_schema.dump(User.get_user(name))

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
        return users_schema.dump(User.get_all_users_list()).data

    @db_session
    def post(self):
        loaded = user_schema.load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        User.add_user(**loaded.data)
        return '', 201, {'location': api.url_for(UserResource, name=loaded.data['name'])}


def post_exists(id):
    return bool(Post.get_post(id))


class PostResource(Resource):
    @db_session
    def get(self, name, id):
        if not user_exists(name) or not post_exists(id):
            abort(404)
        return post_schema.dump(Post.get_post(id)).data

    @db_session
    def put(self, name, id):
        if not user_exists(name) or not post_exists(id):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        data = post_schema.load(request.get_json()).data
        Post.update_post(id, **data)
        return post_schema.dump(Post.get_post(id))

    @db_session
    def delete(self, name, id):
        if not user_exists(name) or not post_exists(id):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        Post.delete_post(id)
        return {}, 204


class PostsResource(Resource):
    @db_session
    def get(self, name):
        if not user_exists(name):
            abort(404)
        return posts_schema.dump(Post.get_all_users_posts_list(name))

    @db_session
    def post(self, name):
        if not user_exists(name):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        loaded = post_schema.load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        post = Post.add_post(**loaded.data)
        return '', 201, {'location': api.url_for(PostResource, id=post.id, name=name)}


class LoginResource(Resource):
    @db_session
    def post(self):
        loaded = LoginSchema().load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        user = User.get_user(loaded.data['name'])
        if not check_password_hash(user.password, loaded.data['password']):
            abort(401, message='Incorrect password')
        return create_access_token(identity=loaded.data['name'])
