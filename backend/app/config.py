import os
from celery.schedules import crontab


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///site.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "4ce4ba18b8dedb84629da4be421c1d2d"
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "edb84629da4be421c1d2d4ce4ba18b8d"
    )
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = "static"
    FILE_UPLOAD_FOLDER = "static/uploads/files"
    IMAGE_UPLOAD_FOLDER = "static/uploads/images"
    EXPORT_FOLDER = "static/exports"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS = ["pdf"]
    ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

    # Mail Configuration - localhost defaults for development
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 1025)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "False").lower() in [
        "true",
        "1",
        "yes",
    ]
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False").lower() in [
        "true",
        "1",
        "yes",
    ]

    # Redis Configuration - localhost defaults for development
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST") or "localhost"
    CACHE_REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT") or 6379)
    CACHE_REDIS_PASSWORD = os.environ.get("CACHE_REDIS_PASSWORD")
    CACHE_REDIS_DB = int(os.environ.get("CACHE_REDIS_DB") or 0)
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT") or 300)

    # Celery Configuration - localhost defaults for development
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


# create the file_upload_folder and image_upload_folder if not exist inside the static folder
# Use the same logic as Flask app initialization to ensure consistency
base_path = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.dirname(base_path)  # Go up one level from app to backend
file_upload_folder = os.path.join(backend_path, Config.FILE_UPLOAD_FOLDER)
image_upload_folder = os.path.join(backend_path, Config.IMAGE_UPLOAD_FOLDER)
export_folder = os.path.join(backend_path, Config.EXPORT_FOLDER)

for folder in [file_upload_folder, image_upload_folder, export_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created {folder}")
