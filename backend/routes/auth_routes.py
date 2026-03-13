# ============================================================
# routes/auth_routes.py — Authentication API Endpoints
#
# Endpoints:
#   POST /api/auth/signup  → Register a new user
#   POST /api/auth/login   → Login and get JWT cookie
#   POST /api/auth/logout  → Clear JWT cookie
#   GET  /api/auth/me      → Get logged-in user's details from token
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
import bcrypt        # For secure password hashing
import re            # For email validation using regex
from backend.extensions import db, limiter
from backend.models import User

# Blueprint groups related routes together
auth_bp = Blueprint("auth", __name__)


# ============================================================
# HELPER: Input Validation
# ============================================================
def validate_email(email):
    """Check if email looks valid using a simple regex pattern"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Password rules:
    - At least 8 characters long
    - Contains at least one number
    - Contains at least one letter
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, "OK"


# ============================================================
# SIGNUP — POST /api/auth/signup
# BONUS: Rate limited to 5 signups per minute per IP
# ============================================================
@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("5 per minute")   # BONUS: Rate limiting
def signup():
    data = request.get_json()

    # --- Step 1: Check all required fields are present ---
    required = ["name", "email", "password"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    name     = data["name"].strip()
    email    = data["email"].strip().lower()
    password = data["password"]
    role     = data.get("role", "faculty")  # Default role is "faculty"

    # --- Step 2: Validate email format ---
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # --- Step 3: Validate password strength ---
    is_valid, msg = validate_password(password)
    if not is_valid:
        return jsonify({"error": msg}), 400

    # --- Step 4: Check if email is already registered ---
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409  # 409 = Conflict

    # --- Step 5: Hash the password using bcrypt ---
    # bcrypt automatically adds a "salt" (random data) to the hash
    # so even if two users have the same password, the hashes differ
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # --- Step 6: Save user to database ---
    new_user = User(
        name     = name,
        email    = email,
        password = hashed.decode("utf-8"),  # Store as string in DB
        role     = role if role in ["faculty", "super_admin"] else "faculty"
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully!",
        "user": new_user.to_dict()
    }), 201  # 201 = Created


# ============================================================
# LOGIN — POST /api/auth/login
# BONUS: Rate limited to 10 attempts per minute per IP
# ============================================================
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")   # BONUS: Rate limiting prevents brute force
def login():
    data = request.get_json()

    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # --- Step 1: Basic validation ---
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # --- Step 2: Find user in database ---
    user = User.query.filter_by(email=email).first()
    if not user:
        # Use a vague error to not reveal if email exists
        return jsonify({"error": "Invalid email or password"}), 401

    # --- Step 3: Check password using bcrypt ---
    # bcrypt.checkpw compares plain password to stored hash
    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    )
    if not password_matches:
        return jsonify({"error": "Invalid email or password"}), 401

    # --- Step 4: Create JWT token ---
    # The token contains the user's ID as the "identity"
    # We can later decode it to find out who is logged in
    access_token = create_access_token(identity=str(user.id))

    # --- Step 5: Set token in HttpOnly Cookie (BONUS) ---
    response = jsonify({
        "message": "Login successful!",
        "user": user.to_dict()
    })
    # set_access_cookies puts the JWT in a secure HttpOnly cookie
    # JavaScript cannot read HttpOnly cookies — much safer than localStorage!
    set_access_cookies(response, access_token)

    return response, 200


# ============================================================
# LOGOUT — POST /api/auth/logout
# ============================================================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    # unset_jwt_cookies clears the JWT cookie from the browser
    unset_jwt_cookies(response)
    return response, 200


# ============================================================
# ME — GET /api/auth/me
# Decodes the JWT token and returns the user's details
# This proves we understand JWT decryption!
# ============================================================
@auth_bp.route("/me", methods=["GET"])
@jwt_required()  # This decorator checks the JWT cookie automatically
def get_me():
    # get_jwt_identity() reads the user ID from the decoded token
    user_id = get_jwt_identity()

    # Fetch full user details from database using the ID from token
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "Token decoded successfully",
        "user": user.to_dict()
    }), 200
