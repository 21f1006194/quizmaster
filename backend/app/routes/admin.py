from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from datetime import datetime

# Importing service functions
from app.services.catalog import (
    get_all_subjects,
    get_subject_by_id,
    get_chapters_by_subject,
    get_chapter_by_id,
    get_quizzes_by_chapter,
    get_quiz_by_id,
    get_all_quizzes,
    get_questions_by_quiz,
    get_question_by_id,
)
from app.services.admin import (
    create_subject,
    update_subject,
    delete_subject,
    create_chapter,
    update_chapter,
    delete_chapter,
)
from app.services.admin.quiz_admin_service import (
    create_quiz,
    update_quiz,
    delete_quiz,
)
from app.services.admin.question_admin_service import (
    create_question,
    update_question,
    delete_question,
)
from app.services.admin.user_admin_service import get_all_users

admin_bp = Blueprint("admin_api", __name__)
admin_api = Api(admin_bp)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"msg": "Admin access only"}, 403
        return fn(*args, **kwargs)

    return wrapper


# ------------------ Subject Endpoints ------------------
class SubjectList(Resource):
    @admin_required
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

    @admin_required
    def post(self):
        data = request.get_json()
        subject = create_subject(data)
        return {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
        }, 201


class SubjectDetail(Resource):
    @admin_required
    def get(self, subject_id):
        subject = get_subject_by_id(subject_id)
        if not subject:
            return {"msg": "Subject not found"}, 404
        return {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
        }, 200

    @admin_required
    def put(self, subject_id):
        data = request.get_json()
        subject = update_subject(subject_id, data)
        if not subject:
            return {"msg": "Subject not found"}, 404
        return {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
        }, 200

    @admin_required
    def delete(self, subject_id):
        result = delete_subject(subject_id)
        if not result["success"]:
            return {"msg": result["message"]}, 400
        return {"msg": result["message"]}, 200


# ------------------ Chapter Endpoints ------------------
class ChapterList(Resource):
    @admin_required
    def get(self, subject_id):
        chapters = get_chapters_by_subject(subject_id)
        return {
            "chapters": [
                {"id": c.id, "name": c.name, "description": c.description}
                for c in chapters
            ]
        }, 200

    @admin_required
    def post(self, subject_id):
        data = request.get_json()
        chapter = create_chapter(subject_id, data)
        return {
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description,
            "subject_id": chapter.subject_id,
        }, 201


class ChapterDetail(Resource):
    @admin_required
    def get(self, chapter_id):
        chapter = get_chapter_by_id(chapter_id)
        if not chapter:
            return {"msg": "Chapter not found"}, 404
        return {
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description,
            "subject_id": chapter.subject_id,
        }, 200

    @admin_required
    def put(self, chapter_id):
        data = request.get_json()
        chapter = update_chapter(chapter_id, data)
        if not chapter:
            return {"msg": "Chapter not found"}, 404
        return {
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description,
            "subject_id": chapter.subject_id,
        }, 200

    @admin_required
    def delete(self, chapter_id):
        result = delete_chapter(chapter_id)
        if not result["success"]:
            return {"msg": result["message"]}, 400
        return {"msg": result["message"]}, 200


# ------------------ Quiz Endpoints ------------------
class QuizList(Resource):
    @admin_required
    def get(self, chapter_id):
        quizzes = get_quizzes_by_chapter(chapter_id)
        return {
            "quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "quiz_date": quiz.quiz_date.isoformat(),
                    "time_duration": quiz.time_duration,
                    "remarks": quiz.remarks,
                }
                for quiz in quizzes
            ]
        }, 200

    @admin_required
    def post(self, chapter_id):
        data = request.get_json()

        # Validate required fields
        required_fields = ["title", "quiz_date", "time_duration"]
        for field in required_fields:
            if field not in data:
                return {"msg": f"Missing required field: {field}"}, 400

        try:
            # Parse and validate quiz date
            quiz_date = datetime.fromisoformat(data["quiz_date"].replace("Z", "+00:00"))
            if quiz_date < datetime.now():
                return {"msg": "Quiz date must be in the future"}, 400

            # Create quiz data
            quiz_data = {
                "title": data["title"],
                "quiz_date": quiz_date,
                "time_duration": int(data["time_duration"]),
                "remarks": data.get("remarks"),
            }

            quiz = create_quiz(chapter_id, quiz_data)
            return {
                "id": quiz.id,
                "title": quiz.title,
                "quiz_date": quiz.quiz_date.isoformat(),
                "time_duration": quiz.time_duration,
                "remarks": quiz.remarks,
            }, 201

        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            return {"msg": "Failed to create quiz"}, 500


