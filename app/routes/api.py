from functools import wraps
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Group
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)


# API Authentication decorator
def api_admin_required(f):
    """Decorator to require admin for API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if not session.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ============= USER ENDPOINTS =============

@api_bp.route('/users', methods=['GET'])
@api_admin_required
def get_users():
    """Get all users - Admin only"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@api_admin_required
def get_user(user_id):
    """Get specific user by ID - Admin only"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@api_bp.route('/users', methods=['POST'])
@api_admin_required
def create_user():
    """Create new user - Admin only"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email and password are required'}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False),
            is_active=data.get('is_active', True)
        )
        user.set_password(data['password'])
        
        # Add groups if provided
        if 'group_ids' in data:
            groups = Group.query.filter(Group.id.in_(data['group_ids'])).all()
            user.groups = groups
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@api_admin_required
def update_user(user_id):
    """Update existing user - Admin only"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    try:
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'password' in data:
            user.set_password(data['password'])
        
        # Update groups if provided
        if 'group_ids' in data:
            groups = Group.query.filter(Group.id.in_(data['group_ids'])).all()
            user.groups = groups
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@api_admin_required
def delete_user(user_id):
    """Delete user - Admin only"""
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@api_admin_required
def activate_user(user_id):
    """Activate user - Admin only"""
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    return jsonify(user.to_dict()), 200


@api_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@api_admin_required
def deactivate_user(user_id):
    """Deactivate user - Admin only"""
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return jsonify(user.to_dict()), 200


@api_bp.route('/users/<int:user_id>/make-admin', methods=['POST'])
@api_admin_required
def make_admin(user_id):
    """Make user admin - Admin only"""
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    return jsonify(user.to_dict()), 200


@api_bp.route('/users/<int:user_id>/remove-admin', methods=['POST'])
@api_admin_required
def remove_admin(user_id):
    """Remove admin privileges - Admin only"""
    user = User.query.get_or_404(user_id)
    user.is_admin = False
    db.session.commit()
    return jsonify(user.to_dict()), 200


@api_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@api_admin_required
def reset_password(user_id):
    """Reset user password - Admin only"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data or not data.get('new_password'):
        return jsonify({'error': 'New password is required'}), 400
    
    user.set_password(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password reset successfully'}), 200


@api_bp.route('/users/<int:user_id>/groups', methods=['POST'])
@api_admin_required
def add_user_to_groups(user_id):
    """Add user to groups - Admin only"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data or 'group_ids' not in data:
        return jsonify({'error': 'group_ids are required'}), 400
    
    groups = Group.query.filter(Group.id.in_(data['group_ids'])).all()
    
    for group in groups:
        if group not in user.groups:
            user.groups.append(group)
    
    db.session.commit()
    return jsonify(user.to_dict()), 200


@api_bp.route('/users/<int:user_id>/groups/<int:group_id>', methods=['DELETE'])
@api_admin_required
def remove_user_from_group(user_id, group_id):
    """Remove user from group - Admin only"""
    user = User.query.get_or_404(user_id)
    group = Group.query.get_or_404(group_id)
    
    if group in user.groups:
        user.groups.remove(group)
        db.session.commit()
    
    return jsonify(user.to_dict()), 200


# ============= GROUP ENDPOINTS =============

@api_bp.route('/groups', methods=['GET'])
def get_groups():
    """Get all groups"""
    groups = Group.query.all()
    return jsonify([group.to_dict() for group in groups]), 200


@api_bp.route('/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """Get specific group by ID"""
    group = Group.query.get_or_404(group_id)
    return jsonify(group.to_dict()), 200


@api_bp.route('/groups', methods=['POST'])
def create_group():
    """Create new group"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Group name is required'}), 400
    
    try:
        group = Group(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(group)
        db.session.commit()
        
        return jsonify(group.to_dict()), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Group name already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """Update existing group"""
    group = Group.query.get_or_404(group_id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            group.name = data['name']
        if 'description' in data:
            group.description = data['description']
        
        db.session.commit()
        return jsonify(group.to_dict()), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Group name already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete group"""
    group = Group.query.get_or_404(group_id)
    
    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': 'Group deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/groups/<int:group_id>/users', methods=['GET'])
def get_group_users(group_id):
    """Get all users in a group"""
    group = Group.query.get_or_404(group_id)
    return jsonify([user.to_dict() for user in group.users]), 200


