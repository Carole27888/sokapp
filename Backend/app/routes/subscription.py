from flask import Blueprint, request, jsonify
from app.models.subscription import Subscription
from app import db
from datetime import datetime

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.get_json()
    subscription = Subscription(
        user_id=data['user_id'],
        plan_name=data['plan_name'],
        start_date=datetime.fromisoformat(data.get('start_date')) if data.get('start_date') else datetime.utcnow(),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'active')
    )
    db.session.add(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription created', 'id': subscription.id}), 201

@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404
    return jsonify({
        'id': subscription.id,
        'user_id': subscription.user_id,
        'plan_name': subscription.plan_name,
        'start_date': subscription.start_date.isoformat() if subscription.start_date else None,
        'end_date': subscription.end_date.isoformat() if subscription.end_date else None,
        'status': subscription.status
    }), 200

@subscription_bp.route('/subscriptions', methods=['GET'])
def list_subscriptions():
    subscriptions = Subscription.query.all()
    result = []
    for sub in subscriptions:
        result.append({
            'id': sub.id,
            'user_id': sub.user_id,
            'plan_name': sub.plan_name,
            'start_date': sub.start_date.isoformat() if sub.start_date else None,
            'end_date': sub.end_date.isoformat() if sub.end_date else None,
            'status': sub.status
        })
    return jsonify(result), 200

@subscription_bp.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404

    data = request.get_json()
    if 'plan_name' in data:
        subscription.plan_name = data['plan_name']
    if 'start_date' in data:
        subscription.start_date = datetime.fromisoformat(data['start_date'])
    if 'end_date' in data:
        subscription.end_date = datetime.fromisoformat(data['end_date'])
    if 'status' in data:
        subscription.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Subscription updated'}), 200