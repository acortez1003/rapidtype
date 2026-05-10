from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db, bcrypt
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Not valid input
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    # Email exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Username exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username taken'}), 409
    
    # Hashing the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, email=email, password_hash=password_hash)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Something went wrong'}), 500

    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({
        'access_token': access_token,
        'username': new_user.username
    }), 201

@auth.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    user = User.query.filter_by(username=login).first() or User.query.filter_by(email=login).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'username': user.username 
    }), 200