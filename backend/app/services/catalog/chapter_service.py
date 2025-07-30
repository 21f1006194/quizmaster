from app.models.chapter import Chapter
from app import cache


@cache.memoize(timeout=300)
def get_chapters_by_subject(subject_id):
    print(f"Getting chapters by subject : {subject_id}")
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return chapters


def get_chapter_by_id(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    return chapter
