from flask import Blueprint, request, jsonify
from app.models.user_profile import User_Profile
from app import db

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/user_profiles', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    profile = User_Profile(
        user_id=data['user_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data.get('phone_number'),
        address=data.get('address'),
        profile_picture=data.get('profile_picture'),
        is_verified=data.get('is_verified', False),
        is_active=data.get('is_active', True),
        location=data.get('location'),
        bio=data.get('bio'),
        social_links=data.get('social_links'),
        received_notifications=data.get('received_notifications', True),
        favorite_products=data.get('favorite_products')
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'User profile created', 'id': profile.id}), 201

@user_profile_bp.route('/user_profiles/<int:profile_id>', methods=['GET'])
def get_user_profile(profile_id):
    profile = User_Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    return jsonify({
        'id': profile.id,
        'user_id': profile.user_id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'phone_number': profile.phone_number,
        'address': profile.address,
        'profile_picture': profile.profile_picture,
        'is_verified': profile.is_verified,
        'is_active': profile.is_active,
        'created_at': profile.created_at.isoformat() if profile.created_at else None,
        'updated_at': profile.updated_at.isoformat() if profile.updated_at else None,
        'location': profile.location,
        'bio': profile.bio,
        'social_links': profile.social_links,
        'received_notifications': profile.received_notifications,
        'favorite_products': profile.favorite_products
    }), 200

@user_profile_bp.route('/user_profiles', methods=['GET'])
def list_user_profiles():
    profiles = User_Profile.query.all()
    result = []
    for profile in profiles:
        result.append({
            'id': profile.id,
            'user_id': profile.user_id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'profile_picture': profile.profile_picture,
            'is_verified': profile.is_verified,
            'is_active': profile.is_active,
            'created_at': profile.created_at.isoformat() if profile.created_at else None,
            'updated_at': profile.updated_at.isoformat() if profile.updated_at else None,
            'location': profile.location,
            'bio': profile.bio,
            'social_links': profile.social_links,
            'received_notifications': profile.received_notifications,
            'favorite_products': profile.favorite_products
        })
    return jsonify(result), 200

@user_profile_bp.route('/user_profiles/<int:profile_id>', methods=['PUT'])
def update_user_profile(profile_id):
    profile = User_Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404

    data = request.get_json()
    for field in [
        'first_name', 'last_name', 'phone_number', 'address', 'profile_picture',
        'is_verified', 'is_active', 'location', 'bio', 'social_links',
        'received_notifications', 'favorite_products'
    ]:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()
    return jsonify({'message': 'User profile updated'}), 200