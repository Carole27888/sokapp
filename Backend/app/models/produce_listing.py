from app.extensions import db
import datetime

class ProduceListing(db.Model):
    __tablename__ = 'produce_listings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    price_per_unit = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    unit_of_measurement = db.Column(db.String(50), nullable=False)  # e.g., kg, lbs, etc.
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    swipe_actions = db.relationship("SwipeAction", back_populates="produce_listing")  

    farmer = db.relationship("User_Profile", back_populates="produce_listings")
    matches = db.relationship("Match", back_populates="produce_listing")
    pricing_history = db.relationship("PricingHistory", back_populates="listing")

    def __repr__(self):
        return f"<ProduceListing(id={self.id}, title={self.title}, price_per_unit={self.price_per_unit})>"