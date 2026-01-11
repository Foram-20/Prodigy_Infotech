from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from functools import wraps
from models import User, db
from config import Config

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = Config.SECRET_KEY

# JWT Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Role check decorator
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            if user.role != role:
                return jsonify({'message': 'You are not authorized!'}), 403
            return f(user, *args, **kwargs)
        return decorated
    return wrapper

# Register
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_pw, role=data.get('role', 'user'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials!'}), 401

# Protected
@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role
    })

# Admin-only route
@auth_bp.route('/admin-data', methods=['GET'])
@token_required
@role_required('admin')
def admin_route(current_user):
    return jsonify({'message': f'Hello {current_user.username}, you are an admin!'})
