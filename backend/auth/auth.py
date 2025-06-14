import os
import jwt
from flask import Blueprint, request, jsonify, make_response
from models import Session, User
from datetime import datetime, timedelta, timezone


# Initialize the Flask application
auth_bp = Blueprint("auth_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")

@auth_bp.route("/api/auth/register", methods=["POST"])
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


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    session = Session()

    user = session.query(User).filter_by(email=data["email"]).first()
    session.close()

    if not user:
        return jsonify({"message": f"User with {data['email']} doesn't exist"}), 401
    elif not user.check_password(data["password"]):
        return jsonify({"message": f"Incorrect password"}), 401
    else: 
        response = make_response(jsonify({"message": "Login successful"}))
        token = jwt.encode(
            {
                "user_id": user.id,
                "role": user.role,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        response.set_cookie(
            "access_token",
            token,
            httponly=True,  # Prevents JavaScript access (protects against XSS)
            secure=False,  # for localhost testing
            samesite=None
        )
        return response     


@auth_bp.route("/api/users", methods=["GET"])
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