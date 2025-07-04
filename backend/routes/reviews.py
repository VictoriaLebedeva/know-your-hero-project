import os
from utils.auth_utils import verify_token
from flask import Blueprint, current_app, request, jsonify
from models.models import Session, Review, User
from errors.api_errors import (
    SelfReviewNotAllowedError,
    MissingFieldsError,
    ReviewTargetNotFoundError,
    DatabaseError,
)

# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)

# Get SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY")


@reviews_bp.route("/api/reviews", methods=["GET", "POST"])
def handle_reviews():
    """Handles creating and retrieving reviews."""

    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    try:
        with Session() as session:
            # POST
            if request.method == "POST":
                data = request.get_json()

                # check for required fields
                required_fields = ["adresed_id", "author_id"]
                missing_fields = [
                    field
                    for field in required_fields
                    if field not in data or not data[field]
                ]

                if missing_fields:
                    raise MissingFieldsError(missing_fields)

                # check for creating review for user themselves
                if user_id == data["adresed_id"]:
                    raise SelfReviewNotAllowedError()

                # check for existance of addressed user
                target_user = (
                    session.query(User).filter_by(id=data["adresed_id"]).first()
                )
                if not target_user:
                    raise ReviewTargetNotFoundError()

                new_review = Review()
                new_review.positive = data["positive"]
                new_review.negative = data["negative"]
                new_review.adresed_id = data["adresed_id"]
                new_review.author_id = data["author_id"]

                session.add(new_review)
                session.commit()

                return jsonify({"message": "Review created successfully"}), 201

            # GET
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
            return jsonify(reviews_data), 200
    except (MissingFieldsError, SelfReviewNotAllowedError, ReviewTargetNotFoundError) as e:
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")
