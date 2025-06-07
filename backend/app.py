from flask import Flask, request, jsonify
from models import init_db, Session, User

# app initialization
app = Flask(__name__)
init_db()

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    session = Session()
    
    # check if User exists
    if session.query(User).filter_by(email=data['email']).first():
        session.close()
        return jsonify({'message': 'Email already registered'}), 400
    
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
