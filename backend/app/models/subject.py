from app import db
from sqlalchemy.orm import validates


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)

    chapters = db.relationship("Chapter", backref="subject", lazy=True)

    @validates("name")
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Subject name cannot be empty")
        if len(name) > 255:
            raise ValueError("Subject name cannot be longer than 255 characters")
        return name
