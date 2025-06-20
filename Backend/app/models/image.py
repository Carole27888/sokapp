from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    file_size = db.Column(db.Float, nullable=True)  # Size in bytes
    file_type = db.Column(db.String(50), nullable=True)  # e.g., 'image/jpeg', 'image/png'
    
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @validates('url')
    def validate_url(self, key, value):
        if not isinstance(value, str) or not value.startswith(('http://', 'https://')):
            raise ValueError("URL must be a valid HTTP or HTTPS URL")
        return value

    def __repr__(self):
        return f"<Image(id={self.id}, url={self.url}, description={self.description})>"