from datetime import timedelta, timezone

import jwt
from errors.api_errors import (
    AccountLockError,
    EmailExistsError,
    ExpiredTokenError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from flask import Blueprint, current_app, jsonify, request
from models.models import Session, User
from sqlalchemy import func, select
from utils.auth_utils import (
    check_user_locked,
    create_auth_response,
    decode_token,
    revoke_refresh_token,
    revoke_user_refresh_tokens,
    validate_email_format,
    verify_token,
)
from utils.general_utils import check_required_fields

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

    email = data["email"].strip().lower()
    validate_email_format(email)

    with Session.begin() as session:
        # check if a user with the given email already exists
        if session.execute(
            select(User.id).where(User.email == email)
        ).scalar_one_or_none():
            raise EmailExistsError()

        # create a new user instance
        new_user = User(
            email=email,
            name=data["name"].strip(),
            role="colleague",
        )
        new_user.set_password(data["password"])

        session.add(new_user)
        session.flush()
        session.refresh(new_user, attribute_names=["id", "created_at"])

        return (
            jsonify(
                {
                    "id": str(new_user.id),
                    "email": new_user.email,
                    "name": new_user.name,
                    "role": new_user.role,
                    "created_at": new_user.created_at if new_user.created_at else None,
                }
            ),
            201,
        )


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

    email = data["email"].strip().lower()
    validate_email_format(email)

    with Session() as session:
        # check if email exists in database
        user = session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
        if not user:
            raise InvalidCredentialsError()

        # check if accont is blocked
        retry_after = check_user_locked(session, user)
        if retry_after is not None:
            lock_until_utc = user.lock_login_until.astimezone(timezone.utc)
            raise AccountLockError(lock_until_utc)

        # check if password is correct
        if not user.check_password(data["password"]):
            attempts = (user.failed_login_attempts or 0) + 1
            limit = current_app.config["LOCKOUT_ATTEMPTS"]

            if attempts >= limit:
                duration = current_app.config["LOCKOUT_DURATION_SECONDS"]
                db_now = session.execute(select(func.now())).scalar_one()  # get DB time
                user.failed_login_attempts = 0
                user.lock_login_until = db_now + timedelta(seconds=duration)
            else:
                user.failed_login_attempts = attempts

            session.commit()
            raise InvalidCredentialsError()

        revoke_user_refresh_tokens(session, user.id)

        user.failed_login_attempts = 0
        session.commit()

        return create_auth_response("Login successful", user)


@auth_bp.route("/api/users", methods=["GET"])
def get_users():
    """Retrieves a list of all users with their id, name, and email."""

    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    with Session() as session:
        users = session.execute(select(User).where(User.id != user_id)).scalars().all()
        return jsonify(
            [
                {"id": str(user.id), "name": user.name, "email": user.email}
                for user in users
            ]
        )


@auth_bp.route("/api/me", methods=["GET"])
def get_user():
    """Fetches information about the currently authorized user based on the JWT token in the request."""

    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    with Session() as session:
        user = session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()
        if not user:
            raise UserNotFoundError()

        return (
            jsonify(
                {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at,
                }
            ),
            200,
        )


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh():
    """Refreshes the authentication token using the refresh token stored in cookies.
    If the refresh token is valid, a new access token and refresh token are issued."""

    token = request.cookies.get("refresh_token")
    
    try:
        token_payload = verify_token(request, "refresh_token")
        jti = token_payload.get("jti")
        user_id = token_payload.get("user_id")
        
        with Session() as session:
            user = session.get(User, user_id)
            if not user:
                raise UserNotFoundError()
            revoke_refresh_token(jti, session)
            return create_auth_response("Token refresh successful", user)
        
    except ExpiredTokenError:
        current_app.logger.warning("This logic brunch")
        payload = decode_token(token, verify_exp=False)
        current_app.logger.warning(f"This logic brunch {payload}")
        jti = payload.get("jti")
        if jti:
            with Session() as session:
                revoke_refresh_token(jti, session)
        raise


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    refresh_token = request.cookies.get("refresh_token")
    response = create_auth_response("Log Out", logout=True)

    if not refresh_token:
        return response

    try:
        payload = decode_token(refresh_token, verify_exp=False)
        jti = payload.get("jti")

        if jti:
            with Session.begin() as session:
                revoke_refresh_token(jti, session)
        return response
    except jwt.InvalidSignatureError:
        current_app.logger.warning(
            "Logout: refresh token signature invalid. Revocation skipped. Cookies cleared."
        )
        return response
    except Exception:
        return response
