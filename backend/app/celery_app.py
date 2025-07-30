import os
from celery import Celery

# Get broker URL from environment with localhost default
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Create celery instance with environment-aware configuration
celery_app = Celery(
    "app",
    backend=result_backend,
    broker=broker_url,
    include=["app.tasks.periodic", "app.tasks.user_tasks"],
)

# Configure with defaults - will be updated when Flask app is available
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


def init_celery(app):
    """Initialize Celery with Flask app configuration."""
    celery_app.conf.update(
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        task_serializer=app.config["CELERY_TASK_SERIALIZER"],
        accept_content=app.config["CELERY_ACCEPT_CONTENT"],
        result_serializer=app.config["CELERY_RESULT_SERIALIZER"],
        timezone=app.config["CELERY_TIMEZONE"],
        enable_utc=app.config["CELERY_ENABLE_UTC"],
        beat_schedule=app.config["CELERY_BEAT_SCHEDULE"],
    )

    class ContextTask(celery_app.Task):
        """Make celery tasks work with Flask app context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
