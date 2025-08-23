

from flask import Blueprint, request, jsonify
from services import student_service

students_bp = Blueprint("students", __name__)

@students_bp.route("/", methods=["GET"])
def get_students():
    return jsonify(student_service.get_all_students())

@students_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = student_service.get_student_by_id(student_id)
    return jsonify(student) if student else ({"error": "Student not found"}, 404)

@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.json
    student = student_service.create_student(data)
    return jsonify(student), 201

@students_bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    student = student_service.update_student(student_id, data)
    return jsonify(student) if student else ({"error": "Student not found"}, 404)

@students_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_service.delete_student(student_id):
        return {"message": "Student deleted"}
    return {"error": "Student not found"}, 404
