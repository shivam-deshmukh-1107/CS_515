# app.py

from flask import Flask
from routes import init_routes

app = Flask(__name__)

# Register all API endpoints from routes.py
init_routes(app)

if __name__ == '__main__':
    # Run the Flask application in debug mode.
    app.run(debug=True)
