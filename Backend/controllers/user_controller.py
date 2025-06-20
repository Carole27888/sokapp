from flask import request, jsonify
from app.models.user import User
from app.extensions import db

# Create a new user
def create_user():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        hashed_password=data.get('hashed_password'),  # You should hash this before saving
        role=data.get('role', 'farmer')  # Default to 'farmer' if not provided
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201


# Get all users
def get_all_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active
        })
    return jsonify(users_data), 200


# Get a single user
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active
    }), 200


# Update a user
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.is_active = data.get('is_active', user.is_active)

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


# Delete a user
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200
