from flask import Flask, jsonify
from flask_cors import CORS
from errors.api_errors import APIError
from models.models import init_db
from routes.auth import auth_bp
from routes.reviews import reviews_bp
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

# Initialize database
init_db()

# Register blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)


# Custom error handling
@app.errorhandler(APIError)
def handle_api_error(error):
    return error.to_response()


# Standard HTTP error handling
@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = jsonify({"error": {"code": error.code, "message": error.description}})
    response.status_code = error.code
    return response


# Unhandled errors
@app.errorhandler(Exception)
def handle_generic_exception(error):
    app.logger.error(f"Unhandled exception: {str(error)}")

    response = jsonify(
        {
            "error": {
                "code": 5001,
                "message": "Error processing request. Please try again later",
            }
        }
    )
    response.status_code = 500
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
