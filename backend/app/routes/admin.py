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
            # Update quiz data
            update_data = {}

            if "title" in data:
                update_data["title"] = data["title"]

            if "quiz_date" in data:
                quiz_date = datetime.fromisoformat(
                    data["quiz_date"].replace("Z", "+00:00")
                )
                if quiz_date < datetime.now():
                    return {"msg": "Quiz date must be in the future"}, 400
                update_data["quiz_date"] = quiz_date

            if "time_duration" in data:
                update_data["time_duration"] = int(data["time_duration"])

            if "remarks" in data:
                update_data["remarks"] = data["remarks"]

            updated_quiz = update_quiz(quiz_id, update_data)
            return {
                "id": updated_quiz.id,
                "title": updated_quiz.title,
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


# ------------------ Route Registrations ------------------
admin_api.add_resource(SubjectList, "/subjects")
admin_api.add_resource(SubjectDetail, "/subjects/<int:subject_id>")

admin_api.add_resource(ChapterList, "/subjects/<int:subject_id>/chapters")
admin_api.add_resource(ChapterDetail, "/chapters/<int:chapter_id>")

admin_api.add_resource(QuizList, "/chapters/<int:chapter_id>/quiz")
admin_api.add_resource(QuizDetail, "/quiz/<int:quiz_id>")
