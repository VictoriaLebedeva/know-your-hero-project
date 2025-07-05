import os
import uuid

import jwt
from flask import Blueprint, request, jsonify, make_response, current_app

from models.models import Session, User, RefreshToken
from errors.api_errors import (
    UserNotFoundError,
    EmailExistsError,
    DatabaseError,
    InvalidCredentialsError,
    TokenRevokedError,
    TokenNotFoundError,
)
from utils.general_utils import check_required_fields
from utils.auth_utils import verify_token, create_token


# Initialize the Flask application
auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """
    Handles user registration by creating a new user if the email is not already registered.
    Returns a success message or an error if the email exists.
    """
    data = request.get_json()

    required_fields = ["email", "name", "password"]
    check_required_fields(data, required_fields)

    try:
        with Session() as session:
            # check if a user with the given email already exists
            if session.query(User).filter_by(email=data["email"]).first():
                raise EmailExistsError()

            # create a new user instance
            new_user = User(
                id=str(uuid.uuid4()),
                email=data["email"],
                name=data["name"],
                role=data.get("role", "colleague"),
            )
            new_user.set_password(data["password"])

            session.add(new_user)
            session.commit()

    except EmailExistsError:
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Authenticates a user by verifying email and password,
    then issues a JWT token as an HTTP-only cookie if successful.
    """
    data = request.get_json()

    # check for required fields
    required_fields = ["email", "password"]
    check_required_fields(data, required_fields)

    try:
        with Session() as session:
            # check if email exists in database
            user = session.query(User).filter_by(email=data["email"]).first()
            if not user:
                raise UserNotFoundError()

            # check if password is correct
            if not user.check_password(data["password"]):
                raise InvalidCredentialsError()
            
            response = make_response(jsonify({"message": "Login successful"}))
            
            # generate access_token
            response = create_token(
                response=response,
                token_name="access_token",
                expiry=current_app.config["ACCESS_TOKEN_EXPIRES_SECONDS"], 
                user_info=user
            )
            
            # generate refresh_token
            response = create_token(
                response=response,
                token_name="refresh_token",
                expiry=current_app.config["REFRESH_TOKEN_EXPIRES_SECONDS"], 
                user_info=user
            )
                  
            return response

    except (UserNotFoundError, InvalidCredentialsError):
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")


@auth_bp.route("/api/users", methods=["GET"])
def get_users():
    """Retrieves a list of all users with their id, name, and email."""

    verify_token(request, "access_token")

    try:
        with Session() as session:
            users = session.query(User).all()
            return jsonify(
                [
                    {"id": user.id, "name": user.name, "email": user.email}
                    for user in users
                ]
            )
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")


@auth_bp.route("/api/me", methods=["GET"])
def get_user():
    """Fetches information about the currently authorized user based on the JWT token in the request."""

    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    try:
        with Session() as session:

            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise UserNotFoundError()

            return jsonify(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at.isoformat(),
                }
            )
    except UserNotFoundError:
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh():
    """Refreshes the authentication token using the refresh token stored in cookies.
    If the refresh token is valid, a new access token and refresh token are issued."""

    token_payload = verify_token(request, "refresh_token")

    jti = token_payload.get("jti")
    user_id = token_payload.get("user_id")

    try:
        with Session() as session:

            refresh_token_db = session.query(RefreshToken).filter_by(id=jti).first()
            if not refresh_token_db:
                raise TokenNotFoundError()
            if refresh_token_db.is_revoked:
                raise TokenRevokedError()

            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise UserNotFoundError()
            
            # revoke refresh token
            refresh_token_db.is_revoked = True
            session.add(refresh_token_db)
            session.commit()

            response = make_response(jsonify({"message": "Token refresh successful"}))
            
            # generate new access_token
            response = create_token(
                response=response,
                token_name="access_token",
                expiry=current_app.config["ACCESS_TOKEN_EXPIRES_SECONDS"], 
                user_info=user
            )
            
            # generate new refresh_token
            response = create_token(
                response=response,
                token_name="refresh_token",
                expiry=current_app.config["REFRESH_TOKEN_EXPIRES_SECONDS"], 
                user_info=user
            )
                  
            return response

    except (TokenRevokedError, TokenNotFoundError, UserNotFoundError):
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing token")


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logs out the current user by clearing the authentication cookie
    and revoking the refresh token in the database."""

    token_payload = verify_token(request, "refresh_token")
    jti = token_payload.get("jti")

    try:
        with Session() as session:

            refresh_token_db = session.query(RefreshToken).filter_by(id=jti).first()
            if not refresh_token_db:
                raise TokenNotFoundError()
            if refresh_token_db.is_revoked:
                raise TokenRevokedError()

            refresh_token_db.is_revoked = True
            session.add(refresh_token_db)
            session.commit()

    except (TokenNotFoundError, TokenRevokedError) as e:
        current_app.logger.error(f"Refresh Token Error: {str(e)}")
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing token")
    finally:
        response = make_response(jsonify({"message": "Log Out successful!"}))

        response.set_cookie(
            "access_token",
            value="",
            max_age=0,
            httponly=True,
            secure=False,
            samesite="Lax",
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
