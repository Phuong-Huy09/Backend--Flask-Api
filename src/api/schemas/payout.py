from marshmallow import Schema, fields, validate
from decimal import Decimal

class PayoutRequestSchema(Schema):
    """Schema for payout creation requests"""
    tutor_id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, places=2, validate=validate.Range(min=Decimal('0.01')))

class PayoutUpdateSchema(Schema):
    """Schema for payout status updates"""
    status = fields.Str(required=True, validate=validate.OneOf(['Pending', 'Processing', 'Paid', 'Failed']))

class PayoutResponseSchema(Schema):
    """Schema for payout responses"""
    id = fields.Int(required=True)
    tutor_id = fields.Int(required=True)
    booking_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, places=2)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

class PayoutActionSchema(Schema):
    """Schema for payout actions (process, complete, fail)"""
    action = fields.Str(required=True, validate=validate.OneOf(['process', 'complete', 'fail']))

class TutorEarningsResponseSchema(Schema):
    """Schema for tutor earnings summary"""
    tutor_id = fields.Int(required=True)
    total_earnings = fields.Decimal(required=True, places=2)
    pending_earnings = fields.Decimal(required=True, places=2)
    completed_payouts_count = fields.Int(required=True)
    pending_payouts_count = fields.Int(required=True)
