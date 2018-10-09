from marshmallow import Schema, fields


class LoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)


class PostSchema(Schema):
    id = fields.Integer(required=True)
    user = fields.String(required=True)
    text = fields.String(required=True)
