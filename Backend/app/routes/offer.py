from flask import Blueprint, request, jsonify
from app.models.offer import Offer
from app import db
from datetime import datetime

offer_bp = Blueprint('offer', __name__)

@offer_bp.route('/offers', methods=['POST'])
def create_offer():
    data = request.get_json()
    offer = Offer(
        listing_id=data['listing_id'],
        buyer_id=data['buyer_id'],
        offered_price=data['offered_price'],
        quantity_requested=data['quantity_requested'],
        status=data.get('status', 'pending'),
        timestamp=datetime.utcnow()
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify({'message': 'Offer created', 'id': offer.id}), 201

@offer_bp.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'error': 'Offer not found'}), 404
    return jsonify({
        'id': offer.id,
        'listing_id': offer.listing_id,
        'buyer_id': offer.buyer_id,
        'offered_price': offer.offered_price,
        'quantity_requested': offer.quantity_requested,
        'status': offer.status,
        'timestamp': offer.timestamp.isoformat() if offer.timestamp else None
    }), 200

@offer_bp.route('/offers', methods=['GET'])
def list_offers():
    offers = Offer.query.all()
    result = []
    for offer in offers:
        result.append({
            'id': offer.id,
            'listing_id': offer.listing_id,
            'buyer_id': offer.buyer_id,
            'offered_price': offer.offered_price,
            'quantity_requested': offer.quantity_requested,
            'status': offer.status,
            'timestamp': offer.timestamp.isoformat() if offer.timestamp else None
        })
    return jsonify(result), 200

@offer_bp.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'error': 'Offer not found'}), 404

    data = request.get_json()
    for field in ['offered_price', 'quantity_requested', 'status']:
        if field in data:
            setattr(offer, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Offer updated'}), 200