import jwt
import os

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")

def verify_token(request):
    """Validates JWT token from cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("⚠️ Token Expired")
        return None
    except jwt.InvalidTokenError as e:
        print("⚠️ Incalid token:", e)
        return None

