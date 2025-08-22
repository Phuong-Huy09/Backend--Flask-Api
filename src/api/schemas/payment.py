from marshmallow import Schema, fields, validate
from decimal import Decimal

class PaymentRequestSchema(Schema):
    """Schema for payment creation requests"""
    booking_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, places=2, validate=validate.Range(min=Decimal('0.01')))
    method = fields.Str(required=True, validate=validate.OneOf(['Card', 'Wallet', 'Bank']))
    provider_txn_id = fields.Str(required=False, allow_none=True)
    currency = fields.Str(required=False, allow_none=True, validate=validate.Length(equal=3))

class PaymentUpdateSchema(Schema):
    """Schema for payment status updates"""
    status = fields.Str(required=True, validate=validate.OneOf(['Authorized', 'Captured', 'Failed', 'Refunded']))

class PaymentResponseSchema(Schema):
    """Schema for payment responses"""
    id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    method = fields.Str(required=True)
    provider_txn_id = fields.Str(required=True)
    amount = fields.Decimal(required=True, places=2)
    currency = fields.Str(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

class PaymentActionSchema(Schema):
    """Schema for payment actions (capture, refund, etc.)"""
    action = fields.Str(required=True, validate=validate.OneOf(['capture', 'refund', 'fail']))
