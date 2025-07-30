import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # or `from app import app` if not using factory
from app import db  # your SQLAlchemy or DB instance
from app.services.admin import (
    create_subject,
    create_chapter,
    create_quiz,
    create_question,
)
from app.models.user import User
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.option import Option
from app.models.quiz_attempt import QuizAttempt
from app.models.user_response import UserResponse
from datetime import datetime, timedelta
import json
import random

# Load the seed data from the correct path
script_dir = os.path.dirname(os.path.abspath(__file__))
seed_data_path = os.path.join(script_dir, "seed_data.json")
dummy_data = json.load(open(seed_data_path))
os.environ["IS_DEMO"] = "true"


def seed_data():
    print("Starting to seed data...")

    for subject in dummy_data:
        print(f"Creating subject: {subject['name']}")
        sub = create_subject(subject)

        for chapter in subject["chapters"]:
            print(f"  Creating chapter: {chapter['name']}")
            chap = create_chapter(sub.id, chapter)

            # Handle quizzes in the chapter
            for quiz_data in chapter.get("quiz", []):
                print(f"    Creating quiz: {quiz_data['quiz_title']}")

                # Convert quiz_date string to datetime object
                quiz_date_obj = datetime.now() + timedelta(
                    days=quiz_data.get("quiz_date")
                )
                if quiz_data.get("quiz_date") == 0:
                    quiz_date_obj = datetime.now() - timedelta(
                        minutes=quiz_data.get("duration") // 2
                    )

                # Map the JSON fields to the expected service fields
                quiz_service_data = {
                    "title": quiz_data.get("quiz_title"),
                    "quiz_date": quiz_date_obj,
                    "time_duration": quiz_data.get("duration"),
                    "remarks": quiz_data.get("remarks"),
                }

                quiz = create_quiz(chap.id, quiz_service_data)

                # Handle questions in the quiz
                for question_data in quiz_data.get("questions", []):
                    print(
                        f"      Creating question with {len(question_data.get('options', []))} options"
                    )
                    create_question(quiz.id, question_data)

    print("Data seeding completed!")


def create_demo_user(name, random_seed):
    username = name.lower().replace(" ", "_")
    full_name = name.capitalize()
    email = f"{username}@demo.com"
    password = f"{username.capitalize().strip()}12345"
    print("Creating demo user...")
    user = User(
        username=username,
        password=password,
        email=email,
        full_name=full_name,
        qualification="B.Tech",
        date_of_birth=datetime.now() - timedelta(days=365 * (10 + random_seed)),
        is_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    print("Demo user created!")
    return user


def get_eligible_quizzes():
    """Get all quizzes that have quiz_date < now"""
    now = datetime.now()
    eligible_quizzes = Quiz.query.filter(Quiz.quiz_date < now).all()
    print(f"Found {len(eligible_quizzes)} eligible quizzes for demo attempts")
    return eligible_quizzes


def get_quiz_questions_and_options(quiz_id):
    """Get all questions and their options for a given quiz"""
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_options = {}

    for question in questions:
        options = Option.query.filter_by(question_id=question.id).all()
        question_options[question.id] = {"question": question, "options": options}

    return question_options


def generate_random_responses(question_options, answer_accuracy):
    """
    Generate random responses for questions
    answer_accuracy: probability of selecting correct answer
    """
    responses = {}

    for question_id, data in question_options.items():
        options = data["options"]
        if not options:
            continue

        # Find correct option
        correct_options = [opt for opt in options if opt.is_correct]
        incorrect_options = [opt for opt in options if not opt.is_correct]

        # Randomly decide if this question should be answered correctly
        if correct_options and random.random() < answer_accuracy:
            # Select a correct answer
            selected_option = random.choice(correct_options)
        else:
            # Select an incorrect answer or any available option
            available_options = incorrect_options if incorrect_options else options
            selected_option = random.choice(available_options)

        responses[question_id] = selected_option.id

    return responses


def calculate_attempt_score(question_options, user_responses):
    """Calculate the score for an attempt based on correct answers"""
    total_marks = 0
    earned_marks = 0

    for question_id, data in question_options.items():
        question = data["question"]
        total_marks += question.max_marks

        if question_id in user_responses:
            option_id = user_responses[question_id]
            option = Option.query.get(option_id)
            if option and option.is_correct:
                earned_marks += question.max_marks

    return earned_marks if total_marks > 0 else 0


def create_demo_attempt(user_id, quiz, question_options, answer_accuracy):
    """Create a demo quiz attempt for a user"""
    try:
        # Check if attempt already exists (due to unique constraint)
        existing_attempt = QuizAttempt.query.filter_by(
            user_id=user_id, quiz_id=quiz.id
        ).first()

        if existing_attempt:
            print(f"  Attempt already exists for user {user_id} and quiz {quiz.id}")
            return existing_attempt

        # Generate random start time: quiz_date + random(1-300) seconds
        start_offset_seconds = random.randint(1, 300)
        start_time = quiz.quiz_date + timedelta(seconds=start_offset_seconds)

        # Generate random end time: start_time + (time_duration - random_reduction) minutes
        # Ensure the attempt doesn't exceed the quiz duration
        max_reduction_minutes = min(
            quiz.time_duration - 1, 5
        )  # Don't reduce by more than 5 minutes or duration-1
        reduction_minutes = random.uniform(0, max_reduction_minutes)
        actual_duration_minutes = quiz.time_duration - reduction_minutes
        end_time = start_time + timedelta(minutes=actual_duration_minutes)

        # Generate random responses for questions with user-specific accuracy
        user_responses = generate_random_responses(question_options, answer_accuracy)

        # Calculate score
        score = calculate_attempt_score(question_options, user_responses)

        # Create the quiz attempt
        attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz.id,
            start_time=start_time,
            end_time=end_time,
            in_progress=False,  # Completed attempt
            score=score,
            remarks="dummy data auto generated",
        )

        db.session.add(attempt)
        db.session.flush()  # Get the attempt ID without committing

        # Create user responses
        for question_id, option_id in user_responses.items():
            response = UserResponse(
                attempt_id=attempt.id,
                question_id=question_id,
                option_id=option_id,
                is_attempted=True,
            )
            db.session.add(response)

        db.session.commit()
        print(f"  Created attempt for user {user_id}, quiz {quiz.id}, score: {score}")
        return attempt

    except Exception as e:
        db.session.rollback()
        print(f"  Error creating attempt for user {user_id}, quiz {quiz.id}: {e}")
        return None


