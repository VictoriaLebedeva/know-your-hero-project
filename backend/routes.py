from flask import request, jsonify
from models import Session, User
from app import app

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Handles user registration."""
    
    data = request.get_json()
    
    # Create a new database session
    session = Session()
    
    # Check if a user with the given email already exists
    if session.query(User).filter_by(email=data['email']).first():
        session.close()
        return jsonify({'message': 'Email already registered'}), 400
    
    # Create a new user instance
    new_user = User()
    new_user.email = data['email']
    new_user.set_password(data['password'])
    new_user.role = data.get('role', 'colleague')
    
    session.add(new_user)
    session.commit()
    session.close()
    
    return jsonify({'message': 'User created successfully'}), 201