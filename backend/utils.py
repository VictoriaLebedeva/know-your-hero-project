import jwt
import uuid
import os
from datetime import datetime, timezone, timedelta
from models import RefreshToken

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


def generate_jwt(user_id, role, expiry):
    """Generates a JWT token with user ID, role, and expiration date."""
    expiration_date = datetime.now(timezone.utc) + expiry
    jti = str(uuid.uuid4())
    new_token = jwt.encode(
        {"jti": jti, "user_id": user_id, "role": role, "exp": expiration_date},
        SECRET_KEY,
        algorithm="HS256",
    )

    return new_token, jti, expiration_date


def verify_token(request):
    """Validates JWT token from cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError as e:
        return None


def validate_credentials(data):
    """Validates the input data for login or registration."""
    if not data or not isinstance(data, dict):
        return "Invalid input. JSON body required."
    if not data.get("email"):
        return "Email is required"
    if not data.get("password"):
        return "Password is required"
    return None


def set_auth_cookies_and_refresh_token(
    response, user, session, old_refresh_token_db=None
):
    """Helper to set cookies and create a new refresh token in DB."""
    access_token, _, _ = generate_jwt(user.id, user.role, timedelta(minutes=1))
    refresh_token, jti, expiration_date = generate_jwt(
        user.id, user.role, timedelta(days=30)
    )

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

    if old_refresh_token_db:
        old_refresh_token_db.is_revoked = True
        session.add(old_refresh_token_db)

    new_refresh_token = RefreshToken()
    new_refresh_token.id = jti
    new_refresh_token.set_token(refresh_token)
    new_refresh_token.user_id = user.id
    new_refresh_token.expires_at = expiration_date
    session.add(new_refresh_token)
    session.commit()
    return response
