import jwt
import uuid
import os
from datetime import datetime, timezone, timedelta

from flask import current_app

from models.models import RefreshToken, Session
from errors.api_errors import (
    MissingTokenError,
    ExpiredTokenError,
    InvalidTokenError,
    ServerError,
    DatabaseError,
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
        return decoded

    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError(token_name)
    except jwt.InvalidTokenError:
        raise InvalidTokenError(token_name)
    except Exception as e:
        raise ServerError()


def create_token(response, token_name, expiry, user_info):

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
