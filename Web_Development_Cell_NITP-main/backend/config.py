# ============================================================
# config.py — All App Settings in One Place
# Change these values to match your environment
# ============================================================

import os
from datetime import timedelta

class Config:
    # ----------------------------------------------------------
    # SECRET KEY — Used to sign JWT tokens. NEVER share this!
    # In production, set this as an environment variable.
    # ----------------------------------------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "wdc-super-secret-key-change-in-production")

    # ----------------------------------------------------------
    # DATABASE — MySQL connection string
    # Format: mysql+pymysql://username:password@host/database_name
    # Make sure you've created the database: CREATE DATABASE wdc_db;
    # ----------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:12345678@localhost/wdc_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable noisy warnings

    # ----------------------------------------------------------
    # JWT SETTINGS — JSON Web Token configuration
    # ----------------------------------------------------------
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "wdc-jwt-secret-change-this")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)   # Token valid for 2 hours
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token valid 30 days

    # ----------------------------------------------------------
    # BONUS: HttpOnly Cookie Settings
    # HttpOnly cookies can't be accessed by JavaScript, making
    # them safer against XSS (Cross-Site Scripting) attacks
    # ----------------------------------------------------------
    JWT_TOKEN_LOCATION = ["cookies"]          # Store JWT in cookies (not headers)
    JWT_COOKIE_SECURE = False                 # Set True in production (HTTPS only)
    JWT_COOKIE_HTTPONLY = True                # JavaScript CANNOT read this cookie ✓
    JWT_COOKIE_SAMESITE = "Lax"              # Protects against CSRF attacks
    JWT_COOKIE_CSRF_PROTECT = False          # Simplified for development

    # ----------------------------------------------------------
    # RATE LIMITING — Prevents brute force attacks
    # e.g. "5 per minute" means max 5 requests per minute per IP
    # ----------------------------------------------------------
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"  # Store limits in memory (use Redis in prod)
