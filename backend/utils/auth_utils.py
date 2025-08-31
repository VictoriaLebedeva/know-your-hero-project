import jwt
import uuid
import re
from datetime import datetime, timezone, timedelta

from flask import current_app
from flask import jsonify, make_response, current_app
from sqlalchemy import select, func

from models.models import RefreshToken, User, Session
from errors.api_errors import (
    MissingTokenError,
    ExpiredTokenError,
    InvalidTokenError,
    DatabaseError,
    TokenNotFoundError,
    TokenRevokedError,
    InvalidEmailFormat,
    TokenUserNotFoundError,
)


def generate_jwt(user_id, role, expiry):
    """Generates a JWT token with user ID, role, and expiration date."""

    expiration_date = datetime.now(timezone.utc) + timedelta(seconds=expiry)
    jti = str(uuid.uuid4())

    new_token = jwt.encode(
        {"jti": jti, "user_id": user_id, "role": role, "exp": expiration_date},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return new_token, jti, expiration_date


def decode_token(token, verify_exp=True):
    return jwt.decode(
        token,
        current_app.config["SECRET_KEY"],
        algorithms=["HS256"],
        options={"verify_exp": verify_exp},
    )


def verify_token(request, token_name):
    """Validates JWT token from cookie"""

    token = request.cookies.get(token_name)

    if token is None:
        raise MissingTokenError(token_name)

    try:
        decoded = decode_token(token)

        user_id = decoded.get("user_id")
        with Session() as session:
            # check if email exists in database
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise TokenUserNotFoundError()

            return decoded

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError(token_name)
    except jwt.InvalidTokenError:
        raise InvalidTokenError(token_name)


def create_token(response, token_name, expiry, user_info):
    """Creates a JWT token and sets it in the response cookie."""
    expiration_date = datetime.now(timezone.utc) + timedelta(seconds=expiry)
    jti = str(uuid.uuid4())

    new_token = jwt.encode(
        {
            "jti": jti,
            "user_id": str(user_info.id),
            "role": user_info.role,
            "exp": expiration_date,
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    response.set_cookie(
        token_name,
        value=new_token,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    if token_name == "refresh_token":
        try:
            with Session() as session:
                new_refresh_token = RefreshToken(
                    id=jti, user_id=str(user_info.id), expires_at=expiration_date
                )
                new_refresh_token.set_token(new_token)
                session.add(new_refresh_token)
                session.commit()
        except Exception as e:
            current_app.logger.error(f"Database error: {str(e)}")
            raise DatabaseError("Error processing review data")

    return response


def revoke_refresh_token(jti, session):
    """Revokes a refresh token by marking it as revoked in the database."""
    token = session.query(RefreshToken).filter_by(id=jti).first()

    if not token:
        raise TokenNotFoundError
    if token.is_revoked:
        raise TokenRevokedError

    token.is_revoked = True
    session.add(token)
    session.commit()


def validate_email_format(email):
    """Validates the format of an email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not bool(re.match(pattern, email)):
        raise InvalidEmailFormat()


def check_user_locked(session, user):
    if not user.lock_login_until:
        return None

    db_now = session.execute(select(func.now())).scalar_one()  # get DB time
    if user.lock_login_until > db_now:
        return int((user.lock_login_until - db_now).total_seconds())
    return None


def revoke_user_refresh_tokens(session, user_id):
    """Revoke all active refresh tokens"""
    session.query(RefreshToken).filter(
        RefreshToken.user_id == user_id, RefreshToken.is_revoked.is_(False)
    ).update({RefreshToken.is_revoked: True}, synchronize_session=False)


def create_auth_response(user, message):
    """Create response with access and refresh tokens"""
    response = make_response(jsonify({"message": message}))

    response = create_token(
        response=response,
        token_name="access_token",
        expiry=current_app.config["ACCESS_TOKEN_EXPIRES_SECONDS"],
        user_info=user,
    )

    response = create_token(
        response=response,
        token_name="refresh_token",
        expiry=current_app.config["REFRESH_TOKEN_EXPIRES_SECONDS"],
        user_info=user,
    )

    return response


def create_auth_response(message, user=None, logout=False):
    """
    Response:
    - if logout=True (or user is None), clear cookies
    - else return access_token and refresh_token
    """
    response = make_response(jsonify({"message": message}))

    if logout or user is None:
        for name in ("access_token", "refresh_token"):
            response.set_cookie(
                name, value="", max_age=0, httponly=True, secure=False, samesite="Lax"
            )
        return response

    # create tokens
    response = create_token(
        response=response,
        token_name="access_token",
        expiry=current_app.config["ACCESS_TOKEN_EXPIRES_SECONDS"],
        user_info=user,
    )
    response = create_token(
        response=response,
        token_name="refresh_token",
        expiry=current_app.config["REFRESH_TOKEN_EXPIRES_SECONDS"],
        user_info=user,
    )
    return response
