from flask import Blueprint, request, jsonify
from app.models.cms_content import CMSContent
from app import db
from datetime import datetime

cms_content_bp = Blueprint('cms_content', __name__)

@cms_content_bp.route('/cms_content', methods=['POST'])
def create_cms_content():
    data = request.get_json()
    cms_content = CMSContent(
        title=data['title'],
        content=data['content'],
        author_id=data['author_id']
    )
    db.session.add(cms_content)
    db.session.commit()
    return jsonify({'message': 'CMS content created', 'id': cms_content.id}), 201

@cms_content_bp.route('/cms_content/<int:content_id>', methods=['GET'])
def get_cms_content(content_id):
    cms_content = CMSContent.query.get(content_id)
    if not cms_content:
        return jsonify({'error': 'CMS content not found'}), 404
    return jsonify({
        'id': cms_content.id,
        'title': cms_content.title,
        'content': cms_content.content,
        'author_id': cms_content.author_id,
        'created_at': cms_content.created_at.isoformat() if cms_content.created_at else None,
        'updated_at': cms_content.updated_at.isoformat() if cms_content.updated_at else None
    }), 200

@cms_content_bp.route('/cms_content', methods=['GET'])
def list_cms_content():
    contents = CMSContent.query.all()
    result = []
    for cms_content in contents:
        result.append({
            'id': cms_content.id,
            'title': cms_content.title,
            'content': cms_content.content,
            'author_id': cms_content.author_id,
            'created_at': cms_content.created_at.isoformat() if cms_content.created_at else None,
            'updated_at': cms_content.updated_at.isoformat() if cms_content.updated_at else None
        })
    return jsonify(result), 200

@cms_content_bp.route('/cms_content/<int:content_id>', methods=['PUT'])
def update_cms_content(content_id):
    cms_content = CMSContent.query.get(content_id)
    if not cms_content:
        return jsonify({'error': 'CMS content not found'}), 404

    data = request.get_json()
    if 'title' in data:
        cms_content.title = data['title']
    if 'content' in data:
        cms_content.content = data['content']
    cms_content.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'CMS content updated'}), 200