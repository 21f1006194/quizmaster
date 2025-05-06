from app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=1)
