"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Token blacklist (in production, use Redis or database)
blacklisted_tokens = set()


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    print(f"[DEBUG] Registration attempt with data: {data}")  # Debug logging
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        print(f"[ERROR] Missing required fields")  # Debug logging
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        print(f"[ERROR] Username already exists: {data['username']}")  # Debug logging
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        print(f"[ERROR] Email already exists: {data['email']}")  # Debug logging
        return jsonify({'message': 'Email already exists'}), 409
    
    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        print(f"[DEBUG] User registered successfully: {user.id}")  # Debug logging
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        print(f"[ERROR] Registration failed: {str(e)}")  # Debug logging
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Account is disabled'}), 403
    
    # Create tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user by blacklisting the token"""
    jti = get_jwt()['jti']
    blacklisted_tokens.add(jti)
    
    return jsonify({'message': 'Logout successful'}), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token}), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


# JWT token blacklist check
from app import jwt as jwt_manager

@jwt_manager.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens
