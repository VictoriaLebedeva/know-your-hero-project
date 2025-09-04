from enum import Enum


class Role(str, Enum):
    super_rat = "super_rat"
    rat = "rat"
    colleague = "colleague"
    guest = "guest"


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
    Role.guest: {"id", "created_at", "positive", "recipient_id", "recipient_name"},
}


def visible_fields(role):
    return VISIBLE_FIELDS_BY_ROLE.get(role, VISIBLE_FIELDS_BY_ROLE[Role.guest])


def list_row_filters(role):
    return {"positive_only": role in (Role.guest, Role.colleague)}
