from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from app.models.match import Match, MatchStatus
from app.models.user_profile import User_Profile
from app.models.produce_listing import ProduceListing
from app import db

match_bp = Blueprint('match', __name__)

@match_bp.route('/matches', methods=['POST'])
@jwt_required()
def create_match():
    data = request.get_json()
    buyer_id = data.get('buyer_id')
    produce_listing_id = data.get('produce_listing_id')
    status = data.get('status', MatchStatus.pending.value)

    if not buyer_id or not produce_listing_id:
        return jsonify({'error': 'buyer_id and produce_listing_id are required'}), 400

    match = Match(
        buyer_id=buyer_id,
        produce_listing_id=produce_listing_id,
        status=status
    )
    db.session.add(match)
    db.session.commit()
    return jsonify({'message': 'Match created', 'match_id': match.id}), 201

@match_bp.route('/matches/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify({
        'id': match.id,
        'buyer_id': match.buyer_id,
        'produce_listing_id': match.produce_listing_id,
        'match_date': match.match_date.isoformat() if match.match_date else None,
        'status': match.status
    }), 200

@match_bp.route('/matches', methods=['GET'])
@jwt_required()
def list_matches():
    matches = Match.query.all()
    result = []
    for match in matches:
        result.append({
            'id': match.id,
            'buyer_id': match.buyer_id,
            'produce_listing_id': match.produce_listing_id,
            'match_date': match.match_date.isoformat() if match.match_date else None,
            'status': match.status
        })
    return jsonify(result), 200
@match_bp.route('/test-token', methods=['GET'])
def get_test_token():
    # This creates a test token with a dummy identity
    token = create_access_token(identity={"user_id": 1})
    return jsonify(access_token=token)