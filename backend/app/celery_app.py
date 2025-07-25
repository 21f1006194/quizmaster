from celery import Celery


def make_celery(app=None):
    """Create and configure Celery app with Flask context."""
    if app is None:
        # Import here to avoid circular imports
        from app import create_app

        app = create_app()

    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["app.tasks.periodic", "app.tasks.user_tasks"],
    )

    # Update configuration from Flask config
    celery.conf.update(
        task_serializer=app.config["CELERY_TASK_SERIALIZER"],
        accept_content=app.config["CELERY_ACCEPT_CONTENT"],
        result_serializer=app.config["CELERY_RESULT_SERIALIZER"],
        timezone=app.config["CELERY_TIMEZONE"],
        enable_utc=app.config["CELERY_ENABLE_UTC"],
        beat_schedule=app.config["CELERY_BEAT_SCHEDULE"],
    )

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Create celery instance - import here to avoid circular imports
def get_celery_app():
    """Get the celery app instance, creating it if necessary."""
    from app import create_app

    flask_app = create_app()
    return make_celery(flask_app)


# Create the celery app instance
celery_app = get_celery_app()
