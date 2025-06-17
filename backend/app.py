from flask import Flask
from flask_cors import CORS
from models import init_db
from auth.auth import auth_bp
from reviews.reviews import reviews_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize database
init_db()

# Register blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


