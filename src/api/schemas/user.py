from marshmallow import Schema, fields

class UserRequestSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True) 