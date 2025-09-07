from enum import Enum


class Role(str, Enum):
    super_rat = "super_rat"
    rat = "rat"
    colleague = "colleague"


VISIBLE_FIELDS_BY_ROLE = {
    Role.super_rat: {
        "id",
        "author_id",
        "author_name",
        "created_at",
        "negative",
        "positive",
        "recipient_id",
        "recipient_name",
    },
    Role.rat: {
        "id",
        "created_at",
        "negative",
        "positive",
        "recipient_id",
        "recipient_name",
    },
    Role.colleague: {"id", "created_at", "positive", "recipient_id", "recipient_name"},
}

CAN_CREATE_NEGATIVE_REVIEW = {
    Role.super_rat: True,
    Role.rat: True,
    Role.colleague: False,
}


def visible_fields(role):
    return VISIBLE_FIELDS_BY_ROLE.get(role, VISIBLE_FIELDS_BY_ROLE[Role.colleague])


def can_create_negative_review(role):
    return CAN_CREATE_NEGATIVE_REVIEW.get(role, False)
