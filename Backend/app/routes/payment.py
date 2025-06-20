from flask import Blueprint, request, jsonify
from app.models.payment import Payment
from app import db
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    try:
        payment = Payment(
            user_id=data['user_id'],
            amount=data['amount'],
            payment_method=data['payment_method'],
            status=data.get('status', 'pending'),
            transaction_id=data.get('transaction_id'),
            related_order_id=data.get('related_order_id'),
            description=data.get('description'),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else datetime.utcnow(),
            updated_at=datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else datetime.utcnow()
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify({'message': 'Payment created', 'id': payment.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify({
        'id': payment.id,
        'user_id': payment.user_id,
        'amount': payment.amount,
        'payment_method': payment.payment_method,
        'status': payment.status,
        'transaction_id': payment.transaction_id,
        'created_at': payment.created_at.isoformat() if payment.created_at else None,
        'updated_at': payment.updated_at.isoformat() if payment.updated_at else None,
        'related_order_id': payment.related_order_id,
        'description': payment.description
    }), 200

@payment_bp.route('/payments', methods=['GET'])
def list_payments():
    payments = Payment.query.all()
    result = []
    for payment in payments:
        result.append({
            'id': payment.id,
            'user_id': payment.user_id,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'status': payment.status,
            'transaction_id': payment.transaction_id,
            'created_at': payment.created_at.isoformat() if payment.created_at else None,
            'updated_at': payment.updated_at.isoformat() if payment.updated_at else None,
            'related_order_id': payment.related_order_id,
            'description': payment.description
        })
    return jsonify(result), 200

@payment_bp.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    data = request.get_json()
    for field in [
        'amount', 'payment_method', 'status', 'transaction_id',
        'related_order_id', 'description'
    ]:
        if field in data:
            setattr(payment, field, data[field])
    payment.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Payment updated'}), 200