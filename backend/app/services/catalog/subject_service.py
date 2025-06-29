from app.models.subject import Subject


def get_all_subjects():
    subjects = Subject.query.all()
    return subjects


def get_subject_by_id(subject_id):
    subject = Subject.query.get(subject_id)
    return subject
