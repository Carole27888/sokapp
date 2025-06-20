from flask import Blueprint, request, jsonify
from app.models.feedback import Feedback
from app import db
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback = Feedback(
        user_id=data['user_id'],
        content=data['content'],
        rating=data['rating'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback created', 'id': feedback.id}), 201

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    return jsonify(feedback.to_dict()), 200

@feedback_bp.route('/feedback', methods=['GET'])
def list_feedback():
    feedbacks = Feedback.query.all()
    return jsonify([f.to_dict() for f in feedbacks]), 200

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404

    data = request.get_json()
    if 'content' in data:
        feedback.content = data['content']
    if 'rating' in data:
        feedback.rating = data['rating']
    feedback.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Feedback updated'}), 200