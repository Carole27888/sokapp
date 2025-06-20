from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.Enum('pending', 'confirmed', 'shipped', 'delivered', 'cancelled', name='order_status'),
        default='pending'
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listing = db.relationship("ProduceListing", backref="orders")
    buyer = db.relationship("User", backref="orders")