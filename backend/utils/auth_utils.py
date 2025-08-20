import jwt
import uuid
import re
from datetime import datetime, timezone, timedelta

from flask import current_app

from models.models import RefreshToken, User, Session
from errors.api_errors import (
    MissingTokenError,
    ExpiredTokenError,
    InvalidTokenError,
    DatabaseError,
    TokenNotFoundError,
    TokenRevokedError,
    InvalidEmailFormat,
    TokenUserNotFoundError
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


def verify_token(request, token_name):
    """Validates JWT token from cookie"""

    token = request.cookies.get(token_name)

    if token is None:
        raise MissingTokenError(token_name)

    try:
        decoded = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        
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
            "user_id": user_info.id,
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
                    id=jti, user_id=user_info.id, expires_at=expiration_date
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
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    try:
        if not bool(re.match(pattern, email)):
            raise InvalidEmailFormat()
    except InvalidEmailFormat:
        raise
