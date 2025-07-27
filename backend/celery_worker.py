#!/usr/bin/env python
"""
Celery Worker Startup Script

python celery_worker.py
or
celery -A celery_worker.celery_app worker --loglevel=info
"""
from app import create_app
from app.celery_app import celery_app, init_celery
import os
import sys

# Add the backend/app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

flask_app = create_app()
init_celery(flask_app)
