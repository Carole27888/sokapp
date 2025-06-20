from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, rating={self.rating})>"

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    @validates('content')
    def validate_content(self, key, value):
        if len(value) > 500:
            raise ValueError("Content cannot exceed 500 characters")
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

    @validates('created_at', 'updated_at')
    def validate_datetime_fields(self, key, value):
        import datetime
        if not isinstance(value, datetime.datetime):
            raise ValueError(f"{key} must be a valid datetime object")
        return value

    def __init__(self, user_id, content, rating, created_at=None, updated_at=None):
        self.user_id = user_id
        self.content = content
        self.rating = rating
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }