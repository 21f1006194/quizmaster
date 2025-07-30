from app.models.question import Question
from app.models.option import Option
from app import db, cache
from app.services.catalog.question_service import get_questions_by_quiz


def create_question(quiz_id, data):
    question = Question(
        quiz_id=quiz_id,
        question=data.get("question"),
        max_marks=data.get("max_marks", 1.0),
    )
    db.session.add(question)
    db.session.flush()  # Flush to generate an ID for the question before adding options

    options_data = data.get("options", [])
    for opt in options_data:
        option = Option(
            question_id=question.id,
            option_text=opt.get("option_text"),
            is_correct=opt.get("is_correct", False),
        )
        db.session.add(option)

    db.session.commit()
    cache.delete_memoized(get_questions_by_quiz, quiz_id)
    return question


def update_question(question_id, data):
    question = Question.query.get(question_id)
    quiz_id = question.quiz_id
    if not question:
        return None

    # Update question fields
    question.question = data.get("question", question.question)
    question.max_marks = data.get("max_marks", question.max_marks)

    # If options are provided, replace the existing options
    if "options" in data:
        # Delete existing options
        for option in question.options:
            db.session.delete(option)
        db.session.flush()
        # Add new options
        for opt in data["options"]:
            new_option = Option(
                question_id=question.id,
                option_text=opt.get("option_text"),
                is_correct=opt.get("is_correct", False),
            )
            db.session.add(new_option)

    db.session.commit()
    cache.delete_memoized(get_questions_by_quiz, quiz_id)
    return question


def delete_question(question_id):

    question = Question.query.get(question_id)
    quiz_id = question.quiz_id
    if not question:
        return False

    # Delete associated options
    for option in question.options:
        db.session.delete(option)

    db.session.delete(question)
    db.session.commit()
    cache.delete_memoized(get_questions_by_quiz, quiz_id)
    return True
