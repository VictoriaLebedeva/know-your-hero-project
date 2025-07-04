import os
from utils.auth_utils import verify_token
from flask import Blueprint, request, jsonify, make_response
from models.models import Session, Review

# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


@reviews_bp.route("/api/reviews", methods=["GET", "POST"])
def handle_reviews():
    """Handles creating and retrieving reviews."""

    if verify_token(request) is None:
        return jsonify({"message": "Unathorized"}), 401

    try:
        session = Session()
        if request.method == "POST":
            data = request.get_json()
            required_fields = ["adresed_id", "author_id"]
            for field in required_fields:
                if field not in data or not data[field]:
                    session.close()
                    return jsonify({"message": f"Missing or empty field: {field}"}), 400
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
        reviews_data = [
            {
                "id": review.id,
                "positive": review.positive,
                "negative": review.negative,
                "adresed_id": review.adresed_id,
                "adresed_name": review.adresed.name,
                "author_id": review.author_id,
                "author_name": review.author.name,
                "created_at": review.created_at,
            }
            for review in reviews
        ]
        session.close()
        return jsonify(reviews_data), 200
    except Exception as e:
        if "session" in locals():
            session.close()
        return jsonify({"message": f"Database error: {str(e)}"}), 500
