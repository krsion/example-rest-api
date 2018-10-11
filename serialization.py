from marshmallow import fields

from app import ma


class LoginSchema(ma.Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(ma.Schema):
    name = fields.String(required=True)
    posts = fields.Nested('PostSchema', many=True, exclude=('author',))
    _links = ma.Hyperlinks({
        'self': ma.URLFor('userresource', name='<name>'),
        'collection': ma.URLFor('usersresource')
    })

    class Meta:
        ordered = True


class PostSchema(ma.Schema):
    id = fields.Integer(required=True)
    author = fields.Nested(UserSchema, only=['name'])
    text = fields.String()
    _links = ma.Hyperlinks({
        'self': ma.URLFor('postresource', id='<id>', name='<author.name>'),
        'collection': ma.URLFor('postsresource', name='<author.name>')
    })

    class Meta:
        ordered = True
