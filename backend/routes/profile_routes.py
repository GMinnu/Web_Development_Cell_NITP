# ============================================================
# routes/profile_routes.py — User Profile CRUD Operations
#
# Endpoints:
#   GET    /api/profile/        → Get current user's profile
#   PUT    /api/profile/update  → Update name, bio, contact
#   DELETE /api/profile/delete  → Delete own account
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import User

profile_bp = Blueprint("profile", __name__)


# ============================================================
# GET PROFILE — GET /api/profile/
# Returns the logged-in user's profile details
# ============================================================
@profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200


# ============================================================
# UPDATE PROFILE — PUT /api/profile/update
# Allows user to update: name, bio, contact, department
# ============================================================
@profile_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # --- Only update fields that were actually sent ---
    # This way, if you only want to update name, you don't
    # have to send bio and contact too
    if "name" in data:
        name = data["name"].strip()
        if not name:
            return jsonify({"error": "Name cannot be empty"}), 400
        if len(name) > 100:
            return jsonify({"error": "Name too long (max 100 chars)"}), 400
        user.name = name

    if "bio" in data:
        user.bio = data["bio"].strip()[:500]  # Limit bio to 500 characters

    if "contact" in data:
        user.contact = data["contact"].strip()[:100]

    if "department" in data:
        user.department = data["department"].strip()[:100]

    # Save changes to database
    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully!",
        "user": user.to_dict()
    }), 200


# ============================================================
# DELETE ACCOUNT — DELETE /api/profile/delete
# Allows user to delete their own account
# ============================================================
@profile_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    # Clear the cookie after deletion
    from flask import make_response
    from flask_jwt_extended import unset_jwt_cookies
    response = make_response(jsonify({"message": "Account deleted"}))
    unset_jwt_cookies(response)
    return response, 200