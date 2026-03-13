# ============================================================
# models.py — Database Tables (defined as Python classes)
#
# SQLAlchemy lets us define tables as Python classes.
# Each class = one table. Each attribute = one column.
# ============================================================

from backend.extensions import db
from datetime import datetime


# ============================================================
# USER TABLE — Stores all registered users (faculty + admins)
# ============================================================
class User(db.Model):
    __tablename__ = "users"

    id          = db.Column(db.Integer, primary_key=True)           # Auto ID
    name        = db.Column(db.String(100), nullable=False)         # Full name
    email       = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password    = db.Column(db.String(255), nullable=False)         # Hashed password (NEVER plain text)
    bio         = db.Column(db.Text, default="")                    # Short bio
    contact     = db.Column(db.String(100), default="")             # Phone / contact info
    department  = db.Column(db.String(100), default="")             # Department name

    # Role: "faculty" can only edit own profile
    #        "super_admin" has full access to everything
    role        = db.Column(db.String(20), default="faculty")
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert user object to dictionary (for JSON responses)"""
        return {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "bio":        self.bio,
            "contact":    self.contact,
            "department": self.department,
            "role":       self.role,
            "created_at": self.created_at.isoformat()
        }
        # NOTE: We never include 'password' in responses!


# ============================================================
# NOTICE TABLE — Club notices/announcements
# ============================================================
class Notice(db.Model):
    __tablename__ = "notices"

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    # content stores HTML from the Rich Text Editor (TinyMCE)
    # We sanitize this on the backend before saving (BONUS)
    content    = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))  # Which admin posted it
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "title":      self.title,
            "content":    self.content,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat()
        }


# ============================================================
# EVENT TABLE — Club events
# ============================================================
class Event(db.Model):
    __tablename__ = "events"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    event_date  = db.Column(db.DateTime, nullable=False)
    location    = db.Column(db.String(200), default="")
    created_by  = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "event_date":  self.event_date.isoformat(),
            "location":    self.location,
            "created_by":  self.created_by,
            "created_at":  self.created_at.isoformat()
        }


# ============================================================
# NEWS TABLE — Club news articles
# ============================================================
class News(db.Model):
    __tablename__ = "news"

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    body       = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "title":      self.title,
            "body":       self.body,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat()
        }
