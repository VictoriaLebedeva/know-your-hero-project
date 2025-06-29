import jwt
import uuid
import os
from datetime import datetime, timezone

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


def generate_jwt(user_id, role, expiry):

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
        print("Token Expired")
        return None
    except jwt.InvalidTokenError as e:
        print("Incalid token:", e)
        return None


def validate_credentials(data):
    if not data or not isinstance(data, dict):
        return "Invalid input. JSON body required."
    if not data.get("email"):
        return "Email is required"
    if not data.get("password"):
        return "Password is required"
    return None
