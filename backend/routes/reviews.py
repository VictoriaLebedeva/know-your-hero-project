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
from utils.general_utils import check_required_fields

# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)


@reviews_bp.route("/api/reviews", methods=["GET", "POST"])
def handle_reviews():
    """Handles creating and retrieving reviews."""
    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    try:
        with Session() as session:
            if request.method == "POST":
                data = request.get_json()

                # check required fields
                required_fields = ["adresed_id"]
                check_required_fields(data, required_fields)

                # any of positive or negative reviews should be filled
                if not (
                    (data.get("positive") or "").strip()
                    or (data.get("negative") or "").strip()
                ):
                    raise MissingFieldsError()

                # check if user tries to create reviews about themselves
                if user_id == data["adresed_id"]:
                    raise SelfReviewNotAllowedError()

                target_user = (
                    session.query(User).filter_by(id=data["adresed_id"]).first()
                )
                if not target_user:
                    raise ReviewTargetNotFoundError()

                new_review = Review(
                    positive=data["positive"],
                    negative=data["negative"],
                    adresed_id=target_user.id,
                    author_id=user_id
                )
                session.add(new_review)
                session.commit()
                return jsonify({"message": "Review created successfully"}), 201

            # GET
            reviews = session.query(Review).order_by(Review.created_at.desc()).all()
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

    except (MissingFieldsError, SelfReviewNotAllowedError, ReviewTargetNotFoundError):
        raise
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error processing review data")
