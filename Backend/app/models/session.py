from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(50), nullable=False, unique=True)
    token = db.Column(db.String(255), nullable=False)
    device_info = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=func.now())
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Float, nullable=True)

    @validates('session_id')
    def validate_session_id(self, key, value):
        if not value:
            raise ValueError("Session ID cannot be empty")
        return value