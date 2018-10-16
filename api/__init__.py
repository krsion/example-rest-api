from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from pony.orm import Database

db = Database('sqlite', '../db.sqlite', create_db=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)
ma = Marshmallow(app)

jwt = JWTManager(app)

from .post import PostResource, PostsResource
from .user import UserResource, UsersResource
from .login import LoginResource

db.generate_mapping()

api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<name>')
api.add_resource(PostsResource, '/users/<name>/posts')
api.add_resource(PostResource, '/users/<name>/posts/<id>')
api.add_resource(LoginResource, '/login')
