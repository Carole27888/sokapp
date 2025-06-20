from app import db
from sqlalchemy import ForeignKey
import datetime

class User_Profile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    social_links = db.Column(db.String(255), nullable=True)
    received_notifications = db.Column(db.Boolean, default=True)
    favorite_products = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", back_populates="user_profiles")
    produce_listings = db.relationship("ProduceListing", back_populates="farmer")
    matches = db.relationship("Match", back_populates="buyer")

    def __repr__(self):
        return f"<User_Profile(id={self.id}, user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name})>"