from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class GeoLocation(db.Model):
    __tablename__ = 'geo_locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)

    @validates('latitude', 'longitude')
    def validate_coordinates(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be a number")
        if key == 'latitude':
            if not (-90 <= value <= 90):
                raise ValueError("Latitude must be between -90 and 90 degrees")
        elif key == 'longitude':
            if not (-180 <= value <= 180):
                raise ValueError("Longitude must be between -180 and 180 degrees")
        return value

    @validates('address', 'city')
    def validate_string_fields(self, key, value):
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if key == 'address' and len(value) > 255:
            raise ValueError("Address cannot exceed 255 characters")
        if key == 'city' and len(value) > 100:
            raise ValueError("City cannot exceed 100 characters")
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

    def __repr__(self):
        return f"<GeoLocation(id={self.id}, latitude={self.latitude}, longitude={self.longitude}, address={self.address}, city={self.city})>"

    def __str__(self):
        return f"GeoLocation: {self.latitude}, {self.longitude} - Address: {self.address or 'N/A'}, City: {self.city or 'N/A'}"

    def __init__(self, latitude, longitude, address=None, city=None):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.city = city

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'city': self.city,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }