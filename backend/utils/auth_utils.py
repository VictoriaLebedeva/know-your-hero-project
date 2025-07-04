import jwt
import uuid
import os
from datetime import datetime, timezone, timedelta
from models.models import RefreshToken

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
    access_token, _, _ = generate_jwt(user.id, user.role, timedelta(days=15))
    refresh_token, jti, expiration_date = generate_jwt(
        user.id, user.role, timedelta(days=90)
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
        revoke_refresh_token(old_refresh_token_db.id, session)

    new_refresh_token = RefreshToken()
    new_refresh_token.id = jti
    new_refresh_token.set_token(refresh_token)
    new_refresh_token.user_id = user.id
    new_refresh_token.expires_at = expiration_date
    session.add(new_refresh_token)
    session.commit()
    return response


def revoke_refresh_token(jti: str, session):
    """Revokes the refresh token with the given jti in the database."""
    refresh_token_db = session.query(RefreshToken).filter_by(id=jti).first()

    if refresh_token_db:
        refresh_token_db.is_revoked = True
        session.add(refresh_token_db)
        session.commit()
        return True
    return False


def get_jti_from_refresh_token(request):
    """Extracts jti from refresh_token in cookies, returns None if invalid or missing."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return None
    try:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("jti")
    except Exception:
        return None


def revoke_refresh_token_by_request(request, session):
    """Revokes refresh token from request cookies if possible."""
    jti = get_jti_from_refresh_token(request)
    if not jti:
        return False
    return revoke_refresh_token(jti, session)
