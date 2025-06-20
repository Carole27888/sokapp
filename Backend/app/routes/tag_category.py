from flask import Blueprint, request, jsonify
from app.models.tag_category import TagCategory
from app import db
from datetime import datetime

tag_category_bp = Blueprint('tag_category', __name__)

@tag_category_bp.route('/tag_categories', methods=['POST'])
def create_tag_category():
    data = request.get_json()
    tag_category = TagCategory(
        name=data['name'],
        description=data.get('description'),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(tag_category)
    db.session.commit()
    return jsonify({'message': 'Tag category created', 'id': tag_category.id}), 201

@tag_category_bp.route('/tag_categories/<int:category_id>', methods=['GET'])
def get_tag_category(category_id):
    category = TagCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Tag category not found'}), 404
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'created_at': category.created_at.isoformat() if category.created_at else None,
        'updated_at': category.updated_at.isoformat() if category.updated_at else None
    }), 200

@tag_category_bp.route('/tag_categories', methods=['GET'])
def list_tag_categories():
    categories = TagCategory.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'created_at': category.created_at.isoformat() if category.created_at else None,
            'updated_at': category.updated_at.isoformat() if category.updated_at else None
        })
    return jsonify(result), 200



@tag_category_bp.route('/tag_categories/<int:category_id>', methods=['DELETE'])
def delete_tag_category(category_id):
    category = TagCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Tag category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Tag category deleted'}), 200



@tag_category_bp.route('/tag_categories/<int:category_id>', methods=['PUT'])
def update_tag_category(category_id):
    category = TagCategory.query.get(category_id)
    if not category:
        return jsonify({'error': 'Tag category not found'}), 404

    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    category.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Tag category updated'}), 200

