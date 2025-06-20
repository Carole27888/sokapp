from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class ExportData(db.Model):
    __tablename__ = 'export_data'

    EXPORT_TYPES = [
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('excel', 'Excel')
    ]
    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    export_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = db.relationship("User", back_populates="export_data")

    @validates('export_type', 'status')
    def validate_enum(self, key, value):
        if key == 'export_type' and value not in dict(self.EXPORT_TYPES):
            raise ValueError(f"Invalid export type: {value}")
        if key == 'status' and value not in dict(self.STATUS_OPTIONS):
            raise ValueError(f"Invalid status: {value}")
        return value

    def __repr__(self):
        return f"<ExportData(id={self.id}, user_id={self.user_id}, export_type={self.export_type}, status={self.status})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'export_type': self.export_type,
            'status': self.status,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }