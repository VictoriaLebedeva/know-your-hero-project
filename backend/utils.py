import jwt
import os

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")

def verify_token(request):
    """Validates JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    token = auth_header.split(" ")[1]
    
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded  # Return decoded user data if valid
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
