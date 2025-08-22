from flask import Blueprint, request, jsonify
from services.subject_service import SubjectService

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")
subject_service = SubjectService()


@subjects_bp.route("/", methods=["GET"])
def get_all_subjects():
    subjects = subject_service.get_all_subjects()
    return jsonify(subjects), 200


@subjects_bp.route("/<int:subject_id>", methods=["GET"])
def get_subject_by_id(subject_id):
    subject = subject_service.get_subject_by_id(subject_id)
    if subject:
        return jsonify(subject), 200
    return jsonify({"message": "Subject not found"}), 404


@subjects_bp.route("/", methods=["POST"])
def create_subject():
    data = request.json
    subject = subject_service.create_subject(data)
    return jsonify(subject), 201