from flask import Blueprint, request, jsonify
from services.booking_service import BookingService

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")
booking_service = BookingService()


@bookings_bp.route("/", methods=["GET"])
def get_all_bookings():
    bookings = booking_service.get_all_bookings()
    return jsonify(bookings), 200


@bookings_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking_by_id(booking_id):
    booking = booking_service.get_booking_by_id(booking_id)
    if booking:
        return jsonify(booking), 200
    return jsonify({"message": "Booking not found"}), 404


@bookings_bp.route("/", methods=["POST"])
def create_booking():
    data = request.json
    booking = booking_service.create_booking(data)
    return jsonify(booking), 201