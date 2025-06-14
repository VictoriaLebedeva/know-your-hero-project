import os
import jwt
from flask import Blueprint, request, jsonify, make_response
from models import Session, Review
from datetime import datetime, timedelta, timezone


# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")

def verify_token():
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



@reviews_bp.route("/reviews", methods=["GET", "POST"])
def handle_reviews():

    if verify_token() is None:
        return jsonify({"message": "Unathorized"}), 401    
    
    session = Session()
    
    if request.method == "POST":
        data = request.get_json()
        
        new_review = Review()
        new_review.positive = data["positive"]
        new_review.negative = data["negative"]
        new_review.adresed_id = data["adresed_id"]
        new_review.author_id = data["author_id"]
        
        session.add(new_review)
        session.commit()
        session.close()

        return jsonify({"message": "Review created successfully"}), 201

    
    reviews = session.query(Review).all()
    session.close()
    return jsonify(
        [
            {
                "id": review.id,
                "positive": reviews.positive,
                "negative": reviews.negative,
                "adresed_id": reviews.adresed_id,
                "author_id": reviews.author_id,
                "created_at": reviews.created_at,
            }
            for review in reviews
        ]
    ), 200