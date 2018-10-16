from flask_jwt_extended import get_jwt_identity

from api.models import User


def user_exists(name):
    return bool(User.get_user(name))


def self_or_admin(name):
    return get_jwt_identity() in [name, 'admin']
