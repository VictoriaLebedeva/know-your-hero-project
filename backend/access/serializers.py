from .access import visible_fields


def serialize_review_for_role(review, role):
    row = {
        "id": str(review.id),
        "created_at": review.created_at,
        "recipient_id": str(review.recipient_id),
        "recipient_name": review.recipient.name,
        "author_id": str(review.author_id),
        "author_name": review.author.name,
        "positive": review.positive,
        "negative": review.negative,
    }
    allowed = visible_fields(role)
    return {k: v for k, v in row.items() if k in allowed}
