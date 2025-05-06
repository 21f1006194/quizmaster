from app import db


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    quiz_date = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text)

    questions = db.relationship("Question", backref="quiz", lazy=True)
    attempts = db.relationship("QuizAttempt", backref="quiz", lazy=True)
