from flask_jwt_extended import get_jwt_identity
from flask_restful import abort

from models import User


def user_exists(func):
    def wrapper(self, name):
        user = User.get_user(get_jwt_identity())
        if not user:
            abort(404)
        return func(self, name)

    return wrapper


def self_or_admin(func):
    def wrapper(self, name):
        if get_jwt_identity() not in [name, 'admin']:
            abort(403)
        return func(self, name)

    return wrapper
