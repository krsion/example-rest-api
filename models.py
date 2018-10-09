from pony.orm import PrimaryKey, Required, Set, db_session
from werkzeug.security import generate_password_hash

from app import db


class User(db.Entity):
    name = PrimaryKey(str)
    password = Required(str)
    posts = Set('Post', reverse='user')

    @staticmethod
    @db_session
    def get_user(name):
        return User.get(name=name)

    @staticmethod
    @db_session
    def get_all_users_list():
        return User.select()[:]

    @staticmethod
    @db_session
    def add_user(**kwargs):
        kwargs['password'] = generate_password_hash(kwargs['password'])
        return User(**kwargs)

    @staticmethod
    @db_session
    def update_user(name, **kwargs):
        user = User.get(name=name)
        kwargs['password'] = generate_password_hash(kwargs['password'])
        user.set(**kwargs)

    @staticmethod
    @db_session
    def delete_user(name):
        User.get(name=name).delete()


class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User, reverse='posts')
    text = Required(str)


db.generate_mapping(create_tables=True)