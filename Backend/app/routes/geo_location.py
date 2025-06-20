from flask import Blueprint, request, jsonify
from app.models.geo_location import GeoLocation
from app import db
from datetime import datetime

geo_location_bp = Blueprint('geo_location', __name__)

@geo_location_bp.route('/geo_locations', methods=['POST'])
def create_geo_location():
    data = request.get_json()
    geo = GeoLocation(
        latitude=data['latitude'],
        longitude=data['longitude'],
        address=data.get('address'),
        city=data.get('city')
    )
    db.session.add(geo)
    db.session.commit()
    return jsonify({'message': 'GeoLocation created', 'id': geo.id}), 201

@geo_location_bp.route('/geo_locations/<int:geo_id>', methods=['GET'])
def get_geo_location(geo_id):
    geo = GeoLocation.query.get(geo_id)
    if not geo:
        return jsonify({'error': 'GeoLocation not found'}), 404
    return jsonify(geo.to_dict()), 200

@geo_location_bp.route('/geo_locations', methods=['GET'])
def list_geo_locations():
    geos = GeoLocation.query.all()
    return jsonify([g.to_dict() for g in geos]), 200

@geo_location_bp.route('/geo_locations/<int:geo_id>', methods=['PUT'])
def update_geo_location(geo_id):
    geo = GeoLocation.query.get(geo_id)
    if not geo:
        return jsonify({'error': 'GeoLocation not found'}), 404

    data = request.get_json()
    for field in ['latitude', 'longitude', 'address', 'city']:
        if field in data:
            setattr(geo, field, data[field])
    geo.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'GeoLocation updated'}), 200