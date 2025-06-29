from app import db
from sqlalchemy.orm import validates


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    @validates("option_text")
    def validate_option_text(self, key, option_text):
        if not option_text.strip():
            raise ValueError("Option text cannot be empty")
        return option_text
