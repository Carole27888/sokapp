from flask import Blueprint, request, jsonify
from app.models.push_token import PushNotificationsToken
from app import db
from datetime import datetime

push_token_bp = Blueprint('push_token', __name__)

@push_token_bp.route('/push_tokens', methods=['POST'])
def create_push_token():
    data = request.get_json()
    push_token = PushNotificationsToken(
        user_id=data['user_id'],
        token=data['token'],
        platform=data['platform'],
        created_at=datetime.utcnow()
    )
    db.session.add(push_token)
    db.session.commit()
    return jsonify({'message': 'Push notification token created', 'id': push_token.id}), 201

@push_token_bp.route('/push_tokens/<int:token_id>', methods=['GET'])
def get_push_token(token_id):
    token = PushNotificationsToken.query.get(token_id)
    if not token:
        return jsonify({'error': 'Push notification token not found'}), 404
    return jsonify({
        'id': token.id,
        'user_id': token.user_id,
        'token': token.token,
        'platform': token.platform,
        'created_at': token.created_at.isoformat() if token.created_at else None
    }), 200

@push_token_bp.route('/push_tokens', methods=['GET'])
def list_push_tokens():
    tokens = PushNotificationsToken.query.all()
    result = []
    for token in tokens:
        result.append({
            'id': token.id,
            'user_id': token.user_id,
            'token': token.token,
            'platform': token.platform,
            'created_at': token.created_at.isoformat() if token.created_at else None
        })
    return jsonify(result), 200