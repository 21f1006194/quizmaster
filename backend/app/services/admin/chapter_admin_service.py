from app.models.chapter import Chapter
from app import db


def create_chapter(subject_id, data):

    chapter = Chapter(
        subject_id=subject_id,
        name=data.get("name"),
        description=data.get("description"),
    )
    db.session.add(chapter)
    db.session.commit()
    return chapter


def update_chapter(chapter_id, data):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return None

    chapter.name = data.get("name", chapter.name)
    chapter.description = data.get("description", chapter.description)
    db.session.commit()
    return chapter


def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return {"success": False, "message": "Chapter not found"}

    try:
        # Check if chapter has any associated quizzes
        if chapter.quizzes and len(chapter.quizzes) > 0:
            return {
                "success": False,
                "message": "Cannot delete chapter because it has associated quizzes",
            }

        db.session.delete(chapter)
        db.session.commit()
        return {"success": True, "message": "Chapter deleted successfully"}
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting chapter: {e}")
        return {"success": False, "message": str(e)}
