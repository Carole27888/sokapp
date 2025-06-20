from app.extensions import db
from datetime import datetime

class BulkUpload(db.Model):
    __tablename__ = 'bulk_uploads'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Path to the uploaded file
    status = db.Column(db.String(50), default='pending')  # e.g., 'pending', 'processing', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="bulk_uploads")

    def __repr__(self):
        return f"<BulkUpload(id={self.id}, user_id={self.user_id}, file_path='{self.file_path}', status='{self.status}', created_at={self.created_at})>"