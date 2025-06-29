from app import db
from sqlalchemy.orm import validates


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    quizzes = db.relationship(
        "Quiz", backref="chapter", lazy=True, cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Chapter name cannot be empty")
        if len(name) > 255:
            raise ValueError("Chapter name cannot be longer than 255 characters")
        return name
