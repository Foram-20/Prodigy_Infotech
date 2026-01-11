from flask import Flask, request, jsonify
from models import db, User
from config import Config
import re
from flask_migrate import Migrate

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name, email, age = data.get('name'), data.get('email'), data.get('age')

    if not name or not email or not age:
        return jsonify({'error': 'Missing fields'}), 400
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'error': 'Invalid email'}), 400

    user = User(name=name, email=email, age=age)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'name': u.name, 'email': u.email, 'age': u.age}
        for u in users
    ]), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if 'email' in data and not re.match(EMAIL_REGEX, data['email']):
        return jsonify({'error': 'Invalid email'}), 400

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
