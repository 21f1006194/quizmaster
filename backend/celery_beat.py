#!/usr/bin/env python
"""
Celery Beat Scheduler Startup Script
python celery_beat.py
or
celery -A celery_beat.celery_app beat --loglevel=info
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.celery_app import celery_app

if __name__ == "__main__":
    # Configure logging
    import logging

    logging.basicConfig(level=logging.INFO)

    # Start the beat scheduler
    # Note: This is a simple way to start beat, but for production
    # you should use the celery command directly
    print("Starting Celery Beat Scheduler...")
    print(
        "Use 'celery -A celery_beat.celery_app beat --loglevel=info' for more control"
    )

    # You can uncomment this to start beat programmatically:
    # celery_app.start(['celery', 'beat', '--loglevel=info'])
