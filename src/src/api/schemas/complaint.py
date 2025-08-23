from marshmallow import Schema, fields

class ComplaintCreateSchema(Schema):
    reporter_id = fields.Int(required=True)
    target_user_id = fields.Int(allow_none=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)

class ComplaintUpdateStatusSchema(Schema):
    status = fields.Str(required=True)

class ComplaintResponseSchema(Schema):
    id = fields.Int()
    reporter_id = fields.Int()
    target_user_id = fields.Int(allow_none=True)
    title = fields.Str()
    content = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
