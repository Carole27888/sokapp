from flask import Blueprint, request, jsonify
from app.models.session import Session
from app import db
from datetime import datetime

session_bp = Blueprint('session', __name__)

@session_bp.route('/sessions', methods=['POST'])
def create_session():
    data = request.get_json()
    session = Session(
        session_id=data['session_id'],
        token=data['token'],
        device_info=data.get('device_info'),
        user_id=data['user_id'],
        start_time=datetime.fromisoformat(data.get('start_time')) if data.get('start_time') else datetime.utcnow(),
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        duration=data.get('duration')
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'message': 'Session created', 'id': session.id}), 201

@session_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify({
        'id': session.id,
        'session_id': session.session_id,
        'token': session.token,
        'device_info': session.device_info,
        'user_id': session.user_id,
        'start_time': session.start_time.isoformat() if session.start_time else None,
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'duration': session.duration
    }), 200

@session_bp.route('/sessions', methods=['GET'])
def list_sessions():
    sessions = Session.query.all()
    result = []
    for session in sessions:
        result.append({
            'id': session.id,
            'session_id': session.session_id,
            'token': session.token,
            'device_info': session.device_info,
            'user_id': session.user_id,
            'start_time': session.start_time.isoformat() if session.start_time else None,
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'duration': session.duration
        })
    return jsonify(result), 200

@session_bp.route('/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    data = request.get_json()
    if 'token' in data:
        session.token = data['token']
    if 'device_info' in data:
        session.device_info = data['device_info']
    if 'user_id' in data:
        session.user_id = data['user_id']
    if 'start_time' in data:
        session.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        session.end_time = datetime.fromisoformat(data['end_time'])
    if 'duration' in data:
        session.duration = data['duration']

    db.session.commit()
    return jsonify({'message': 'Session updated'}), 200