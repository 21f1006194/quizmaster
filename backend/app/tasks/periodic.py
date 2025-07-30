from datetime import datetime, timedelta, timezone
from app.celery_app import celery_app
from app import db
from app.models import User, QuizAttempt, Quiz
from app.utils.mail import send_email, create_email_template


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

        if len(today_quizzes) == 0:
            print("No quizzes today")
            return {
                "status": "success",
                "users_checked": len(active_users),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            }

        # Create HTML content for today's quizzes
        for user in active_users:
            print(f"Sending reminder to user {user.username}")

            # Create HTML content
            greeting = (
                f'<div class="greeting">Dear <strong>{user.username}</strong>,</div>'
            )
            intro = f'<p>Here are the quizzes scheduled for today, <strong>{today.strftime("%B %d, %Y")}</strong>:</p>'

            # Create quiz table
            quiz_table = """
            <table class="quiz-table">
                <thead>
                    <tr>
                        <th>📚 Quiz Title</th>
                        <th>📖 Chapter</th>
                        <th>⏱️ Duration</th>
                        <th>🕐 Time</th>
                    </tr>
                </thead>
                <tbody>
            """

            for quiz in today_quizzes:
                quiz_table += f"""
                    <tr>
                        <td><strong>{quiz.title}</strong></td>
                        <td>{quiz.chapter.name}</td>
                        <td>{quiz.time_duration} minutes</td>
                        <td>{quiz.quiz_date.strftime('%H:%M')}</td>
                    </tr>
                """

            quiz_table += "</tbody></table>"

            # Add summary stats
            stats_section = f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-number">{len(today_quizzes)}</div>
                    <div class="stat-label">QUIZZES TODAY</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{sum(q.time_duration for q in today_quizzes)}</div>
                    <div class="stat-label">TOTAL MINUTES</div>
                </div>
            </div>
            """

            closing = "<p>Good luck with your quizzes! 🎯</p>"

            html_content = greeting + intro + quiz_table + stats_section + closing

            # Create plain text fallback
            text_content = f"Dear {user.username},\n\nHere are the quizzes for today {today.strftime('%Y-%m-%d')}\n\n"
            for quiz in today_quizzes:
                text_content += f"Title: {quiz.title}\nChapter: {quiz.chapter.name}\nTime Duration: {quiz.time_duration} mins\nQuiz Date: {quiz.quiz_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            # Generate HTML email
            html_body = create_email_template(
                title=f"Today's Quizzes - {today.strftime('%B %d, %Y')}",
                content=html_content,
                footer_text="This is an automated reminder from Quiz Master. Stay focused and do your best! 📚✨",
            )

            send_email(
                f"📚 Today's Quizzes - {today.strftime('%B %d, %Y')}",
                [user.email],
                text_content,
                html_body,
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

        for user in active_users:
            quiz_attempts = QuizAttempt.query.filter(
                QuizAttempt.user_id == user.id,
                QuizAttempt.start_time >= last_month_first_day,
                QuizAttempt.start_time <= today,
            ).all()
            print(f"Found {len(quiz_attempts)} quiz attempts for user {user.username}")

            # Create HTML content
            greeting = (
                f'<div class="greeting">Dear <strong>{user.username}</strong>,</div>'
            )
            period = f"<p>Here is your monthly performance report for the period <strong>{last_month_first_day.strftime('%B %d, %Y')}</strong> to <strong>{today.strftime('%B %d, %Y')}</strong>:</p>"

            if len(quiz_attempts) == 0:
                no_attempts = "<div class=\"no-content\">📊 No quiz attempts found for this period.<br/>Don't worry, there's always next month to shine! ⭐</div>"
                html_content = greeting + period + no_attempts
                text_content = f"Dear {user.username},\n\nHere is your monthly report for the period {today.strftime('%Y-%m-%d')} - {last_month_first_day.strftime('%Y-%m-%d')}\n\nNo quiz attempts found for the period\n"
            else:
                # Calculate statistics
                total_score = sum(quiz_attempt.score for quiz_attempt in quiz_attempts)
                avg_score = total_score / len(quiz_attempts)
                max_score = max(quiz_attempt.score for quiz_attempt in quiz_attempts)

                # Statistics section
                stats_section = f"""
                <div class="stats-container">
                    <div class="stat-box">
                        <div class="stat-number">{len(quiz_attempts)}</div>
                        <div class="stat-label">TOTAL ATTEMPTS</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{total_score:.1f}</div>
                        <div class="stat-label">TOTAL SCORE</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{avg_score:.1f}</div>
                        <div class="stat-label">AVERAGE SCORE</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{max_score:.1f}</div>
                        <div class="stat-label">HIGHEST SCORE</div>
                    </div>
                </div>
                """

                # Quiz attempts table
                attempts_table = """
                <h3>📋 Quiz Attempt Details</h3>
                <table class="quiz-table">
                    <thead>
                        <tr>
                            <th>📚 Quiz Title</th>
                            <th>📅 Date</th>
                            <th>⏰ Time</th>
                            <th>🎯 Score</th>
                        </tr>
                    </thead>
                    <tbody>
                """

                for quiz_attempt in quiz_attempts:
                    attempts_table += f"""
                        <tr>
                            <td><strong>{quiz_attempt.quiz.title}</strong></td>
                            <td>{quiz_attempt.start_time.strftime('%B %d, %Y')}</td>
                            <td>{quiz_attempt.start_time.strftime('%H:%M')}</td>
                            <td><strong>{quiz_attempt.score:.1f}</strong></td>
                        </tr>
                    """

                attempts_table += "</tbody></table>"

                encouragement = "<p>Keep up the great work! Your dedication to learning is truly commendable. 🌟</p>"

                html_content = (
                    greeting + period + stats_section + attempts_table + encouragement
                )

                # Plain text fallback
                text_content = f"Dear {user.username},\n\nHere is your monthly report for the period {today.strftime('%Y-%m-%d')} - {last_month_first_day.strftime('%Y-%m-%d')}\n\n"
                text_content += f"Total Quiz Attempts: {len(quiz_attempts)}\n"
                text_content += f"Total Score: {total_score:.1f}\n"
                text_content += f"Average Score: {avg_score:.1f}\n"
                text_content += f"Highest Score: {max_score:.1f}\n\n"
                for quiz_attempt in quiz_attempts:
                    text_content += f"Quiz Title: {quiz_attempt.quiz.title}\nQuiz Date: {quiz_attempt.start_time.strftime('%Y-%m-%d %H:%M:%S')}\nScore: {quiz_attempt.score:.1f}\n\n"

            # Generate HTML email
            html_body = create_email_template(
                title=f"Monthly Performance Report - {last_month_first_day.strftime('%B %Y')}",
                content=html_content,
                footer_text="This is your automated monthly report from Quiz Master. Keep learning and growing! 🚀📈",
            )

            send_email(
                f"📊 Monthly Report - {last_month_first_day.strftime('%B %Y')}",
                [user.email],
                text_content,
                html_body,
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
