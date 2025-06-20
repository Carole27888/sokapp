from flask import Blueprint, jsonify

sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/sample', methods=['GET'])
def sample_route():
    return jsonify({'message': 'This is a sample route from sample_bp'})
