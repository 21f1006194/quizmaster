from app import db
from sqlalchemy.orm import validates


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    max_marks = db.Column(db.Float, nullable=False, default=1.0)

    options = db.relationship("Option", backref="question", lazy=True)
    responses = db.relationship("UserResponse", backref="question", lazy=True)

    @validates("max_marks")
    def validate_max_marks(self, key, max_marks):
        if max_marks <= 0:
            raise ValueError("Marks should be greater than 0")
        return max_marks

    @validates("question")
    def validate_question(question):
        if not question.strip():
            raise ValueError("Question cannot be empty")
        return question
