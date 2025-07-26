from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from flask import Blueprint, request
from app.models import User
from app.services.catalog import (
    get_all_subjects,
    get_chapters_by_subject,
    get_all_quizzes,
    get_questions_by_quiz,
    get_quiz_by_id,
)
from app.services.user.quiz_service import (
    create_quiz_attempt,
    save_user_response,
    close_quiz_attempt,
    get_user_responses,
    get_quiz_score,
    get_full_quiz_result,
    get_user_quiz_history,
)


user_bp = Blueprint("user_api", __name__)

user_api = Api(user_bp)


class ProfileInfo(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"msg": "User not found"}, 404
        return {
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "date_of_birth": str(user.date_of_birth),
            "role": "admin" if user.is_admin else "user",
        }, 200


class UserSubjects(Resource):
    @jwt_required()
    def get(self):
        subjects = get_all_subjects()
        return {
            "subjects": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "chapters": [
                        {"id": c.id, "name": c.name, "description": c.description}
                        for c in get_chapters_by_subject(s.id)
                    ],
                }
                for s in subjects
            ]
        }, 200


class UserQuizzes(Resource):
    @jwt_required()
    def get(self):
        try:
            quizzes = get_all_quizzes()
            return [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "quiz_date": quiz.quiz_date.isoformat(),
                    "time_duration": quiz.time_duration,
                    "remarks": quiz.remarks,
                    "chapter_id": quiz.chapter_id,
                }
                for quiz in quizzes
            ], 200
        except Exception as e:
            return {"msg": "Failed to fetch quizzes"}, 500


class UserQuestions(Resource):
    @jwt_required()
    def get(self, quiz_id):
        try:
            quiz = get_quiz_by_id(quiz_id)
            if not quiz:
                return {"msg": "Quiz not found"}, 404
            questions = get_questions_by_quiz(quiz_id)

            return {
                "quiz_id": quiz_id,
                "quiz_details": {
                    "quiz_id": quiz_id,
                    "quiz_title": quiz.title,
                    "quiz_date": quiz.quiz_date.isoformat(),
                    "time_duration": quiz.time_duration,
                    "remarks": quiz.remarks,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": quiz.chapter.name,
                    "subject_name": quiz.chapter.subject.name,
                },
                "questions": [
                    {
                        "id": q.id,
                        "question": q.question,
                        "max_marks": q.max_marks,
                        "options": [
                            {
                                "id": opt.id,
                                "option_text": opt.option_text,
                            }
                            for opt in q.options
                        ],
                    }
                    for q in questions
                ],
            }, 200
        except Exception as e:
            return {"msg": "Failed to fetch questions"}, 500

    @jwt_required()
    def post(self, quiz_id):
        """Starts a new quiz attempt or returns existing attempt"""
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()

            quiz_attempt, is_new = create_quiz_attempt(user.id, quiz_id)

            if is_new:
                return {
                    "msg": "Quiz attempt started successfully",
                    "attempt_id": quiz_attempt.id,
                }, 201
            else:
                return {
                    "msg": "Existing attempt found",
                    "attempt_id": quiz_attempt.id,
                    "warning": "Complete or submit existing attempt before starting new one",
                }, 200

        except Exception as e:
            return {"msg": "Failed to start quiz attempt"}, 500


class QuizAttempt(Resource):
    """Handle quiz responses"""

    # get requests to get the answers in the open attempt
    @jwt_required()
    def get(self, quiz_id):
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()

            responses = get_user_responses(user.id, quiz_id)
            if not responses:
                return {"msg": "No active attempt found"}, 404
            return {
                "responses": [
                    {
                        "question_id": r.question_id,
                        "option_id": r.option_id,
                        "is_attempted": r.is_attempted,
                    }
                    for r in responses
                ]
            }, 200
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to get quiz responses"}, 500

    @jwt_required()
    def post(self, quiz_id):
        """Submit or update answer for a question"""
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()

            data = request.get_json()
            if (
                not data
                or "question_id" not in data
                or "selected_option_id" not in data
            ):
                return {"msg": "Missing question_id or selected_option_id"}, 400

            response = save_user_response(
                user_id=user.id,
                quiz_id=quiz_id,
                question_id=data["question_id"],
                selected_option_id=data["selected_option_id"],
            )
            return {"msg": "Answer recorded successfully"}, 201
        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to record answer"}, 500


class QuizAttemptStartStop(Resource):
    """Handle quiz attempt submission"""

    @jwt_required()
    def post(self, quiz_id):
        """Start a new quiz attempt"""
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()

            data = request.get_json()
            if data and data.get("start_quiz"):
                # Open the quiz attempt if it is not already open
                attempt, status = create_quiz_attempt(user.id, quiz_id)
                if status:
                    return {"msg": "Quiz attempt started successfully"}, 201
                else:
                    return {
                        "msg": "Quiz attempt already exists",
                        "attempt_id": attempt.id,
                    }, 200
            else:
                return {"msg": 'Invalid payload. Use {"start_quiz": true}'}, 400

        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to start quiz attempt"}, 500

    @jwt_required()
    def put(self, quiz_id):
        """Stop the current quiz attempt"""
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()

            data = request.get_json()
            if data and data.get("stop_quiz"):
                attempt = close_quiz_attempt(user.id, quiz_id)
                return {"msg": "Quiz attempt submitted successfully"}, 200
            else:
                return {"msg": 'Invalid payload. Use {"stop_quiz": true}'}, 400

        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            return {"msg": "Failed to submit quiz attempt"}, 500


class QuizResult(Resource):
    @jwt_required()
    def get(self, quiz_id):
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            result = get_full_quiz_result(user.id, quiz_id)
            return result, 200
        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to get quiz result"}, 500


class UserQuizHistory(Resource):
    @jwt_required()
    def get(self):
        try:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            history = get_user_quiz_history(user.id)
            return history, 200
        except Exception as e:
            return {"msg": "Failed to get quiz history"}, 500


user_api.add_resource(ProfileInfo, "/profileinfo")
user_api.add_resource(UserSubjects, "/subjects")
user_api.add_resource(UserQuizzes, "/quizzes")
user_api.add_resource(UserQuestions, "/quiz/<int:quiz_id>/questions")
user_api.add_resource(QuizAttempt, "/quiz/<int:quiz_id>/attempt")
user_api.add_resource(QuizAttemptStartStop, "/quiz/<int:quiz_id>")
user_api.add_resource(QuizResult, "/quiz/<int:quiz_id>/result")
user_api.add_resource(UserQuizHistory, "/quiz/history")
