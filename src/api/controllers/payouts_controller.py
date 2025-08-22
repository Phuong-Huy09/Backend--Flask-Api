from flask import Blueprint, request, jsonify
from services.payout_service import PayoutService
from infrastructure.repositories.payout_repository import PayoutRepository
from api.schemas.payout import (
    PayoutRequestSchema, 
    PayoutResponseSchema, 
    PayoutUpdateSchema,
    PayoutActionSchema,
    TutorEarningsResponseSchema
)
from domain.models.payout import PayoutStatus
from infrastructure.databases.mssql import session
from decimal import Decimal
from datetime import datetime

bp = Blueprint('payouts', __name__, url_prefix='/payouts')

# Initialize service with repository
payout_service = PayoutService(PayoutRepository(session))

# Initialize schemas
request_schema = PayoutRequestSchema()
response_schema = PayoutResponseSchema()
update_schema = PayoutUpdateSchema()
action_schema = PayoutActionSchema()
earnings_schema = TutorEarningsResponseSchema()

@bp.route('/', methods=['POST'])
def create_payout():
    """
    Create a new payout
    ---
    post:
      summary: Create a new payout for a tutor
      tags:
        - Payouts
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PayoutRequestSchema'
      responses:
        201:
          description: Payout created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutResponseSchema'
        400:
          description: Invalid request data
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = request_schema.load(request.json)
        
        # Create payout
        payout = payout_service.create_payout(
            tutor_id=data['tutor_id'],
            booking_id=data['booking_id'],
            amount=Decimal(str(data['amount']))
        )
        
        return jsonify(response_schema.dump(payout)), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:payout_id>', methods=['GET'])
def get_payout(payout_id):
    """
    Get payout by ID
    ---
    get:
      summary: Get payout by ID
      parameters:
        - name: payout_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payout cần lấy
      tags:
        - Payouts
      responses:
        200:
          description: Payout found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutResponseSchema'
        404:
          description: Payout not found
        500:
          description: Internal server error
    """
    try:
        payout = payout_service.get_payout(payout_id)
        
        if not payout:
            return jsonify({'error': 'Payout not found'}), 404
            
        return jsonify(response_schema.dump(payout)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tutor/<int:tutor_id>', methods=['GET'])
def get_tutor_payouts(tutor_id):
    """
    Get all payouts for a tutor
    ---
    get:
      summary: Get all payouts for a specific tutor
      parameters:
        - name: tutor_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của tutor
      tags:
        - Payouts
      responses:
        200:
          description: List of payouts for the tutor
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PayoutResponseSchema'
        500:
          description: Internal server error
    """
    try:
        payouts = payout_service.get_tutor_payouts(tutor_id)
        return jsonify(response_schema.dump(payouts, many=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/booking/<int:booking_id>', methods=['GET'])
def get_booking_payouts(booking_id):
    """
    Get all payouts for a booking
    ---
    get:
      summary: Get all payouts for a specific booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của booking
      tags:
        - Payouts
      responses:
        200:
          description: List of payouts for the booking
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PayoutResponseSchema'
        500:
          description: Internal server error
    """
    try:
        payouts = payout_service.get_booking_payouts(booking_id)
        return jsonify(response_schema.dump(payouts, many=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payout_id>/actions', methods=['POST'])
def payout_action(payout_id):
    """
    Perform action on payout (process, complete, fail)
    ---
    post:
      summary: Perform action on payout
      parameters:
        - name: payout_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payout
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PayoutActionSchema'
      tags:
        - Payouts
      responses:
        200:
          description: Action performed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutResponseSchema'
        400:
          description: Invalid action or payout state
        404:
          description: Payout not found
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = action_schema.load(request.json)
        action = data['actionSchema']
        
        payout = None
        
        if action == 'process':
            payout = payout_service.process_payout(payout_id)
        elif action == 'complete':
            payout = payout_service.complete_payout(payout_id)
        elif action == 'fail':
            payout = payout_service.fail_payout(payout_id)
            
        if not payout:
            return jsonify({'error': 'Payout not found'}), 404
            
        return jsonify(response_schema.dump(payout)), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payout_id>/status', methods=['PUT'])
