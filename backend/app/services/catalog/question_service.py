from app.models.question import Question


def get_questions_by_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return questions


def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    return question
