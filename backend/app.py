from flask import Flask, request, jsonify
from models import init_db, Session, User

# Initialize the Flask application
app = Flask(__name__)

# Initialize the database (this function sets up the database connection and tables)
init_db()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)