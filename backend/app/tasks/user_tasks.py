from datetime import datetime, timezone
import pandas as pd
import uuid
from flask_sse import sse
from app.services.user.quiz_service import get_user_quiz_history
from app.celery_app import celery_app
from flask import current_app
import os


@celery_app.task(bind=True, name="app.tasks.user_tasks.export_user_data_csv")
def export_user_data_csv(self, user_id, export_type="complete"):
    try:

        print(f"Getting user data for {user_id}")
        # get the BASE_DIR from the config
        base_dir = current_app.config["BASE_DIR"]
        export_folder = current_app.config["EXPORT_FOLDER"]
        export_path = os.path.join(base_dir, export_folder)
        data = get_user_quiz_history(user_id)

        print("Starting CSV export")
        df = pd.DataFrame(data)
        filename = f"user_{user_id}_history_{uuid.uuid4()}.csv"
        file_path = os.path.join(export_path, filename)
        df.to_csv(file_path, index=False)
        # Generate download URL (relative to static folder)
        download_url = f"/download/{filename}"
        print(f"CSV export completed for user {user_id}: {download_url}")

        msg = {
            "status": "success",
            "filename": filename,
            "download_url": download_url,
            "export_type": export_type,
            "user_id": user_id,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        # Send this message via SSE to the client
        sse.publish(msg, type="message")
        print("Message sent to client")
        return msg

    except Exception as exc:
        print(f"CSV export failed for user {user_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)
