# Import the necessary modules from Flask
from flask import Flask  # Core Flask framework to build the web application
from flask_sqlalchemy import SQLAlchemy  # Extension to work with databases using Python classes
from flask_cors import CORS  # Allows the API to be accessed from different origins (e.g., frontend on another port)

# Create a Flask application instance
app = Flask(__name__)  # '__name__' lets Flask know where to find static files and templates

# Enable CORS (Cross-Origin Resource Sharing) for the entire app
CORS(app)  # This allows your frontend (e.g., React, Next.js) to make requests to this Flask backend

# ================================
# Configuration for the database
# ================================

# Set the URI (Uniform Resource Identifier) for the database
# 'sqlite:///clients.db' means we are using a SQLite database named 'salon.db' in the same directory
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///salon.db"

# Disable the event notification system of SQLAlchemy to save memory
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create a SQLAlchemy database instance linked to the Flask app
db = SQLAlchemy(app)

# =======================================
# This is the main entry point of the app
# =======================================

# If this script is run directly (not imported as a module), start the Flask development server
if __name__ == "__main__":
    # Run the app in debug mode (shows helpful error messages and reloads on code changes)
    app.run(debug=True)
