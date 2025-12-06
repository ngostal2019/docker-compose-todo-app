"""Small helper to create DB tables.

Run from workspace root:
  python todo_app/create_db.py
or
  python -c "from todo_app.app import db; db.create_all()"
"""
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure /app is in path for Docker container runs
sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from todo_app.app import app, db

    with app.app_context():
        db.create_all()
        logger.info('Database tables created (if connection ok).')
