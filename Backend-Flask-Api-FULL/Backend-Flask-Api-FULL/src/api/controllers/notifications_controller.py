from flask import Blueprint, request, jsonify
from src.services.notification_service import NotificationService
from src.api.schemas.notification import NotificationCreateSchema, NotificationResponseSchema

bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")
service = NotificationService()
create_schema = NotificationCreateSchema()
resp_schema = NotificationResponseSchema()
resp_many = NotificationResponseSchema(many=True)

@bp.get("")
def list_notifications():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    is_read = request.args.get("is_read", default=None)
    if is_read is not None:
        is_read = is_read.lower() in ["1","true","yes"]
    data = service.list_notifications(user_id=user_id, is_read=is_read)
    return jsonify(resp_many.dump(data))

@bp.post("")
def create_notification():
    payload = request.get_json() or {}
    errors = create_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    n = service.create_notification(**payload)
    return jsonify(resp_schema.dump(n)), 201

@bp.post("/<int:notif_id>/read")
def mark_read(notif_id: int):
    n = service.mark_as_read(notif_id)
    if not n:
        return jsonify({"error": "Not found"}), 404
    return jsonify(resp_schema.dump(n))

@bp.delete("/<int:notif_id>")
def delete_notification(notif_id: int):
    ok = service.delete(notif_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404
    return "", 204
