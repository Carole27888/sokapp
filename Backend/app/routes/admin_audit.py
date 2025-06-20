from flask import Blueprint, request, jsonify
from app.models.admin_audit import AdminAudit
from app import db
from datetime import datetime

admin_audit_bp = Blueprint('admin_audit', __name__)

@admin_audit_bp.route('/admin_audits', methods=['POST'])
def create_admin_audit():
    data = request.get_json()
    audit = AdminAudit(
        admin_id=data['admin_id'],
        action=data['action'],
        target_user_id=data.get('target_user_id'),
        timestamp=datetime.utcnow()
    )
    db.session.add(audit)
    db.session.commit()
    return jsonify({'message': 'Admin audit log created', 'id': audit.id}), 201

@admin_audit_bp.route('/admin_audits/<int:audit_id>', methods=['GET'])
def get_admin_audit(audit_id):
    audit = AdminAudit.query.get(audit_id)
    if not audit:
        return jsonify({'error': 'Admin audit log not found'}), 404
    return jsonify({
        'id': audit.id,
        'admin_id': audit.admin_id,
        'action': audit.action,
        'target_user_id': audit.target_user_id,
        'timestamp': audit.timestamp.isoformat() if audit.timestamp else None
    }), 200

@admin_audit_bp.route('/admin_audits', methods=['GET'])
def list_admin_audits():
    audits = AdminAudit.query.all()
    result = []
    for audit in audits:
        result.append({
            'id': audit.id,
            'admin_id': audit.admin_id,
            'action': audit.action,
            'target_user_id': audit.target_user_id,
            'timestamp': audit.timestamp.isoformat() if audit.timestamp else None
        })
    return jsonify(result), 200