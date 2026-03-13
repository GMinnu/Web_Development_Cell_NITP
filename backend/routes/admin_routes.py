# ============================================================
# routes/admin_routes.py — Admin Panel with Role-Based Access
#
# ROLES:
#   faculty     → Can only view/edit their own profile
#   super_admin → Full access to all modules
#
# Endpoints:
#   Faculty Management: GET/POST/PUT/DELETE /api/admin/faculty
#   Notices:  GET/POST/PUT/DELETE /api/admin/notices
#   Events:   GET/POST/PUT/DELETE /api/admin/events
#   News:     GET/POST/PUT/DELETE /api/admin/news
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import bleach   # BONUS: XSS sanitization library
from backend.extensions import db
from backend.models import User, Notice, Event, News
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


# ============================================================
# HELPER: Role Checker — Reusable security function
# ============================================================
def require_super_admin(user_id):
    """
    Returns (user, error_response) tuple.
    If user is NOT super_admin, returns an error.
    Usage: user, err = require_super_admin(user_id)
           if err: return err
    """
    user = User.query.get(int(user_id))
    if not user:
        return None, (jsonify({"error": "User not found"}), 404)
    if user.role != "super_admin":
        return None, (jsonify({"error": "Access denied. Super Admin only."}), 403)
    return user, None


# ============================================================
# BONUS: XSS Sanitization using bleach
# Strips dangerous HTML tags from Rich Text Editor content.
# e.g. <script>steal_cookies()</script> gets removed
# ============================================================
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "u", "h1", "h2", "h3",
    "ul", "ol", "li", "a", "blockquote", "img", "span", "div"
]
ALLOWED_ATTRS = {
    "a":   ["href", "title", "target"],
    "img": ["src", "alt", "width", "height"],
    "*":   ["class", "style"]
}

def sanitize_html(raw_html):
    """Remove any dangerous HTML to prevent XSS attacks"""
    return bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)


# ============================================================
# =================== FACULTY MANAGEMENT ====================
# ============================================================

@admin_bp.route("/faculty", methods=["GET"])
@jwt_required()
def get_all_faculty():
    """Super Admin: Get list of all faculty members"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    faculty = User.query.filter_by(role="faculty").all()
    return jsonify({"faculty": [f.to_dict() for f in faculty]}), 200


@admin_bp.route("/faculty/<int:faculty_id>", methods=["PUT"])
@jwt_required()
def update_faculty(faculty_id):
    """
    Update a faculty member's profile.
    - Super Admin can update ANY faculty profile
    - Faculty can only update THEIR OWN profile
    """
    user_id = get_jwt_identity()
    current_user = User.query.get(int(user_id))

    if not current_user:
        return jsonify({"error": "Not authenticated"}), 401

    # Check permission: faculty can only edit themselves
    if current_user.role == "faculty" and current_user.id != faculty_id:
        return jsonify({"error": "You can only edit your own profile"}), 403

    faculty = User.query.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    data = request.get_json()
    if "name"       in data: faculty.name       = data["name"].strip()
    if "bio"        in data: faculty.bio        = data["bio"].strip()
    if "contact"    in data: faculty.contact    = data["contact"].strip()
    if "department" in data: faculty.department = data["department"].strip()

    db.session.commit()
    return jsonify({"message": "Faculty updated", "faculty": faculty.to_dict()}), 200


@admin_bp.route("/faculty/<int:faculty_id>", methods=["DELETE"])
@jwt_required()
def delete_faculty(faculty_id):
    """Super Admin: Remove a faculty member"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    faculty = User.query.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    db.session.delete(faculty)
    db.session.commit()
    return jsonify({"message": "Faculty deleted"}), 200


# ============================================================
# ======================= NOTICES ===========================
# ============================================================

@admin_bp.route("/notices", methods=["GET"])
def get_notices():
    """Public: Anyone can read notices"""
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return jsonify({"notices": [n.to_dict() for n in notices]}), 200


@admin_bp.route("/notices", methods=["POST"])
@jwt_required()
def create_notice():
    """Super Admin: Create a new notice"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    data = request.get_json()
    title   = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    # BONUS: Sanitize HTML content from Rich Text Editor
    safe_content = sanitize_html(content)

    notice = Notice(title=title, content=safe_content, created_by=int(user_id))
    db.session.add(notice)
    db.session.commit()

    return jsonify({"message": "Notice created!", "notice": notice.to_dict()}), 201


@admin_bp.route("/notices/<int:notice_id>", methods=["PUT"])
@jwt_required()
def update_notice(notice_id):
    """Super Admin: Edit an existing notice"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404

    data = request.get_json()
    if "title"   in data: notice.title   = data["title"].strip()
    if "content" in data: notice.content = sanitize_html(data["content"])  # Sanitize on update too!

    db.session.commit()
    return jsonify({"message": "Notice updated", "notice": notice.to_dict()}), 200


@admin_bp.route("/notices/<int:notice_id>", methods=["DELETE"])
@jwt_required()
def delete_notice(notice_id):
    """Super Admin: Delete a notice"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404

    db.session.delete(notice)
    db.session.commit()
    return jsonify({"message": "Notice deleted"}), 200


# ============================================================
# ======================== EVENTS ===========================
# ============================================================

@admin_bp.route("/events", methods=["GET"])
def get_events():
    """Public: Anyone can view events"""
    events = Event.query.order_by(Event.event_date.asc()).all()
    return jsonify({"events": [e.to_dict() for e in events]}), 200


@admin_bp.route("/events", methods=["POST"])
@jwt_required()
def create_event():
    """Super Admin: Create a new event"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    data = request.get_json()
    title      = data.get("title", "").strip()
    event_date = data.get("event_date")

    if not title or not event_date:
        return jsonify({"error": "Title and event_date are required"}), 400

    try:
        parsed_date = datetime.fromisoformat(event_date)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format: 2025-01-15T10:00:00"}), 400

    event = Event(
        title       = title,
        description = data.get("description", ""),
        event_date  = parsed_date,
        location    = data.get("location", ""),
        created_by  = int(user_id)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event created!", "event": event.to_dict()}), 201


@admin_bp.route("/events/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    """Super Admin: Edit an event"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if "title"       in data: event.title       = data["title"].strip()
    if "description" in data: event.description = data["description"]
    if "location"    in data: event.location    = data["location"]
    if "event_date"  in data:
        try:
            event.event_date = datetime.fromisoformat(data["event_date"])
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    db.session.commit()
    return jsonify({"message": "Event updated", "event": event.to_dict()}), 200


@admin_bp.route("/events/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    """Super Admin: Delete an event"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200


# ============================================================
# ========================= NEWS ============================
# ============================================================

@admin_bp.route("/news", methods=["GET"])
def get_news():
    """Public: Anyone can read news"""
    news = News.query.order_by(News.created_at.desc()).all()
    return jsonify({"news": [n.to_dict() for n in news]}), 200


@admin_bp.route("/news", methods=["POST"])
@jwt_required()
def create_news():
    """Super Admin: Post a news article"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    data  = request.get_json()
    title = data.get("title", "").strip()
    body  = data.get("body", "").strip()

    if not title or not body:
        return jsonify({"error": "Title and body are required"}), 400

    news = News(title=title, body=body, created_by=int(user_id))
    db.session.add(news)
    db.session.commit()
    return jsonify({"message": "News posted!", "news": news.to_dict()}), 201


@admin_bp.route("/news/<int:news_id>", methods=["PUT"])
@jwt_required()
def update_news(news_id):
    """Super Admin: Edit a news article"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    news = News.query.get(news_id)
    if not news:
        return jsonify({"error": "News not found"}), 404

    data = request.get_json()
    if "title" in data: news.title = data["title"].strip()
    if "body"  in data: news.body  = data["body"]

    db.session.commit()
    return jsonify({"message": "News updated", "news": news.to_dict()}), 200


@admin_bp.route("/news/<int:news_id>", methods=["DELETE"])
@jwt_required()
def delete_news(news_id):
    """Super Admin: Delete a news article"""
    user_id = get_jwt_identity()
    _, err = require_super_admin(user_id)
    if err: return err

    news = News.query.get(news_id)
    if not news:
        return jsonify({"error": "News not found"}), 404

    db.session.delete(news)
    db.session.commit()
    return jsonify({"message": "News deleted"}), 200
