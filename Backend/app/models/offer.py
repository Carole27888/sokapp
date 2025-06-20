from app.extensions import db
from datetime import datetime

class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offered_price = db.Column(db.Float, nullable=False)
    quantity_requested = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.Enum('pending', 'accepted', 'rejected', name='offer_status'),
        default='pending'
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    listing = db.relationship("ProduceListing", backref="offers")
    buyer = db.relationship("User", backref="offers_made")