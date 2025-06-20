from flask import Blueprint, request, jsonify
from app.models.activity_log import ActivityLog
from app import db
from datetime import datetime

activity_log_bp = Blueprint('activity_log', __name__)

@activity_log_bp.route('/activity_logs', methods=['POST'])
def create_activity_log():
    data = request.get_json()
    activity_log = ActivityLog(
        user_id=data['user_id'],
        action=data['action'],
        description=data.get('description'),
        ip_address=data.get('ip_address'),
        user_agent=data.get('user_agent'),
        related_order_id=data.get('related_order_id')
    )
    db.session.add(activity_log)
    db.session.commit()
    return jsonify({'message': 'Activity log created', 'id': activity_log.id}), 201

@activity_log_bp.route('/activity_logs/<int:log_id>', methods=['GET'])
def get_activity_log(log_id):
    log = ActivityLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Activity log not found'}), 404
    return jsonify({
        'id': log.id,
        'user_id': log.user_id,
        'action': log.action,
        'description': log.description,
        'created_at': log.created_at.isoformat() if log.created_at else None,
        'updated_at': log.updated_at.isoformat() if log.updated_at else None,
        'ip_address': log.ip_address,
        'user_agent': log.user_agent,
        'related_order_id': log.related_order_id
    }), 200

@activity_log_bp.route('/activity_logs', methods=['GET'])
def list_activity_logs():
    logs = ActivityLog.query.all()
    result = []
    for log in logs:
        result.append({
            'id': log.id,
            'user_id': log.user_id,
            'action': log.action,
            'description': log.description,
            'created_at': log.created_at.isoformat() if log.created_at else None,
            'updated_at': log.updated_at.isoformat() if log.updated_at else None,
            'ip_address': log.ip_address,
            'user_agent': log.user_agent,
            'related_order_id': log.related_order_id
        })
    return jsonify(result), 200