def create_all_demo_attempts(demo_users_dict):
    """Create demo attempts for specified users and eligible quizzes"""
    print("Starting to create demo attempts...")

    # Get all eligible quizzes
    eligible_quizzes = get_eligible_quizzes()

    if not eligible_quizzes:
        print("No eligible quizzes found (all quiz dates are in the future)")
        return

    # Create attempts for each user and quiz combination
    for username, user_data in demo_users_dict.items():
        user = user_data["user"]
        accuracy_options = user_data["accuracy"]
        print(
            f"Creating attempts for user: {username} (accuracy range: {min(accuracy_options)*100:.0f}%-{max(accuracy_options)*100:.0f}%)"
        )

        for quiz in eligible_quizzes:
            print(f"  Processing quiz: {quiz.title}")
            # select randomly with user_data["attendance"] probability for [true, false]
            skip = random.choices(
                [False, True],
                weights=[user_data["attendance"], 1 - user_data["attendance"]],
                k=1,
            )[0]
            if skip:
                print(f"  Skipping quiz: {quiz.title}")
                continue

            # Get questions and options for this quiz
            question_options = get_quiz_questions_and_options(quiz.id)

            if not question_options:
                print(f"  No questions found for quiz {quiz.id}")
                continue

            # Randomly select accuracy for this specific quiz attempt
            quiz_accuracy = random.choice(accuracy_options)
            print(f"    Selected accuracy for this quiz: {quiz_accuracy*100:.0f}%")

            # Create attempt for this user and quiz with randomly selected accuracy
            create_demo_attempt(user.id, quiz, question_options, quiz_accuracy)

    print("Demo attempts creation completed!")


if __name__ == "__main__":
    # Demo users configuration with username, random_seed, and accuracy variations
    demo_users_config = {
        "anjali": {
            "random_seed": 11,
            "accuracy": [0.95, 0.9, 0.6],
            "user": None,
            "attendance": 0.75,
        },
        "bibin": {
            "random_seed": 12,
            "accuracy": [0.85, 0.8, 0.75],
            "user": None,
            "attendance": 0.7,
        },
        "chitra": {
            "random_seed": 13,
            "accuracy": [0.8, 0.75, 0.7],
            "user": None,
            "attendance": 1,
        },
        "dinesh": {
            "random_seed": 14,
            "accuracy": [0.75, 0.7, 0.65],
            "user": None,
            "attendance": 1,
        },
        "elizabeth": {
            "random_seed": 15,
            "accuracy": [0.7, 0.65, 0.5],
            "user": None,
            "attendance": 0.9,
        },
        "fahad": {
            "random_seed": 16,
            "accuracy": [0.65, 0.6, 0.5],
            "user": None,
            "attendance": 1,
        },
        "govind": {
            "random_seed": 17,
            "accuracy": [0.9, 0.7, 0.8],
            "user": None,
            "attendance": 1,
        },
        "harish": {
            "random_seed": 18,
            "accuracy": [0.6, 0.5, 0.4],
            "user": None,
            "attendance": 1,
        },
    }

    app = create_app()  # if using factory
    with app.app_context():
        seed_data()

        # Create demo users and store in the config dict
        print("Creating demo users...")
        for username, config in demo_users_config.items():
            user = create_demo_user(username, config["random_seed"])
            config["user"] = user
            accuracy_range = config["accuracy"]
            print(
                f"Created user: {username} with accuracy range: {min(accuracy_range)*100:.0f}%-{max(accuracy_range)*100:.0f}%"
            )

        # Create demo attempts with user-specific accuracies
        create_all_demo_attempts(demo_users_config)
