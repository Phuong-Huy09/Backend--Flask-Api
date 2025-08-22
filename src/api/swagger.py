from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
from api.schemas.payout import (
    PayoutRequestSchema, PayoutResponseSchema, PayoutUpdateSchema,
    PayoutActionSchema, TutorEarningsResponseSchema
)
from api.schemas.payment import (
    PaymentRequestSchema, PaymentUpdateSchema,
    PaymentResponseSchema, PaymentActionSchema,
)
spec = APISpec(
    title="Todo API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("TodoRequest", schema=TodoRequestSchema)
spec.components.schema("TodoResponse", schema=TodoResponseSchema)
spec.components.schema("PayoutRequestSchema", schema=PayoutRequestSchema)
spec.components.schema("PayoutResponseSchema", schema=PayoutResponseSchema)
spec.components.schema("PayoutUpdateSchema", schema=PayoutUpdateSchema)
spec.components.schema("PayoutActionSchema", schema=PayoutActionSchema)
spec.components.schema("TutorEarningsResponseSchema", schema=TutorEarningsResponseSchema)

spec.components.schema("PaymentRequestSchema", schema=PaymentRequestSchema)
spec.components.schema("PaymentUpdateSchema",  schema=PaymentUpdateSchema)
spec.components.schema("PaymentResponseSchema", schema=PaymentResponseSchema)
spec.components.schema("PaymentActionSchema",  schema=PaymentActionSchema)