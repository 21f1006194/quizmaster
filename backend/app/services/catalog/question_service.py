from app.models.question import Question
from app import cache


@cache.memoize(timeout=3600)
def get_questions_by_quiz(quiz_id):
    print(f"Getting questions by quiz : {quiz_id}")
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return questions


def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    return question
