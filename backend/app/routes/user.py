from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from flask import Blueprint, request
from app.models import User
from app.services.catalog import (
    get_all_subjects,
    get_chapters_by_subject,
    get_all_quizzes,
    get_questions_by_quiz,
    get_question_by_id,
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
            questions = get_questions_by_quiz(quiz_id)
            if not questions:
                return {"msg": "Quiz not found"}, 404

            return {
                "questions": [
                    {
                        "id": q.id,
                        "question": q.question,
                        "max_marks": q.max_marks,
                        "options": [
                            {
                                "id": opt.id,
                                "option_text": opt.option_text,
                                "is_correct": opt.is_correct,
                            }
                            for opt in q.options
                        ],
                    }
                    for q in questions
                ]
            }, 200
        except Exception as e:
            return {"msg": "Failed to fetch questions"}, 500


class UserQuizAttempt(Resource):
    @jwt_required()
    def get(self, question_id):
        try:
            question = get_question_by_id(question_id)
            if not question:
                return {"msg": "Question not found"}, 404

            return {
                "question": question.question,
                "options": [opt.option_text for opt in question.options],
            }, 200
        except Exception as e:
            return {"msg": "Failed to fetch question"}, 500

    @jwt_required()
    def post(self, question_id):
        try:
            # Get the submitted answer from request
            data = request.get_json()
            if not data or "selected_option_id" not in data:
                return {"msg": "Missing selected option"}, 400

            question = get_question_by_id(question_id)
            if not question:
                return {"msg": "Question not found"}, 404

            # Here you should implement the logic to save the attempt
            # and return appropriate response
            return {"msg": "Answer submitted successfully"}, 200
        except Exception as e:
            return {"msg": "Failed to submit answer"}, 500


user_api.add_resource(ProfileInfo, "/profileinfo")
user_api.add_resource(UserSubjects, "/subjects")
user_api.add_resource(UserQuizzes, "/quizzes")
user_api.add_resource(UserQuestions, "/quiz/<int:quiz_id>/questions")
user_api.add_resource(UserQuizAttempt, "/question/<int:question_id>")
