from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import fields
from pony.orm import PrimaryKey, Required, db_session

from . import db, api, ma
from .user import User, UserSchema
from .auth import user_exists, self_or_admin


class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    text = Required(str)

    @staticmethod
    def get_post(id):
        return Post.get(id=id)

    @staticmethod
    def get_all_users_posts_list(name):
        return User.get_user(name).posts

    @staticmethod
    def add_post(**kwargs):
        return Post(**kwargs)

    @staticmethod
    def update_post(id, **kwargs):
        post = Post.get(id=id)
        post.set(**kwargs)

    @staticmethod
    def delete_post(id):
        User.get(id=id).delete()


class PostSchema(ma.Schema):
    id = fields.Integer()
    author = fields.Nested(UserSchema, only=['name'])
    text = fields.String()
    _links = ma.Hyperlinks({
        'self': ma.URLFor('postresource', id='<id>', name='<author.name>'),
        'collection': ma.URLFor('postsresource', name='<author.name>')
    })

    class Meta:
        ordered = True


def post_exists(id):
    return bool(Post.get_post(id))


class PostResource(Resource):
    @db_session
    def get(self, name, id):
        if not user_exists(name) or not post_exists(id):
            abort(404)
        return PostSchema().dump(Post.get_post(id)).data

    @db_session
    @jwt_required
    def put(self, name, id):
        if not user_exists(name) or not post_exists(id):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        data = PostSchema().load(request.get_json()).data
        Post.update_post(id, **data)
        return PostSchema().dump(Post.get_post(id))

    @db_session
    @jwt_required
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
        return PostSchema(many=True).dump(User.get_user(name).posts)

    @db_session
    @jwt_required
    def post(self, name):
        if not user_exists(name):
            abort(404)
        if not self_or_admin(name):
            abort(403)
        loaded = PostSchema(exclude=('id','author')).load(request.get_json())
        if loaded.errors:
            abort(400, message=loaded.errors)
        post = Post.add_post(**loaded.data, author=User.get_user(name))
        return '', 201
