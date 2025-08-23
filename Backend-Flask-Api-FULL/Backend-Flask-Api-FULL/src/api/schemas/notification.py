from marshmallow import Schema, fields

class NotificationCreateSchema(Schema):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    message = fields.Str(required=True)

class NotificationResponseSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    title = fields.Str()
    message = fields.Str()
    is_read = fields.Bool()
    created_at = fields.DateTime()
