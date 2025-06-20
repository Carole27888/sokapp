from flask import Blueprint, request, jsonify
from app.models.image import Image
from app import db
from datetime import datetime

image_bp = Blueprint('image', __name__)

@image_bp.route('/images', methods=['POST'])
def create_image():
    data = request.get_json()
    image = Image(
        url=data['url'],
        description=data.get('description'),
        file_size=data.get('file_size'),
        file_type=data.get('file_type'),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(image)
    db.session.commit()
    return jsonify({'message': 'Image created', 'id': image.id}), 201

@image_bp.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify({
        'id': image.id,
        'url': image.url,
        'description': image.description,
        'file_size': image.file_size,
        'file_type': image.file_type,
        'created_at': image.created_at.isoformat() if image.created_at else None,
        'updated_at': image.updated_at.isoformat() if image.updated_at else None
    }), 200

@image_bp.route('/images', methods=['GET'])
def list_images():
    images = Image.query.all()
    result = []
    for image in images:
        result.append({
            'id': image.id,
            'url': image.url,
            'description': image.description,
            'file_size': image.file_size,
            'file_type': image.file_type,
            'created_at': image.created_at.isoformat() if image.created_at else None,
            'updated_at': image.updated_at.isoformat() if image.updated_at else None
        })
    return jsonify(result), 200

@image_bp.route('/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'error': 'Image not found'}), 404

    data = request.get_json()
    for field in ['url', 'description', 'file_size', 'file_type']:
        if field in data:
            setattr(image, field, data[field])
    image.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Image updated'}), 200