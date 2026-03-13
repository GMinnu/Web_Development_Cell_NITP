# ============================================================
# app.py — Main Entry Point for WDC Platform Backend
# This file starts the Flask server and registers all routes
# ============================================================

from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.extensions import db, jwt, limiter
from backend.routes.auth_routes import auth_bp
from backend.routes.profile_routes import profile_bp
from backend.routes.admin_routes import admin_bp

def create_app():
    """
    Application Factory Pattern:
    We use a function to create the app so it's easier to test
    and configure for different environments (dev, production).
    """
    app = Flask(__name__)

    # Load all settings from config.py
    app.config.from_object(Config)

    # -------------------------------------------------------
    # CORS = Cross-Origin Resource Sharing
    # This allows our Vue.js frontend (running on port 5173)
    # to talk to our Flask backend (running on port 5000)
    # supports_credentials=True is needed for HttpOnly cookies
    # -------------------------------------------------------
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Initialize all extensions with our app
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # -------------------------------------------------------
    # Register Blueprints (groups of related routes)
    # /api/auth    → signup, login, logout
    # /api/profile → view/update user profile
    # /api/admin   → admin panel (notices, events, news, faculty)
    # -------------------------------------------------------
    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(profile_bp,  url_prefix="/api/profile")
    app.register_blueprint(admin_bp,    url_prefix="/api/admin")

    # Create all database tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app


# Run the server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)



