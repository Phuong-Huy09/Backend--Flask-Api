from flask import Blueprint, jsonify
from src.infrastructure.databases.db import db
from src.infrastructure.models.user import User

bp = Blueprint("seed", __name__, url_prefix="/api/seed")

@bp.post("/users")
def seed_users():
    if User.query.first():
        return jsonify({"message": "Already seeded"}), 200
    users = [
        User(role="student", name="Alice", email="alice@example.com"),
        User(role="tutor", name="Bob", email="bob@example.com"),
        User(role="moderator", name="Mod", email="mod@example.com"),
        User(role="admin", name="Admin", email="admin@example.com"),
    ]
    db.session.add_all(users)
    db.session.commit()
    return jsonify({"message": "Seeded", "count": len(users)}), 201
