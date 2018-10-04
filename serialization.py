from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)
