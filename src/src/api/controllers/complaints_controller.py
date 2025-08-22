from flask import Blueprint, request, jsonify
from src.services.complaint_service import ComplaintService
from src.api.schemas.complaint import (
    ComplaintCreateSchema,
    ComplaintUpdateStatusSchema,
    ComplaintResponseSchema,
)

bp = Blueprint("complaints", __name__, url_prefix="/api/complaints")
service = ComplaintService()
create_schema = ComplaintCreateSchema()
update_schema = ComplaintUpdateStatusSchema()
resp_schema = ComplaintResponseSchema()
resp_many = ComplaintResponseSchema(many=True)

@bp.get("")
def list_complaints():
    status = request.args.get("status")
    data = service.list_complaints(status=status)
    return jsonify(resp_many.dump(data))

@bp.post("")
def create_complaint():
    payload = request.get_json() or {}
    errors = create_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    c = service.create_complaint(**payload)
    return jsonify(resp_schema.dump(c)), 201

@bp.patch("/<int:complaint_id>/status")
def update_status(complaint_id: int):
    payload = request.get_json() or {}
    errors = update_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    c = service.update_status(complaint_id, payload["status"])
    if not c:
        return jsonify({"error": "Not found"}), 404
    return jsonify(resp_schema.dump(c))

@bp.delete("/<int:complaint_id>")
def delete_complaint(complaint_id: int):
    ok = service.delete(complaint_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return "", 204
