from flask import Blueprint, request, jsonify
from app.models.message import Message
from app import db
import datetime

message_bp = Blueprint('message', __name__)

@message_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        content=data['content'],
        timestamp=int(datetime.datetime.utcnow().timestamp())
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': 'Message sent', 'id': message.id}), 201

@message_bp.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify({
        'id': message.id,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'timestamp': message.timestamp
    }), 200

@message_bp.route('/messages', methods=['GET'])
def list_messages():
    messages = Message.query.all()
    result = []
    for message in messages:
        result.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'content': message.content,
            'timestamp': message.timestamp
        })
    return jsonify(result), 200