from flask import Blueprint, request, jsonify
from app.models.produce_listing import ProduceListing
from app import db
from datetime import datetime

produce_listing_bp = Blueprint('produce_listing', __name__)

@produce_listing_bp.route('/produce_listings', methods=['POST'])
def create_produce_listing():
    data = request.get_json()
    listing = ProduceListing(
        user_id=data['user_id'],
        farmer_id=data['farmer_id'], 
        title=data['title'],
        description=data.get('description'),
        image=data.get('image'),
        price_per_unit=data['price_per_unit'],
        quantity_available=data['quantity_available'],
        unit_of_measurement=data['unit_of_measurement'],
        location=data['location'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(listing)
    db.session.commit()
    return jsonify({'message': 'Produce listing created', 'id': listing.id}), 201

@produce_listing_bp.route('/produce_listings/<int:listing_id>', methods=['GET'])
def get_produce_listing(listing_id):
    listing = ProduceListing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Produce listing not found'}), 404
    return jsonify({
        'id': listing.id,
        'user_id': listing.user_id,
        'title': listing.title,
        'description': listing.description,
        'image': listing.image,
        'price_per_unit': listing.price_per_unit,
        'quantity_available': listing.quantity_available,
        'unit_of_measurement': listing.unit_of_measurement,
        'location': listing.location,
        'created_at': listing.created_at.isoformat() if listing.created_at else None,
        'updated_at': listing.updated_at.isoformat() if listing.updated_at else None
    }), 200

@produce_listing_bp.route('/produce_listings', methods=['GET'])
def list_produce_listings():
    listings = ProduceListing.query.all()
    result = []
    for listing in listings:
        result.append({
            'id': listing.id,
            'user_id': listing.user_id,
            'title': listing.title,
            'description': listing.description,
            'image': listing.image,
            'price_per_unit': listing.price_per_unit,
            'quantity_available': listing.quantity_available,
            'unit_of_measurement': listing.unit_of_measurement,
            'location': listing.location,
            'created_at': listing.created_at.isoformat() if listing.created_at else None,
            'updated_at': listing.updated_at.isoformat() if listing.updated_at else None
        })
    return jsonify(result), 200

@produce_listing_bp.route('/produce_listings/<int:listing_id>', methods=['PUT'])
def update_produce_listing(listing_id):
    listing = ProduceListing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Produce listing not found'}), 404

    data = request.get_json()
    for field in [
        'title', 'description', 'image', 'price_per_unit', 'quantity_available',
        'unit_of_measurement', 'location'
    ]:
        if field in data:
            setattr(listing, field, data[field])
    listing.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Produce listing updated'}), 200