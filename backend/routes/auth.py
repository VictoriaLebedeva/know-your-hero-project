import os
import jwt
import uuid
from utils.auth_utils import (
    verify_token,
    validate_credentials,
    set_auth_cookies_and_refresh_token,
    revoke_refresh_token_by_request,
)
from flask import Blueprint, request, jsonify, make_response
from models.models import Session, User, RefreshToken


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
        with Session() as session:
            # Check if a user with the given email already exists
            if session.query(User).filter_by(email=data["email"]).first():
                return jsonify({"message": "Email already registered"}), 400

            # Create a new user instance
            new_user = User()
            new_user.id = str(uuid.uuid4())
            new_user.email = data["email"]
            new_user.name = data["name"]
            new_user.set_password(data["password"])
            new_user.role = data.get("role", "colleague")

            session.add(new_user)
            session.commit()

    except Exception as e:
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
        with Session() as session:
            user = session.query(User).filter_by(email=data["email"]).first()
            if not user:
                return (
                    jsonify({"message": f"User with {data['email']} doesn't exist"}),
                    401,
                )
            elif not user.check_password(data["password"]):
                return jsonify({"message": f"Incorrect password"}), 401
            else:
                response = make_response(jsonify({"message": "Login successful"}))
                response = set_auth_cookies_and_refresh_token(response, user, session)
            return response
    except Exception as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500


@auth_bp.route("/api/users", methods=["GET"])
def get_users():
    """Retrieves a list of all users with their id, name, and email."""

    token_payload = verify_token(request)

    if token_payload is None:
        return jsonify({"message": "Unathorized"}), 401

    with Session() as session:
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

    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
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


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh():
    """Refreshes the authentication token using the refresh token stored in cookies.
    If the refresh token is valid, a new access token and refresh token are issued."""

    refresh_token = request.cookies.get("refresh_token")
    decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    
    jti = decoded.get("jti")
    user_id = decoded.get("user_id")
    
    try:
        with Session() as session:
            refresh_token_db = session.query(RefreshToken).filter_by(id=jti).first()
            user = session.query(User).filter_by(id=user_id).first()

            if not refresh_token_db:
                return jsonify({"message": f"No such token in a database"}), 401
            elif not user:
                return jsonify({"message": f"No such user in a database"}), 401
            else:
                response = make_response(jsonify({"message": "Login successful"}))
                response = set_auth_cookies_and_refresh_token(
                    response, user, session, old_refresh_token_db=refresh_token_db
                )

            return response

    except Exception as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500



@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logs out the current user by clearing the authentication cookie and revoking the refresh token in the database."""
    with Session() as session:
        revoked = revoke_refresh_token_by_request(request, session)
    if not revoked:
        return jsonify({"message": "No valid refresh token found or already revoked"}), 401

    response = make_response(jsonify({"message": "Log Out successful!"}))
    response.set_cookie(
        "access_token", value="", max_age=0, httponly=True, secure=False, samesite="Lax"
    )
    response.set_cookie(
        "refresh_token",
        value="",
        max_age=0,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    return response