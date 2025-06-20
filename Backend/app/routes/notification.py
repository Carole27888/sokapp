from flask import Blueprint, request, jsonify
from app.models.notification import Notification
from app import db
from datetime import datetime

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    try:
        notification = Notification(
            user_id=data['user_id'],
            notification_type=data['notification_type'],
            delivery_method=data['delivery_method'],
            content=data['content'],
            is_read=data.get('is_read', 0),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
        return jsonify({'message': 'Notification created', 'id': notification.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@notification_bp.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    return jsonify(notification.to_dict()), 200

@notification_bp.route('/notifications', methods=['GET'])
def list_notifications():
    notifications = Notification.query.all()
    return jsonify([n.to_dict() for n in notifications]), 200

@notification_bp.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    data = request.get_json()
    if 'is_read' in data:
        notification.is_read = data['is_read']
    if 'content' in data:
        notification.content = data['content']
    if 'notification_type' in data:
        notification.notification_type = data['notification_type']
    if 'delivery_method' in data:
        notification.delivery_method = data['delivery_method']
    notification.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Notification updated'}), 200