
from flask import Blueprint, request, jsonify
from services import tutor_service

tutors_bp = Blueprint("tutors", __name__)

@tutors_bp.route("/", methods=["GET"])
def get_tutors():
    return jsonify(tutor_service.get_all_tutors())

@tutors_bp.route("/<int:tutor_id>", methods=["GET"])
def get_tutor(tutor_id):
    tutor = tutor_service.get_tutor_by_id(tutor_id)
    return jsonify(tutor) if tutor else ({"error": "Tutor not found"}, 404)

@tutors_bp.route("/", methods=["POST"])
def create_tutor():
    data = request.json
    tutor = tutor_service.create_tutor(data)
    return jsonify(tutor), 201

@tutors_bp.route("/<int:tutor_id>", methods=["PUT"])
def update_tutor(tutor_id):
    data = request.json
    tutor = tutor_service.update_tutor(tutor_id, data)
    return jsonify(tutor) if tutor else ({"error": "Tutor not found"}, 404)

@tutors_bp.route("/<int:tutor_id>", methods=["DELETE"])
def delete_tutor(tutor_id):
    if tutor_service.delete_tutor(tutor_id):
        return {"message": "Tutor deleted"}
    return {"error": "Tutor not found"}, 404
