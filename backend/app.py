from flask import Flask
from models import init_db

# Initialize the Flask application
app = Flask(__name__)

# Initialize the database (this function sets up the database connection and tables)
init_db()

# Import routes after initializing the app to avoid circular imports
import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)