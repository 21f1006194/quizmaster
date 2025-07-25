#!/usr/bin/env python
"""
Celery Worker Startup Script

python celery_worker.py
or
celery -A celery_worker.celery_app worker --loglevel=info
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

    # Start the worker
    celery_app.start()
