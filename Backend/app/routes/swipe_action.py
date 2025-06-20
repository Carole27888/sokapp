from flask import Blueprint, request, jsonify
from app.models.swipe_action import SwipeAction, SwipeActionType
from app import db

swipe_action_bp = Blueprint('swipe_action', __name__)

@swipe_action_bp.route('/swipe_actions', methods=['POST'])
def create_swipe_action():
    data = request.get_json()
    user_id = data.get('user_id')
    action_type = data.get('action_type')
    produce_listing_id = data.get('produce_listing_id')  

    if not user_id or not action_type:
        return jsonify({'error': 'user_id and action_type are required'}), 400

    if action_type not in [e.value for e in SwipeActionType]:
        return jsonify({'error': f"Invalid action_type. Must be one of {[e.value for e in SwipeActionType]}"}), 400

    swipe_action = SwipeAction(
        user_id=user_id,
        action_type=action_type,
        produce_listing_id=produce_listing_id  
    )
    db.session.add(swipe_action)
    db.session.commit()
    return jsonify({'message': 'Swipe action created', 'id': swipe_action.id}), 201

@swipe_action_bp.route('/swipe_actions/<int:action_id>', methods=['GET'])
def get_swipe_action(action_id):
    action = SwipeAction.query.get(action_id)
    if not action:
        return jsonify({'error': 'Swipe action not found'}), 404
    return jsonify({
        'id': action.id,
        'user_id': action.user_id,
        'action_type': action.action_type,
        'timestamp': action.timestamp
    }), 200

@swipe_action_bp.route('/swipe_actions', methods=['GET'])
def list_swipe_actions():
    actions = SwipeAction.query.all()
    result = []
    for action in actions:
        result.append({
            'id': action.id,
            'user_id': action.user_id,
            'action_type': action.action_type,
            'timestamp': action.timestamp
        })
    return jsonify(result), 200