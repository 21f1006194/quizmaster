from app.models.quiz import Quiz
from app import db


def create_quiz(chapter_id, data):
    quiz = Quiz(
        title=data.get("title"),
        chapter_id=chapter_id,
        quiz_date=data.get("quiz_date"),
        time_duration=data.get("time_duration"),
        remarks=data.get("remarks"),
    )
    db.session.add(quiz)
    db.session.commit()
    return quiz


def update_quiz(quiz_id, data):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return None

    quiz.quiz_date = data.get("quiz_date", quiz.quiz_date)
    quiz.time_duration = data.get("time_duration", quiz.time_duration)
    quiz.remarks = data.get("remarks", quiz.remarks)
    db.session.commit()
    return quiz


def delete_quiz(quiz_id):

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return False

    db.session.delete(quiz)
    db.session.commit()
    return True
