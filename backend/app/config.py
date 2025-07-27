import os
from celery.schedules import crontab


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "4ce4ba18b8dedb84629da4be421c1d2d"
    JWT_SECRET_KEY = "edb84629da4be421c1d2d4ce4ba18b8d"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = "static"
    FILE_UPLOAD_FOLDER = "static/uploads/files"
    IMAGE_UPLOAD_FOLDER = "static/uploads/images"
    EXPORT_FOLDER = "static/exports"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS = ["pdf"]
    ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    REDIS_URL = "redis://localhost:6379/0"
    # Celery Configuration
    CELERY_BROKER_URL = (
        os.environ.get("CELERY_BROKER_URL") or "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or "redis://localhost:6379/0"
    )
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"
    CELERY_ENABLE_UTC = True

    # Celery Beat Schedule for periodic tasks
    CELERY_BEAT_SCHEDULE = {
        "daily-reminders": {
            "task": "app.tasks.periodic.send_daily_reminders",
            "schedule": 60.0 * 60.0 * 24.0,  # 24 hours
            # "schedule": 60.0,  # 1 minute for testing
        },
        "monthly-reports": {
            "task": "app.tasks.periodic.generate_monthly_reports",
            "schedule": crontab(
                hour=0, minute=0, day_of_month=1
            ),  # 12:00 AM UTC on the first day of the month
            # "schedule": 60.0,  # 1 minute for testing
        },
    }


# creatw the file_upload_folder and image_upload_folder if not exist inside the static folder
base_path = os.path.abspath(os.path.dirname(__file__))
file_upload_folder = os.path.join(base_path, Config.FILE_UPLOAD_FOLDER)
image_upload_folder = os.path.join(base_path, Config.IMAGE_UPLOAD_FOLDER)
export_folder = os.path.join(base_path, Config.EXPORT_FOLDER)

for folder in [file_upload_folder, image_upload_folder, export_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created {folder}")
