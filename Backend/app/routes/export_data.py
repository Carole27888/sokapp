from flask import Blueprint, request, jsonify
from app.models.export_data import ExportData
from app import db
from datetime import datetime

export_data_bp = Blueprint('export_data', __name__)

@export_data_bp.route('/export_data', methods=['POST'])
def create_export_data():
    data = request.get_json()
    export_data = ExportData(
        user_id=data['user_id'],
        export_type=data['export_type'],
        status=data.get('status', 'pending'),
        file_path=data['file_path'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(export_data)
    db.session.commit()
    return jsonify({'message': 'ExportData created', 'id': export_data.id}), 201

@export_data_bp.route('/export_data/<int:export_id>', methods=['GET'])
def get_export_data(export_id):
    export_data = ExportData.query.get(export_id)
    if not export_data:
        return jsonify({'error': 'ExportData not found'}), 404
    return jsonify(export_data.to_dict()), 200

@export_data_bp.route('/export_data', methods=['GET'])
def list_export_data():
    exports = ExportData.query.all()
    return jsonify([e.to_dict() for e in exports]), 200

@export_data_bp.route('/export_data/<int:export_id>', methods=['PUT'])
def update_export_data(export_id):
    export_data = ExportData.query.get(export_id)
    if not export_data:
        return jsonify({'error': 'ExportData not found'}), 404

    data = request.get_json()
    for field in ['export_type', 'status', 'file_path']:
        if field in data:
            setattr(export_data, field, data[field])
    export_data.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'ExportData updated'}), 200