def update_payout_status(payout_id):
    """
    Update payout status
    ---
    put:
      summary: Update payout status
      parameters:
        - name: payout_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payout
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PayoutUpdateSchema'
      tags:
        - Payouts
      responses:
        200:
          description: Payout status updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PayoutResponseSchema'
        400:
          description: Invalid status
        404:
          description: Payout not found
        500:
          description: Internal server error
    """
    try:
        # Validate request data
        data = update_schema.load(request.json)
        
        # Convert status string to enum
        status = PayoutStatus(data['status'])
        
        payout = payout_service.update_payout_status(payout_id, status)
        
        if not payout:
            return jsonify({'error': 'Payout not found'}), 404
            
        return jsonify(response_schema.dump(payout)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/status/<status>', methods=['GET'])
def list_payouts_by_status(status):
    """
    Get payouts by status
    ---
    get:
      summary: Get payouts by status
      parameters:
        - name: status
          in: path
          required: true
          schema:
            type: string
            enum: [Pending, Processing, Paid, Failed]
          description: Payout status
      tags:
        - Payouts
      responses:
        200:
          description: List of payouts
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PayoutResponseSchema'
        400:
          description: Invalid status
        500:
          description: Internal server error
    """
    try:
        # Convert status string to enum
        payout_status = PayoutStatus(status)
        
        payouts = payout_service.get_payouts_by_status(payout_status)
        
        return jsonify(response_schema.dump(payouts, many=True)), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid payout status'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pending', methods=['GET'])
def get_pending_payouts():
    """
    Get all pending payouts
    ---
    get:
      summary: Get all pending payouts for processing
      tags:
        - Payouts
      responses:
        200:
          description: List of pending payouts
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PayoutResponseSchema'
        500:
          description: Internal server error
    """
    try:
        payouts = payout_service.get_pending_payouts()
        return jsonify(response_schema.dump(payouts, many=True)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tutor/<int:tutor_id>/earnings', methods=['GET'])
def get_tutor_earnings(tutor_id):
    """
    Get tutor earnings summary
    ---
    get:
      summary: Get earnings summary for a tutor
      parameters:
        - name: tutor_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của tutor
      tags:
        - Payouts
      responses:
        200:
          description: Tutor earnings summary
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TutorEarningsResponseSchema'
        500:
          description: Internal server error
    """
    try:
        # Calculate earnings
        total_earnings = payout_service.calculate_tutor_earnings(tutor_id)
        pending_earnings = payout_service.calculate_pending_earnings(tutor_id)
        
        # Get payouts for counting
        all_payouts = payout_service.get_tutor_payouts(tutor_id)
        completed_count = len([p for p in all_payouts if p.status == PayoutStatus.PAID])
        pending_count = len([p for p in all_payouts if p.status in [PayoutStatus.PENDING, PayoutStatus.PROCESSING]])
        
        earnings_data = {
            'tutor_id': tutor_id,
            'total_earnings': total_earnings,
            'pending_earnings': pending_earnings,
            'completed_payouts_count': completed_count,
            'pending_payouts_count': pending_count
        }
        
        return jsonify(earnings_schema.dump(earnings_data)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:payout_id>/check', methods=['GET'])
def check_payout_completed(payout_id):
    """
    Check if payout is completed
    ---
    get:
      summary: Check if payout is completed
      parameters:
        - name: payout_id
          in: path
          required: true
          schema:
            type: integer
          description: ID của payout
      tags:
        - Payouts
      responses:
        200:
          description: Payout completion status
          content:
            application/json:
              schema:
                type: object
                properties:
                  payout_id:
                    type: integer
                  is_completed:
                    type: boolean
        404:
          description: Payout not found
        500:
          description: Internal server error
    """
    try:
        is_completed = payout_service.is_payout_completed(payout_id)
        
        # Check if payout exists
        payout = payout_service.get_payout(payout_id)
        if not payout:
            return jsonify({'error': 'Payout not found'}), 404
            
        return jsonify({
            'payout_id': payout_id,
            'is_completed': is_completed
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