class QuizDetail(Resource):
    @admin_required
    def put(self, quiz_id):
        data = request.get_json()
        quiz = get_quiz_by_id(quiz_id)

        if not quiz:
            return {"msg": "Quiz not found"}, 404

        try:
            # Validate quiz date if provided
            if "quiz_date" in data:
                quiz_date = datetime.fromisoformat(
                    data["quiz_date"].replace("Z", "+00:00")
                )
                if quiz_date < datetime.now():
                    return {"msg": "Quiz date must be in the future"}, 400
                data["quiz_date"] = quiz_date

            # Convert time_duration to int if provided
            if "time_duration" in data:
                data["time_duration"] = int(data["time_duration"])

            updated_quiz = update_quiz(quiz_id, data)
            return {
                "id": updated_quiz.id,
                "title": updated_quiz.title,
                "chapter_id": updated_quiz.chapter_id,
                "chapter_name": updated_quiz.chapter.name,
                "quiz_date": updated_quiz.quiz_date.isoformat(),
                "time_duration": updated_quiz.time_duration,
                "remarks": updated_quiz.remarks,
            }, 200

        except ValueError as e:
            return {"msg": str(e)}, 400
        except Exception as e:
            return {"msg": "Failed to update quiz"}, 500

    @admin_required
    def delete(self, quiz_id):
        quiz = get_quiz_by_id(quiz_id)
        if not quiz:
            return {"msg": "Quiz not found"}, 404

        try:
            delete_quiz(quiz_id)
            return {"msg": "Quiz deleted successfully"}, 200
        except Exception as e:
            return {"msg": "Failed to delete quiz"}, 500


class AllQuiz(Resource):
    @admin_required
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


# ------------------ Question Endpoints ------------------
class QuestionList(Resource):
    @admin_required
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
                                "is_correct": opt.is_correct,
                            }
                            for opt in q.options
                        ],
                    }
                    for q in questions
                ],
            }, 200
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to fetch questions"}, 500

    @admin_required
    def post(self, quiz_id):
        data = request.get_json()

        # Validate required fields
        required_fields = ["question", "options"]
        for field in required_fields:
            if field not in data:
                return {"msg": f"Missing required field: {field}"}, 400

        try:
            question = create_question(quiz_id, data)
            return {
                "id": question.id,
                "question": question.question,
                "max_marks": question.max_marks,
                "options": [
                    {
                        "id": opt.id,
                        "option_text": opt.option_text,
                        "is_correct": opt.is_correct,
                    }
                    for opt in question.options
                ],
            }, 201
        except Exception as e:
            import traceback

            traceback.print_exc()
            return {"msg": "Failed to create question"}, 500


class QuestionDetail(Resource):
    @admin_required
    def get(self, question_id):
        question = get_question_by_id(question_id)
        if not question:
            return {"msg": "Question not found"}, 404

        return {
            "id": question.id,
            "question": question.question,
            "max_marks": question.max_marks,
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct,
                }
                for opt in question.options
            ],
        }, 200

    @admin_required
    def put(self, question_id):
        data = request.get_json()
        question = update_question(question_id, data)

        if not question:
            return {"msg": "Question not found"}, 404

        return {
            "id": question.id,
            "question": question.question,
            "max_marks": question.max_marks,
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct,
                }
                for opt in question.options
            ],
        }, 200

    @admin_required
    def delete(self, question_id):
        success = delete_question(question_id)
        if not success:
            return {"msg": "Question not found"}, 404
        return {"msg": "Question deleted successfully"}, 200


# ------------------ User Details Endpoints ------------------
class UserDetails(Resource):
    @admin_required
    def get(self):
        users = get_all_users()
        return (
            users,
            200,
        )  # Return the users directly as they already have the right structure


# ------------------ Route Registrations ------------------
admin_api.add_resource(SubjectList, "/subjects")
admin_api.add_resource(SubjectDetail, "/subjects/<int:subject_id>")

admin_api.add_resource(ChapterList, "/subjects/<int:subject_id>/chapters")
admin_api.add_resource(ChapterDetail, "/chapters/<int:chapter_id>")

admin_api.add_resource(QuizList, "/chapters/<int:chapter_id>/quiz")
admin_api.add_resource(QuizDetail, "/quiz/<int:quiz_id>")
admin_api.add_resource(AllQuiz, "/quizzes")

admin_api.add_resource(QuestionList, "/quiz/<int:quiz_id>/questions")
admin_api.add_resource(QuestionDetail, "/questions/<int:question_id>")
admin_api.add_resource(UserDetails, "/all_users")
