from flask import Blueprint, jsonify, request
from models import db, User
from cache_config import cache
from utils import measure_time

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
@measure_time
@cache.cached(key_prefix='all_users')
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

@api.route('/users', methods=['POST'])
@measure_time
def add_user():
    data = request.json
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    cache.delete('all_users')  # ❌ Invalidate
    return jsonify({'message': 'User added'}), 201

@api.route('/users/<int:id>', methods=['PUT'])
@measure_time
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    cache.delete('all_users')  # ❌ Invalidate
    return jsonify({'message': 'User updated'})

@api.route('/users/<int:id>', methods=['DELETE'])
@measure_time
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    cache.delete('all_users')  # ❌ Invalidate
    return jsonify({'message': 'User deleted'})
    