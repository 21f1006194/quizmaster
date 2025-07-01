from app import db
from datetime import datetime


class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    start_time = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc)
    )
    end_time = db.Column(db.DateTime)
    in_progress = db.Column(
        db.Boolean, nullable=False, default=True
    )  # True when active, False when completed
    score = db.Column(db.Float, nullable=False, default=0)
    remarks = db.Column(db.Text)

    responses = db.relationship("UserResponse", backref="attempt", lazy=True)

    __table_args__ = (
        db.UniqueConstraint("user_id", "quiz_id", name="unique_user_quiz_attempt"),
    )
