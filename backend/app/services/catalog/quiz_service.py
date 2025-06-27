from app.models.quiz import Quiz


def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return quizzes


def get_quiz_by_id(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    return quiz
