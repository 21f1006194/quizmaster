from datetime import datetime, timezone
from app import db
from app.models.quiz_attempt import QuizAttempt
from app.models.user_response import UserResponse
from app.services.catalog import get_questions_by_quiz


def create_quiz_attempt(user_id, quiz_id):
    # Check if user has any ongoing attempt for this quiz
    ongoing_attempt = QuizAttempt.query.filter_by(
        user_id=user_id, quiz_id=quiz_id, in_progress=True
    ).first()

    if ongoing_attempt:
        return (
            ongoing_attempt,
            False,
        )  # Return existing attempt and False to indicate no new attempt created

    try:
        quiz_attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            start_time=datetime.now(timezone.utc),
            in_progress=True,
        )
        db.session.add(quiz_attempt)
        db.session.commit()
        return (
            quiz_attempt,
            True,
        )  # Return new attempt and True to indicate new attempt created
    except Exception as e:
        db.session.rollback()
        if "unique_user_quiz_attempt" in str(e):
            raise ValueError("Quiz already submitted. Cannot create new attempt.")
        raise e


def get_active_attempt(user_id, quiz_id):
    return QuizAttempt.query.filter_by(
        user_id=user_id, quiz_id=quiz_id, in_progress=True
    ).first()


def get_user_responses(user_id, quiz_id):
    active_attempt = get_active_attempt(user_id, quiz_id)
    if not active_attempt:
        return None
    return UserResponse.query.filter_by(attempt_id=active_attempt.id).all()


def save_user_response(user_id, quiz_id, question_id, selected_option_id):
    try:
        # Get active attempt for this quiz
        attempt = get_active_attempt(user_id, quiz_id)
        if not attempt or not attempt.in_progress:
            raise ValueError("No active quiz attempt found")

        # Check if response exists and update, or create new
        user_response = UserResponse.query.filter_by(
            question_id=question_id, attempt_id=attempt.id
        ).first()

        # Delete response if selected_option_id is None
        if selected_option_id is None:
            if user_response:
                db.session.delete(user_response)
                db.session.commit()
                return None
        if user_response:
            user_response.option_id = selected_option_id  # Update the option_id
            user_response.is_attempted = True  # Mark as attempted
        elif selected_option_id is not None:
            user_response = UserResponse(
                attempt_id=attempt.id,
                question_id=question_id,
                option_id=selected_option_id,
                is_attempted=True,  # Mark as attempted
            )
            db.session.add(user_response)

        db.session.commit()
        return user_response
    except Exception as e:
        db.session.rollback()
        raise e


def close_quiz_attempt(user_id, quiz_id):
    try:
        attempt = get_active_attempt(user_id, quiz_id)
        if not attempt:
            raise ValueError("No active attempt found")

        attempt.in_progress = False
        score = 0
        for res in attempt.responses:
            if res.option.is_correct:
                score += res.question.max_marks
        attempt.score = score
        attempt.end_time = datetime.now(timezone.utc)
        db.session.commit()
        return attempt
    except Exception as e:
        db.session.rollback()
        raise e


def get_quiz_score(user_id, quiz_id):
    last_attempt = get_active_attempt(user_id, quiz_id)
    if not last_attempt:
        raise ValueError("No attempt found")
    return {
        "attempt_id": last_attempt.id,
        "user_id": last_attempt.user_id,
        "quiz_id": last_attempt.quiz_id,
        "start_time": last_attempt.start_time.isoformat(),
        "end_time": last_attempt.end_time.isoformat(),
        "score": last_attempt.score,
        "remarks": last_attempt.remarks,
    }


def get_full_quiz_result(user_id, quiz_id):
    last_attempt = (
        QuizAttempt.query.filter_by(user_id=user_id, quiz_id=quiz_id, in_progress=False)
        .order_by(QuizAttempt.end_time.desc())
        .first()
    )
    if not last_attempt:
        raise ValueError("No attempt found")
    responses = {}
    for res in last_attempt.responses:
        responses[res.question_id] = {
            "question_id": res.question_id,
            "selected_option_id": res.option_id,
            "is_correct": res.option.is_correct,
        }
    questions = []
    for q in get_questions_by_quiz(quiz_id):
        questions.append(
            {
                "question_id": q.id,
                "question": q.question,
                "max_marks": q.max_marks,
                "options": [
                    {
                        "option_id": opt.id,
                        "option_text": opt.option_text,
                        "is_correct": opt.is_correct,
                        "is_selected": (
                            False
                            if q.id not in responses
                            else (
                                True
                                if responses[q.id]["selected_option_id"] == opt.id
                                else False
                            )
                        ),
                    }
                    for opt in q.options
                ],
                "is_attempted": q.id in responses,
            }
        )

    result = {
        "attempt_id": last_attempt.id,
        "user_id": last_attempt.user_id,
        "quiz_id": last_attempt.quiz_id,
        "start_time": last_attempt.start_time.isoformat(),
        "end_time": last_attempt.end_time.isoformat(),
        "score": last_attempt.score,
        "remarks": last_attempt.remarks,
        "responses": questions,
    }
    return result
