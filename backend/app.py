import os
import jwt
from flask import Flask, request, jsonify
from models import init_db, Session, User
from datetime import datetime, timedelta, timezone


# Initialize the Flask application
app = Flask(__name__)

# Initialize the database
init_db()

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


@app.route("/api/auth/register", methods=["POST"])
def register():
    """Handles user registration."""

    data = request.get_json()

    # Create a new database session
    session = Session()

    # Check if a user with the given email already exists
    if session.query(User).filter_by(email=data["email"]).first():
        session.close()
        return jsonify({"message": "Email already registered"}), 400

    # Create a new user instance
    new_user = User()
    new_user.email = data["email"]
    new_user.set_password(data["password"])
    new_user.role = data.get("role", "colleague")

    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({"message": "User created successfully"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    session = Session()

    user = session.query(User).filter_by(email=data["email"]).first()
    session.close()

    if user and user.check_password(data["password"]):
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        return jsonify({"token": token})


@app.route("/api/users", methods=["GET"])
def get_users():
    session = Session()
    users = session.query(User).all()

    return jsonify(
        [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
            }
            for user in users
        ]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
