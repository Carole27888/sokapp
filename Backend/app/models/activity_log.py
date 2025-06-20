from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('match', 'Match'),
        ('other', 'Other')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # Supports IPv6
    user_agent = db.Column(db.String(255), nullable=True)
    related_order_id = db.Column(db.Integer, nullable=True)

    @validates('action')
    def validate_action(self, key, value):
        if value not in dict(self.ACTION_CHOICES):
            raise ValueError(f"Action must be one of {', '.join(dict(self.ACTION_CHOICES).keys())}")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        if value <= 0:
            raise ValueError("User ID must be a positive integer")
        return value

    @validates('id')
    def validate_id(self, key, value):
        if value <= 0:
            raise ValueError("ID must be a positive integer")
        return value

    def __repr__(self):
        return f"ActivityLog(id={self.id}, user_id={self.user_id}, action={self.action}, description={self.description}, created_at={self.created_at})"

    def __str__(self):
        return f"ActivityLog: {self.action} by User {self.user_id} at {self.created_at}, Description: {self.description or 'N/A'}"

    def __init__(self, user_id, action, description=None, ip_address=None, user_agent=None, related_order_id=None):
        self.user_id = user_id
        self.action = action
        self.description = description
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.related_order_id = related_order_id