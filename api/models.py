from pony.orm import PrimaryKey, Required, Set
from werkzeug.security import generate_password_hash

from . import db


class User(db.Entity):
    name = PrimaryKey(str, auto=True)
    password = Required(str)
    posts = Set('Post')

    @staticmethod
    def get_user(name):
        return User.get(name=name)

    @staticmethod
    def get_all_users_list():
        return User.select()[:]

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


class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    text = Required(str)

    @staticmethod
    def get_post(id):
        return Post.get(id=id)

    @staticmethod
    def get_all_users_posts_list(name):
        return User.get_user(name).posts[:]

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


db.generate_mapping()
