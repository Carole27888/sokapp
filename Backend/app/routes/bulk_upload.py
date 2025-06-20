from flask import Blueprint, request, jsonify
from app.models.bulk_upload import BulkUpload
from app import db
from datetime import datetime

bulk_upload_bp = Blueprint('bulk_upload', __name__)

@bulk_upload_bp.route('/bulk_uploads', methods=['POST'])
def create_bulk_upload():
    data = request.get_json()
    bulk_upload = BulkUpload(
        user_id=data['user_id'],
        file_path=data['file_path'],
        status=data.get('status', 'pending'),
        created_at=datetime.utcnow()
    )
    db.session.add(bulk_upload)
    db.session.commit()
    return jsonify({'message': 'Bulk upload created', 'id': bulk_upload.id}), 201

@bulk_upload_bp.route('/bulk_uploads/<int:upload_id>', methods=['GET'])
def get_bulk_upload(upload_id):
    bulk_upload = BulkUpload.query.get(upload_id)
    if not bulk_upload:
        return jsonify({'error': 'Bulk upload not found'}), 404
    return jsonify({
        'id': bulk_upload.id,
        'user_id': bulk_upload.user_id,
        'file_path': bulk_upload.file_path,
        'status': bulk_upload.status,
        'created_at': bulk_upload.created_at.isoformat() if bulk_upload.created_at else None
    }), 200

@bulk_upload_bp.route('/bulk_uploads', methods=['GET'])
def list_bulk_uploads():
    uploads = BulkUpload.query.all()
    result = []
    for upload in uploads:
        result.append({
            'id': upload.id,
            'user_id': upload.user_id,
            'file_path': upload.file_path,
            'status': upload.status,
            'created_at': upload.created_at.isoformat() if upload.created_at else None
        })
    return jsonify(result), 200

@bulk_upload_bp.route('/bulk_uploads/<int:upload_id>', methods=['PUT'])
def update_bulk_upload(upload_id):
    bulk_upload = BulkUpload.query.get(upload_id)
    if not bulk_upload:
        return jsonify({'error': 'Bulk upload not found'}), 404

    data = request.get_json()
    if 'file_path' in data:
        bulk_upload.file_path = data['file_path']
    if 'status' in data:
        bulk_upload.status = data['status']
    bulk_upload.created_at = bulk_upload.created_at

    db.session.commit()
    return jsonify({'message': 'Bulk upload updated'}), 200
