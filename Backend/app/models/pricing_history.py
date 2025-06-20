from app.extensions import db
from datetime import datetime

class PricingHistory(db.Model):
    __tablename__ = 'pricing_history'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)
    price_per_unit = db.Column(db.String(50), nullable=False)  # e.g., '2.50 USD/kg'
    old_price_per_unit = db.Column(db.String(50), nullable=True)
    new_price_per_unit = db.Column(db.String(50), nullable=True)
    quantity_available = db.Column(db.String(50), nullable=False)  # e.g., '100 kg'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    listing = db.relationship("ProduceListing", back_populates="pricing_history")

    def __repr__(self):
        return f"<PricingHistory(id={self.id}, listing_id={self.listing_id}, price_per_unit='{self.price_per_unit}', quantity_available='{self.quantity_available}', timestamp={self.timestamp})>"