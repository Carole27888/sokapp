from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class Notification(db.Model):
    __tablename__ = 'notifications'

    NOTIFICATION_TYPES = [
        ('match', 'Match'),
        ('message', 'Message'),
        ('report', 'Report'),
        ('alert', 'Alert'),
        ('reminder', 'Reminder'),
        ('other', 'Other')
    ]
    DELIVERY_METHODS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    delivery_method = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Integer, default=0, nullable=False)  # 0 for unread, 1 for read
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @validates('notification_type', 'delivery_method')
    def validate_enum(self, key, value):
        if key == 'notification_type' and value not in dict(self.NOTIFICATION_TYPES):
            raise ValueError(f"Invalid notification type: {value}")
        if key == 'delivery_method' and value not in dict(self.DELIVERY_METHODS):
            raise ValueError(f"Invalid delivery method: {value}")
        return value

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type}, method={self.delivery_method}, content={self.content[:20]}...)>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type,
            'delivery_method': self.delivery_method,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }