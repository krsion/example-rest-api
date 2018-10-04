from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from pony.orm import Database

db = Database('sqlite', 'db.sqlite', create_db=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)

jwt = JWTManager(app)

from resources import UserResource, UsersResource, LoginResource

api.add_resource(UserResource, '/users/<name>')
api.add_resource(UsersResource, '/users')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run()
