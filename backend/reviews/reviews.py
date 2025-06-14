import os
import jwt
from utils import verify_token
from flask import Blueprint, request, jsonify, make_response
from models import Session, Review
from datetime import datetime, timedelta, timezone

# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")

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
    print(reviews)
    session.close()
    
    return jsonify(
        [
            {
                "id": review.id,
                "positive": review.positive,
                "negative": review.negative,
                "adresed_id": review.adresed_id,
                "author_id": review.author_id,
                "created_at": review.created_at,
            }
            for review in reviews
        ]
    ), 200