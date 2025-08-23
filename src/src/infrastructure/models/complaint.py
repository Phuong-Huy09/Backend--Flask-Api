from datetime import datetime
from src.infrastructure.databases.db import db

class Complaint(db.Model):
    __tablename__ = "complaints"
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="pending")  # pending|in_progress|resolved|rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reporter = db.relationship("User", foreign_keys=[reporter_id], backref="filed_complaints")
    target_user = db.relationship("User", foreign_keys=[target_user_id], backref="received_complaints")
