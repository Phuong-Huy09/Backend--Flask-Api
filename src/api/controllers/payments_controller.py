from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService
from infrastructure.repositories.payment_repository import PaymentRepository
from api.schemas.payment import (
    PaymentRequestSchema, 
    PaymentResponseSchema, 
    PaymentUpdateSchema,
    PaymentActionSchema
)
from domain.models.payment import PaymentMethod, PaymentStatus
from infrastructure.databases.mssql import session
from decimal import Decimal
from datetime import datetime

bp = Blueprint('payments', __name__, url_prefix='/payments')

# Initialize service with repository
payment_service = PaymentService(PaymentRepository(session))

# Initialize schemas
request_schema = PaymentRequestSchema()
response_schema = PaymentResponseSchema()
update_schema = PaymentUpdateSchema()
action_schema = PaymentActionSchema()

@bp.route('/', methods=['POST'])
def create_payment():
    """
    Create a new payment
    ---
    post:
      summary: Create a new payment
      tags:
        - Payments
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentRequestSchema'
      responses:
        201:
          description: Payment created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponseSchema'
        400:
          description: Invalid request data
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = request_schema.load(request.json)
        
        # Convert method string to enum
        method = PaymentMethod(data['method'])
        
        # Create payment
        payment = payment_service.create_payment(
            booking_id=data['booking_id'],
            amount=Decimal(str(data['amount'])),
            method=method,
            provider_txn_id=data.get('provider_txn_id', ''),
            currency=data.get('currency', 'USD')
        )
        
        return jsonify(response_schema.dump(payment)), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """
    Get payment by ID
    ---
    get:
      summary: Get payment by ID
      parameters:
        - name: payment_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payment cần lấy
      tags:
        - Payments
      responses:
        200:
          description: Payment found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponseSchema'
        404:
          description: Payment not found
        500:
          description: Internal server error
    """
    try:
        payment = payment_service.get_payment(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
            
        return jsonify(response_schema.dump(payment)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/booking/<int:booking_id>', methods=['GET'])
def get_payment_by_booking(booking_id):
    """
    Get payment by booking ID
    ---
    get:
      summary: Get payment by booking ID
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của booking
      tags:
        - Payments
      responses:
        200:
          description: Payment found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponseSchema'
        404:
          description: Payment not found
        500:
          description: Internal server error
    """
    try:
        payment = payment_service.get_payment_by_booking(booking_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found for this booking'}), 404
            
        return jsonify(response_schema.dump(payment)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payment_id>/actions', methods=['POST'])
def payment_action(payment_id):
    """
    Perform action on payment (capture, refund, fail)
    ---
    post:
      summary: Perform action on payment
      parameters:
        - name: payment_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentActionSchema'
      tags:
        - Payments
      responses:
        200:
          description: Action performed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponseSchema'
        400:
          description: Invalid action or payment state
        404:
          description: Payment not found
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = action_schema.load(request.json)
        action = data['action']
        
        payment = None
        
        if action == 'capture':
            payment = payment_service.capture_payment(payment_id)
        elif action == 'refund':
            payment = payment_service.refund_payment(payment_id)
        elif action == 'fail':
            payment = payment_service.fail_payment(payment_id)
            
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
            
        return jsonify(response_schema.dump(payment)), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payment_id>/status', methods=['PUT'])
def update_payment_status(payment_id):
    """
    Update payment status
    ---
    put:
      summary: Update payment status
      parameters:
        - name: payment_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PaymentUpdateSchema'
      tags:
        - Payments
      responses:
        200:
          description: Payment status updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaymentResponseSchema'
        400:
          description: Invalid status
        404:
          description: Payment not found
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = update_schema.load(request.json)
        
        # Convert status string to enum
        status = PaymentStatus(data['status'])
        
        payment = payment_service.update_payment_status(payment_id, status)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
            
        return jsonify(response_schema.dump(payment)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/status/<status>', methods=['GET'])
def list_payments_by_status(status):
    """
    Get payments by status
    ---
    get:
      summary: Get payments by status
      parameters:
        - name: status
          in: path
          required: true
          schema:
            type: string
            enum: [Authorized, Captured, Failed, Refunded]
          description: Payment status
      tags:
        - Payments
      responses:
        200:
          description: List of payments
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PaymentResponseSchema'
        400:
          description: Invalid status
        500:
          description: Internal server error
    """
    try:
        # Convert status string to enum
        payment_status = PaymentStatus(status)
        
        payments = payment_service.list_payments_by_status(payment_status)
        
        return jsonify(response_schema.dump(payments, many=True)), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid payment status'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payment_id>/check', methods=['GET'])
def check_payment_success(payment_id):
    """
    Check if payment is successful
    ---
    get:
      summary: Check if payment is successful
      parameters:
        - name: payment_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payment
      tags:
        - Payments
      responses:
        200:
          description: Payment status check result
          content:
            application/json:
              schema:
                type: object
                properties:
                  payment_id:
                    type: integer
                  is_successful:
                    type: boolean
        404:
          description: Payment not found
        500:
          description: Internal server error
    """
    try:
        is_successful = payment_service.is_payment_successful(payment_id)
        
        # Check if payment exists
        payment = payment_service.get_payment(payment_id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
            
        return jsonify({
            'payment_id': payment_id,
            'is_successful': is_successful
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
