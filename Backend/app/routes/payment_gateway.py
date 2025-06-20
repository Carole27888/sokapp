from flask import Blueprint, request, jsonify
from app.models.payment_gateway import PaymentGatewayLog
from app import db
from datetime import datetime

payment_gateway_bp = Blueprint('payment_gateway', __name__)

@payment_gateway_bp.route('/payment_gateway_logs', methods=['POST'])
def create_payment_gateway_log():
    try:
        data = request.get_json(force=True)
        print("Received data for payment gateway log:", data)
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({'error': 'Invalid JSON', 'details': str(e)}), 400

    log = PaymentGatewayLog(
        provider=data['provider'],
        payload=data.get('payload'),
        response=data.get('response'),
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Payment gateway log created', 'id': log.id}), 201

@payment_gateway_bp.route('/payment_gateway_logs/<int:log_id>', methods=['GET'])
def get_payment_gateway_log(log_id):
    log = PaymentGatewayLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Payment gateway log not found'}), 404
    return jsonify({
        'id': log.id,
        'provider': log.provider,
        'payload': log.payload,
        'response': log.response,
        'timestamp': log.timestamp.isoformat() if log.timestamp else None
    }), 200

@payment_gateway_bp.route('/payment_gateway_logs', methods=['GET'])
def list_payment_gateway_logs():
    logs = PaymentGatewayLog.query.all()
    result = []
    for log in logs:
        result.append({
            'id': log.id,
            'provider': log.provider,
            'payload': log.payload,
            'response': log.response,
            'timestamp': log.timestamp.isoformat() if log.timestamp else None
        })
    return jsonify(result), 200