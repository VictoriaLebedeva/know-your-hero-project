from flask import jsonify
from werkzeug.exceptions import HTTPException
from errors.error_codes import ErrorCodes


class APIError(Exception):
    """Base class for all API errors"""

    def __init__(self, message, status_code, error_code):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

    def to_response(self):
        return (
            jsonify({"error": {"code": self.error_code, "message": self.message}}),
            self.status_code,
        )


# Auth errors
class InvalidCredentialsError(APIError):
    def __init__(self):
        super().__init__(
            "Invalid email or password", 401, ErrorCodes.INVALID_CREDENTIALS
        )


class TooManyAttemptsError(APIError):
    def __init__(self):
        super().__init__(
            "Too many login attempts. Try again later",
            429,
            ErrorCodes.TOO_MANY_ATTEMPTS,
        )


class MissingFieldsError(APIError):
    def __init__(self, fields=None):
        message = "Required fields are missing"
        if fields:
            message += f": {', '.join(fields)}"
        super().__init__(message, 400, ErrorCodes.MISSING_FIELDS)


class EmailExistsError(APIError):
    def __init__(self):
        super().__init__(
            "User with this email already exists", 409, ErrorCodes.EMAIL_EXISTS
        )


class AccountLockError(APIError):
    def __init__(self):
        super().__init__(
            "Your account has been locked. Please contact support",
            403,
            ErrorCodes.ACCOUNT_LOCKED,
        )


class UserNotFoundError(APIError):
    def __init__(self):
        super().__init__("User profile not found", 404, ErrorCodes.USER_NOT_FOUND)


# Token errors
class MissingTokenError(APIError):
    def __init__(self, token):
        super().__init__(
            f"Unauthorized: Authentication {token} is required",
            401,
            ErrorCodes.MISSING_TOKEN,
        )


class InvalidTokenError(APIError):
    def __init__(self, token):
        super().__init__(
            f"Unauthorized: Invalid authentication {token}",
            401,
            ErrorCodes.INVALID_TOKEN,
        )


class ExpiredTokenError(APIError):
    def __init__(self, token):
        super().__init__(
            f"Unauthorized: Authentication {token} has expired",
            401,
            ErrorCodes.EXPIRED_TOKEN,
        )


class TokenNotFoundError(APIError):
    def __init__(self):
        super().__init__(
            f"Unauthorized: Refresh token is not found",
            401,
            ErrorCodes.TOKEN_NOT_FOUND,
        )


class TokenRevokedError(APIError):
    def __init__(self):
        super().__init__(
            "Unauthorized: Refresh token has already been revoked",
            401,
            ErrorCodes.TOKEN_ALREADY_REVOKED,
        )


class TokenValidationError(APIError):
    def __init__(self, token):
        super().__init__(
            f"Invalid {token} format", 400, ErrorCodes.TOKEN_ALREADY_REVOKED
        )


# Permission errors
class PermissionsError(APIError):
    def __init__(self):
        super().__init__(
            f"You do not have permission to access this resource",
            403,
            ErrorCodes.INSUFFICIENT_PERMISSIONS,
        )


# Review errors
class ReviewTargetNotFoundError(APIError):
    def __init__(self, target_id):
        super().__init__(
            f"User with id {target_id} to review not found",
            404,
            ErrorCodes.REVIEW_TARGET_NOT_FOUND,
        )


class SelfReviewNotAllowedError(APIError):
    def __init__(self):
        super().__init__(
            f"You cannot submit a review for yourself",
            400,
            ErrorCodes.SELF_REVIEW_NOT_ALLOWED,
        )


# Server errors
class ServerError(APIError):
    def __init__(self, detail=None):
        message = "Internal server error."
        if detail:
            message = f"Internal server error: {detail}"
        super().__init__(message, 500, ErrorCodes.SERVER_ERROR)


class DatabaseError(APIError):
    def __init__(self, detail=None):
        message = "Error retrieving/saving data. Please try again later"
        if detail:
            message = f"Database error: {detail}"
        super().__init__(message, 500, ErrorCodes.DATABASE_ERROR)
