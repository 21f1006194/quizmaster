from app.models.subject import Subject
from app import db


def create_subject(data):
    subject = Subject(name=data.get("name"), description=data.get("description"))
    db.session.add(subject)
    db.session.commit()
    return subject


def update_subject(subject_id, data):
    subject = Subject.query.get(subject_id)
    if not subject:
        return None
    subject.name = data.get("name", subject.name)
    subject.description = data.get("description", subject.description)
    db.session.commit()
    return subject


def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return {"success": False, "message": "Subject not found"}

    # Check if subject has any chapters
    if subject.chapters:
        return {
            "success": False,
            "message": "Cannot delete subject that has chapters. Delete all chapters first.",
        }

    try:
        db.session.delete(subject)
        db.session.commit()
        return {"success": True, "message": "Subject deleted successfully"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
