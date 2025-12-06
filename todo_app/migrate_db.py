"""Run database migrations using Flask-Migrate.

This script handles schema upgrades automatically without manual SQL.
Run from the app root:
  python todo_app/migrate_db.py

Or use Flask-Migrate CLI directly:
  flask --app todo_app.app db upgrade
"""
import sys
import os

sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from todo_app.app import app, db
    from flask_migrate import upgrade

    with app.app_context():
        print('Running database migrations...')
        upgrade()
        print('Migrations complete!')
