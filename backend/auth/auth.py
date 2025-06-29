import os
import jwt
from utils import verify_token, generate_jwt, validate_credentials
from flask import Blueprint, request, jsonify, make_response
from models import Session, User, RefreshToken
from datetime import timedelta


# Initialize the Flask application
auth_bp = Blueprint("auth_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """Handles user registration by creating a new user if the email is not already registered. Returns a success message or an error if the email exists."""

    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"message": "Invalid input. JSON body required."}), 400
    required_fields = ["email", "name", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"Missing or empty field: {field}"}), 400

    try:
        session = Session()
        # Check if a user with the given email already exists
        if session.query(User).filter_by(email=data["email"]).first():
            session.close()
            return jsonify({"message": "Email already registered"}), 400

        # Create a new user instance
        new_user = User()
        new_user.email = data["email"]
        new_user.name = data["name"]
        new_user.set_password(data["password"])
        new_user.role = data.get("role", "colleague")

        session.add(new_user)
        session.commit()
        session.close()
    
    except Exception as e:
        if "session" in locals():
            session.rollback()
            session.close()
        return jsonify({"message": f"Database error: {str(e)}"}), 500

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Authenticates a user by verifying email and password, then issues a JWT token as an HTTP-only cookie if successful."""

    data = request.get_json()
    error = validate_credentials(data)
    if error:
        return jsonify({"message": error}), 400

    try:
        session = Session()
        user = session.query(User).filter_by(email=data["email"]).first()

        if not user:
            return jsonify({"message": f"User with {data['email']} doesn't exist"}), 401
        elif not user.check_password(data["password"]):
            return jsonify({"message": f"Incorrect password"}), 401
        else:
            response = make_response(jsonify({"message": "Login successful"}))
            access_token, _ = generate_jwt(user.id, user.role, timedelta(minutes=15))
            refresh_token, expiration_date = generate_jwt(user.id, user.role, timedelta(days=30))
            print('Refresh:', refresh_token)
            print('Expiraion:', expiration_date)

            response.set_cookie(
                "access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            response.set_cookie(
                "refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            
            
            new_refresh_token = RefreshToken()
            new_refresh_token.set_token(refresh_token) 
            new_refresh_token.user_id = user.id
            new_refresh_token.expires_at = expiration_date
            session.add(new_refresh_token)
            session.commit()
            
        session.close()

    except Exception as e:
        if "session" in locals():
            session.rollback()
            session.close()
        return jsonify({"message": f"Database error: {str(e)}"}), 500

    return response


@auth_bp.route("/api/users", methods=["GET"])
def get_users():
    """Retrieves a list of all users with their id, name, and email."""

    token_payload = verify_token(request)

    if token_payload is None:
        return jsonify({"message": "Unathorized"}), 401

    session = Session()
    users = session.query(User).all()

    return jsonify(
        [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    )


@auth_bp.route("/api/me", methods=["GET"])
def get_user():
    """Fetches information about the currently authorized user based on the JWT token in the request."""

    user_id = None
    token_payload = verify_token(request)

    if token_payload is None:
        return jsonify({"message": "Unathorized"}), 401

    user_id = token_payload.get("user_id")

    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
        }
    )


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logs out the current user by clearing the authentication cookie."""

    token_payload = verify_token(request)

    if token_payload is None:
        return jsonify({"message": "Unathorized"}), 401

    response = make_response(jsonify({"message": "Log Out successful!"}))
    response.set_cookie(
        "access_token", value="", max_age=0, httponly=True, secure=False, samesite="Lax"
    )
    response.set_cookie(
        "refresh_token", value="", max_age=0, httponly=True, secure=False, samesite="Lax"
    )

    return response
