from flask import Blueprint, request, jsonify
from app.models.pricing_history import PricingHistory
from app import db
from datetime import datetime

pricing_history_bp = Blueprint('pricing_history', __name__)

@pricing_history_bp.route('/pricing_history', methods=['POST'])
def create_pricing_history():
    data = request.get_json()
    pricing = PricingHistory(
        listing_id=data['listing_id'],
        price_per_unit=data['price_per_unit'],
        old_price_per_unit=data.get('old_price_per_unit'),
        new_price_per_unit=data.get('new_price_per_unit'),
        quantity_available=data['quantity_available'],
        timestamp=datetime.utcnow()
    )
    db.session.add(pricing)
    db.session.commit()
    return jsonify({'message': 'Pricing history created', 'id': pricing.id}), 201

@pricing_history_bp.route('/pricing_history/<int:listing_id>', methods=['GET'])
def get_pricing_history(listing_id):
    history = PricingHistory.query.filter_by(listing_id=listing_id).all()
    result = []
    for record in history:
        result.append({
            'id': record.id,
            'listing_id': record.listing_id,
            'price_per_unit': record.price_per_unit,
            'old_price_per_unit': record.old_price_per_unit,
            'new_price_per_unit': record.new_price_per_unit,
            'quantity_available': record.quantity_available,
            'timestamp': record.timestamp.isoformat() if record.timestamp else None
        })
    return jsonify(result), 200