from flask import Blueprint, request, jsonify
from app.models.order import Order
from app import db
from datetime import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(
        listing_id=data['listing_id'],
        buyer_id=data['buyer_id'],
        quantity=data['quantity'],
        total_price=data['total_price'],
        status=data.get('status', 'pending'),
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created', 'id': order.id}), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({
        'id': order.id,
        'listing_id': order.listing_id,
        'buyer_id': order.buyer_id,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'status': order.status,
        'created_at': order.created_at.isoformat() if order.created_at else None
    }), 200

@order_bp.route('/orders', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'listing_id': order.listing_id,
            'buyer_id': order.buyer_id,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'status': order.status,
            'created_at': order.created_at.isoformat() if order.created_at else None
        })
    return jsonify(result), 200

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    for field in ['quantity', 'total_price', 'status']:
        if field in data:
            setattr(order, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Order updated'}), 200