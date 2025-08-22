from errors.api_errors import MissingFieldsError


def check_required_fields(data, required_fields):
    """Validates the required fields in the request."""

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise MissingFieldsError(missing_fields)
