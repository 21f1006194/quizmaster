from datetime import datetime, timedelta, timezone
from app.celery_app import celery_app
from app import db
from app.models import User, QuizAttempt, Quiz
from app.utils.mail import send_email


@celery_app.task(bind=True, name="app.tasks.periodic.send_daily_reminders")
def send_daily_reminders(self):

    try:
        print("Starting daily reminders task")

        active_users = User.query.filter_by(is_blocked=False, is_admin=False).all()
        print(f"Found {len(active_users)} active users")
        today = datetime.now(timezone.utc)
        # quiz date > today 00:00:00 and quiz date < today 23:59:59
        today_quizzes = Quiz.query.filter(
            Quiz.quiz_date >= today.replace(hour=0, minute=0, second=0),
            Quiz.quiz_date <= today.replace(hour=23, minute=59, second=59),
        ).all()
        print(f"Found {len(today_quizzes)} today's quizzes")
        quiz_txt = f"Here are the quizzes for today {today.strftime('%Y-%m-%d')}\n\n"
        if len(today_quizzes) == 0:
            print("No quizzes today")
            return {
                "status": "success",
                "users_checked": len(active_users),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            }
        else:
            for quiz in today_quizzes:
                quiz_txt += f"Title: {quiz.title}\nChapter: {quiz.chapter.name}\nTime Duration: {quiz.time_duration} mins\nQuiz Date: {quiz.quiz_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        print(f"Quiz text: {quiz_txt}")
        for user in active_users:
            print(f"Sending reminder to user {user.username}")
            send_email(
                f"Today's Quizzes - {today.strftime('%Y-%m-%d')}",
                [user.email],
                f"Dear {user.username},\n\n{quiz_txt}",
            )
        return {
            "status": "success",
            "users_checked": len(active_users),
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        print(f"Daily reminders task failed: {str(exc)}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@celery_app.task(bind=True, name="app.tasks.periodic.generate_monthly_reports")
def generate_monthly_reports(self):

    try:
        print("Starting monthly reports generation")

        # Calculate date range for last month
        today = datetime.now(timezone.utc)
        last_month_first_day = today.replace(day=1)

        active_users = User.query.filter_by(is_blocked=False, is_admin=False).all()
        print(f"Found {len(active_users)} active users")
        # TODO: Generate reports for active users - All Quiz Attempts and scores for each user
        for user in active_users:
            quiz_attempts = QuizAttempt.query.filter(
                QuizAttempt.user_id == user.id,
                QuizAttempt.start_time >= last_month_first_day,
                QuizAttempt.start_time <= today,
            ).all()
            print(f"Found {len(quiz_attempts)} quiz attempts for user {user.username}")
            quiz_attempts_txt = f"Dear {user.username},\n\n"
            quiz_attempts_txt += f"Here is your monthly report for the period {today.strftime('%Y-%m-%d')} - {last_month_first_day.strftime('%Y-%m-%d')}\n\n"
            if len(quiz_attempts) == 0:
                quiz_attempts_txt += "No quiz attempts found for the period\n"
            else:
                quiz_attempts_txt += f"Total Quiz Attempts: {len(quiz_attempts)}\n"
                quiz_attempts_txt += f"Total Score: {sum(quiz_attempt.score for quiz_attempt in quiz_attempts)}\n"
                # quiz_attempts_txt += f"Average Score: {sum(quiz_attempt.score for quiz_attempt in quiz_attempts) / len(quiz_attempts):.2f}\n"
                # quiz_attempts_txt += f"Highest Score: {max(quiz_attempt.score for quiz_attempt in quiz_attempts)}\n\n"
                quiz_attempts_txt += "\n\n"
                for quiz_attempt in quiz_attempts:
                    quiz_attempts_txt += f"Quiz Title: {quiz_attempt.quiz.title}\nQuiz Date: {quiz_attempt.start_time.strftime('%Y-%m-%d %H:%M:%S')}\nScore: {quiz_attempt.score}\n\n"
            print(f"Quiz attempts text: {quiz_attempts_txt}")
            send_email(
                f"Monthly Report - {today.strftime('%Y-%m-%d')} - {last_month_first_day.strftime('%Y-%m-%d')}",
                [user.email],
                f"{quiz_attempts_txt}",
            )

        return {
            "status": "success",
            "users_checked": len(active_users),
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as exc:
        import traceback

        traceback.print_exc()
        print(f"Monthly reports task failed: {str(exc)}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=300, max_retries=2)
