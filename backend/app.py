from flask import Flask
from models import init_db
from auth.auth import auth_bp

app = Flask(__name__)

# Initialize database
init_db()

# Register blueprint
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


