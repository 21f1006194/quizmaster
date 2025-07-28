from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.chapter import Chapter
from sqlalchemy.orm import joinedload


def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return quizzes


def get_quiz_by_id(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    return quiz


def get_all_quizzes():
    quizzes = Quiz.query.all()
    return quizzes


def get_leaderboard_by_quiz_id(quiz_id):
    """
    Get leaderboard data for a specific quiz including:
    - Quiz details with chapter and subject information
    - Latest attempts by each user (only completed attempts)
    """
    # Get quiz with chapter and subject information
    quiz = Quiz.query.options(joinedload(Quiz.chapter).joinedload(Chapter.subject)).get(
        quiz_id
    )

    if not quiz:
        return None

    # Get all completed attempts for the quiz (in_progress=False)
    completed_attempts = (
        QuizAttempt.query.filter_by(quiz_id=quiz_id, in_progress=False)
        .options(joinedload(QuizAttempt.user))
        .all()
    )

    # Group attempts by user and get the latest one for each user
    user_latest_attempts = {}
    for attempt in completed_attempts:
        user_id = attempt.user_id
        if (
            user_id not in user_latest_attempts
            or attempt.end_time > user_latest_attempts[user_id].end_time
        ):
            user_latest_attempts[user_id] = attempt

    # Convert to list and sort by score (descending) and end_time (ascending for same scores)
    leaderboard_attempts = sorted(
        user_latest_attempts.values(), key=lambda x: (-x.score, x.end_time)
    )

    # Prepare quiz information
    quiz_info = {
        "id": quiz.id,
        "title": quiz.title,
        "quiz_date": quiz.quiz_date.isoformat(),
        "time_duration": quiz.time_duration,
        "remarks": quiz.remarks,
        "chapter_name": quiz.chapter.name,
        "subject_name": quiz.chapter.subject.name,
    }

    # Prepare leaderboard data
    leaderboard_data = []
    for rank, attempt in enumerate(leaderboard_attempts, 1):
        leaderboard_data.append(
            {
                "rank": rank,
                "user_id": attempt.user.id,
                "username": attempt.user.username,
                "full_name": attempt.user.full_name,
                "score": attempt.score,
                "start_time": attempt.start_time.isoformat(),
                "end_time": attempt.end_time.isoformat(),
                "remarks": attempt.remarks,
            }
        )

    return {
        "quiz": quiz_info,
        "leaderboard": leaderboard_data,
        "total_participants": len(leaderboard_data),
    }
