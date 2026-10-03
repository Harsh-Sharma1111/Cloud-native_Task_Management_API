import datetime
import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from app.models import User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Invalid credentials"}), 401
    
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        # Generate JWT with 1-day expiry
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 200
        
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    from werkzeug.security import generate_password_hash
    from app import db
    
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"error": "Missing required fields (name, email, password)"}), 400
        
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists"}), 409
        
    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role='member'
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate JWT with 1-day expiry
    token = jwt.encode(
        {
            'user_id': new_user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        },
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    
    return jsonify({
        "token": token,
        "user": new_user.to_dict()
    }), 201
