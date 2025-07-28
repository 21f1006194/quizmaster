from app.models.quiz import Quiz
from app.models.chapter import Chapter
from app.models.subject import Subject
from app.models.question import Question
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User
from app import db
from sqlalchemy import func, desc
from datetime import datetime


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

    quiz.title = data.get("title", quiz.title)
    quiz.quiz_date = data.get("quiz_date", quiz.quiz_date)
    quiz.time_duration = data.get("time_duration", quiz.time_duration)
    quiz.remarks = data.get("remarks", quiz.remarks)

    if "chapter_id" in data:
        from app.models.chapter import Chapter

        chapter = Chapter.query.get(data["chapter_id"])
        if not chapter:
            raise ValueError("Invalid chapter ID")
        quiz.chapter_id = data["chapter_id"]

    db.session.commit()
    return quiz


def delete_quiz(quiz_id):

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return False

    db.session.delete(quiz)
    db.session.commit()
    return True


def get_all_quiz_summary():
    # Get all quizzes with their chapter and subject information
    quizzes = (
        db.session.query(Quiz, Chapter, Subject)
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .join(Subject, Chapter.subject_id == Subject.id)
        .all()
    )

    quiz_summaries = []

    for quiz, chapter, subject in quizzes:
        # Get question count and total marks for this quiz
        question_stats = (
            db.session.query(
                func.count(Question.id).label("total_questions"),
                func.sum(Question.max_marks).label("total_marks"),
            )
            .filter(Question.quiz_id == quiz.id)
            .first()
        )

        total_questions = question_stats.total_questions or 0
        total_marks = (
            float(question_stats.total_marks) if question_stats.total_marks else 0
        )
        # Get attempt statistics
        attempt_stats = (
            db.session.query(
                func.count(QuizAttempt.id).label("total_attempts"),
                func.max(QuizAttempt.score).label("max_score"),
                func.min(QuizAttempt.score).label("min_score"),
                func.avg(QuizAttempt.score).label("avg_score"),
            )
            .filter(
                QuizAttempt.quiz_id == quiz.id,
                QuizAttempt.in_progress == False,  # Only completed attempts
            )
            .first()
        )

        # Calculate average time spent in Python for better reliability
        attempts_with_times = (
            db.session.query(QuizAttempt.start_time, QuizAttempt.end_time)
            .filter(
                QuizAttempt.quiz_id == quiz.id,
                QuizAttempt.in_progress == False,
                QuizAttempt.end_time.isnot(None),
            )
            .all()
        )

        # Calculate average time spent in minutes
        total_time_minutes = 0
        valid_attempts = 0

        for start_time, end_time in attempts_with_times:
            if start_time and end_time:
                # Calculate time difference in seconds, then convert to minutes
                time_diff_seconds = (end_time - start_time).total_seconds()
                time_diff_minutes = time_diff_seconds / 60
                total_time_minutes += time_diff_minutes
                valid_attempts += 1

        avg_time_spent = (
            total_time_minutes / valid_attempts if valid_attempts > 0 else 0
        )
        # Validate score calculations
        max_score = float(attempt_stats.max_score) if attempt_stats.max_score else 0
        min_score = float(attempt_stats.min_score) if attempt_stats.min_score else 0
        avg_score = float(attempt_stats.avg_score) if attempt_stats.avg_score else 0

        # Get user with highest score
        top_performer = (
            db.session.query(User.id, User.full_name, QuizAttempt.score)
            .join(QuizAttempt, User.id == QuizAttempt.user_id)
            .filter(QuizAttempt.quiz_id == quiz.id, QuizAttempt.in_progress == False)
            .order_by(desc(QuizAttempt.score))
            .first()
        )
        # Build summary object
        summary = {
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "quiz_date": quiz.quiz_date.isoformat() if quiz.quiz_date else None,
            "quiz_time_duration": quiz.time_duration,
            "total_marks": total_marks,
            "subject_id": subject.id,
            "subject_name": subject.name,
            "quiz_chapter_id": chapter.id,
            "quiz_chapter_name": chapter.name,
            "total_questions": total_questions,
            "total_attempts": attempt_stats.total_attempts or 0,
            "Max_score": max_score,
            "Min_score": min_score,
            "Avg_score": avg_score,
            "Total_time_spent": total_time_minutes,
            "Avg_time_spent": avg_time_spent,
            "top_performer": (
                {
                    "user_id": top_performer.id,
                    "user_name": top_performer.full_name,
                    "score": float(top_performer.score),
                }
                if top_performer
                else None
            ),
        }

        quiz_summaries.append(summary)
    return quiz_summaries
