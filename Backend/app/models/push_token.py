from app.extensions import db
from datetime import datetime

class PushNotificationsToken(db.Model):
    __tablename__ = 'push_notifications_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False, unique=True)
    platform = db.Column(db.String(50), nullable=False)  # e.g., 'iOS', 'Android'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="notifications_tokens")

    def __repr__(self):
        return f"<PushToken(id={self.id}, user_id={self.user_id}, token='{self.token}', platform='{self.platform}', created_at={self.created_at})>"