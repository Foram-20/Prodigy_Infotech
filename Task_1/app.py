from flask import Flask, request, jsonify
from uuid import uuid4
import re

app = Flask(__name__)

# In-memory data structure
users_db = {}

# Email validation regex
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'


# Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    if not name or not email or not age:
        return jsonify({'error': 'Missing fields'}), 400
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email format'}), 400

    user_id = str(uuid4())
    users_db[user_id] = {'id': user_id, 'name': name, 'email': email, 'age': age}
    return jsonify(users_db[user_id]), 201


# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users_db.values())), 200


# Read single user
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200


# Update user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    if email and not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email format'}), 400

    user = users_db[user_id]
    user['name'] = name or user['name']
    user['email'] = email or user['email']
    user['age'] = age or user['age']

    return jsonify(user), 200


# Delete user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    del users_db[user_id]
    return jsonify({'message': 'User deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
