# ===============================
# Import required core libraries
# ===============================
from flask import Flask  # Core Flask framework to build the web application
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy extension for ORM/database integration
from flask_cors import CORS  # Enables Cross-Origin Resource Sharing for frontend/backend communication

# ===============================
# Create a Flask application instance
# ===============================
app = Flask(__name__)  # '__name__' tells Flask where to look for resources

# =========================================
# Enable CORS (Cross-Origin Resource Sharing)
# =========================================
# This allows external frontend apps (e.g., React, Next.js) running on different ports
# or domains to access your backend API without security restrictions.
CORS(app)

# =========================================
# Configuration settings for the database
# =========================================
# 'sqlite:///salon.db' means we're using a SQLite database named 'salon.db'
# located in the same folder as this script
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///salon.db"

# Disabling SQLALCHEMY_TRACK_MODIFICATIONS to save system resources
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ========================================
# Initialize the database using SQLAlchemy
# ========================================
db = SQLAlchemy(app)

# ============================
# Import database models first
# ============================
# This ensures all table schemas (Client, Stylist, etc.) are registered with SQLAlchemy.
from models import Client, Stylist, Service, Appointment, Invoice

# ========================================
# Import all API routes (MUST come after app/db setup)
# ========================================
# This line connects the endpoints defined in routes.py to the Flask application.
# All @app.route() decorators in routes.py will now be recognized and active.
from routes import *  # This imports and registers all routes defined in routes.py

# ============================
# Create all tables if needed
# ============================
# This will check the models and create any tables that don't exist yet
with app.app_context():
    db.create_all()
    
# =====================================================
# This is the main entry point — runs the Flask server
# =====================================================
if __name__ == "__main__":
    # Run the server in development mode with auto-reload and detailed errors
    app.run(debug=True)
