from app.extensions import db
from datetime import datetime

class AdminAudit(db.Model):
    __tablename__ = 'admin_audits'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.Text, nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship("User", foreign_keys=[admin_id], backref="admin_actions")
    target_user = db.relationship("User", foreign_keys=[target_user_id], backref="audit_logs")

    def __repr__(self):
        return f"<AdminAudit(id={self.id}, admin_id={self.admin_id}, action='{self.action}', target_user_id={self.target_user_id}, timestamp={self.timestamp})>"