from flask import Flask
from models import init_db

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    return "Привет, Flask!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
