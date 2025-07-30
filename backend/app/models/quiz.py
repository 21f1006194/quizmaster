from app import db
from datetime import datetime
from sqlalchemy.orm import validates
import os


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    quiz_date = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text)

    chapter = db.relationship("Chapter", back_populates="quizzes", lazy=True)
    questions = db.relationship("Question", backref="quiz", lazy=True)
    attempts = db.relationship("QuizAttempt", backref="quiz", lazy=True)

    @validates("quiz_date")
    def validate_quiz_date(self, key, quiz_date):
        is_demo = os.getenv("IS_DEMO")
        if not is_demo and quiz_date < datetime.now():
            raise ValueError("Quiz date should be in the future")
        return quiz_date

    @validates("time_duration")
    def validate_time_duration(self, key, time_duration):
        if time_duration <= 0:
            raise ValueError("Time duration should be greater than 0")
        return time_duration
