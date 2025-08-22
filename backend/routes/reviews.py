import uuid

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from models.models import Session, Review, User
from errors.api_errors import (
    SelfReviewNotAllowedError,
    ReviewTargetNotFoundError,
    MaxLimitExceededError,
    AtLeastOneNonEmptyError,
)
from utils.general_utils import check_required_fields
from utils.auth_utils import verify_token

# Initialize the Flask application
reviews_bp = Blueprint("reviews_bp", __name__)

# maximum length for
MAX_LEN = 1000


@reviews_bp.route("/api/reviews", methods=["POST"])
def create_review():
    """Handles creating and retrieving reviews."""

    token_payload = verify_token(request, "access_token")
    user_id = token_payload.get("user_id")

    data = request.get_json()

    # check required fields
    required_fields = ["recipient_id", "positive", "negative"]
    check_required_fields(data, required_fields)

    # any of positive or negative reviews should be filled
    if not ((data["positive"] or "").strip() or (data["negative"] or "").strip()):
        raise AtLeastOneNonEmptyError(["positive", "negative"])

    # check for character limit exceed
    if len(data["positive"]) > MAX_LEN or len(data["negative"]) > MAX_LEN:
        raise MaxLimitExceededError(MAX_LEN)

    # check if user tries to create reviews about themselves
    if user_id == data["recipient_id"]:
        raise SelfReviewNotAllowedError()

    with Session.begin() as session:
        target_user = session.get(User, data["recipient_id"])
        if not target_user:
            raise ReviewTargetNotFoundError(data["recipient_id"])

        new_review = Review(
            id=str(uuid.uuid4()),
            positive=data["positive"],
            negative=data["negative"],
            recipient_id=target_user.id,
            author_id=user_id,
        )

        session.add(new_review)
        session.flush()
        session.refresh(new_review, attribute_names=["created_at"])

        return (
            jsonify(
                {
                    "id": new_review.id,
                    "positive": new_review.positive,
                    "negative": new_review.negative,
                    "recipient_id": new_review.recipient_id,
                    "author_id": new_review.author_id,
                    "created_at": (
                        new_review.created_at if new_review.created_at else None
                    ),
                }
            ),
            201,
        )


@reviews_bp.route("/api/reviews", methods=["GET"])
def list_reviews():
    """Handles retrieving reviews."""

    verify_token(request, "access_token")
    with Session() as session:
        reviews = session.scalars(
            select(Review).order_by(Review.created_at.desc())
        ).all()

        reviews_data = [
            {
                "id": review.id,
                "positive": review.positive,
                "negative": review.negative,
                "recipient_id": review.recipient_id,
                "recipient_name": review.recipient.name,
                "author_id": review.author_id,
                "author_name": review.author.name,
                "created_at": review.created_at,
            }
            for review in reviews
        ]
        return jsonify(reviews_data), 200
