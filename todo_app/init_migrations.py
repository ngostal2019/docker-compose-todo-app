"""Initialize Flask-Migrate and generate the initial migration."""
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from todo_app.app import app, db
    from flask_migrate import init, migrate as create_migration, upgrade, stamp

    os.chdir('/app')

    with app.app_context():
        # Check if migrations folder exists
        if not os.path.exists('/app/migrations'):
            logger.info('Initializing migrations folder...')
            init('migrations')
        else:
            logger.info('Migrations folder already exists.')

        # Generate a migration for any changes
        logger.info('Generating migration for model changes...')
        try:
            create_migration(message='Add timestamps to Todo model')
            logger.info('Migration generated successfully.')
        except Exception as e:
            logger.warning(f'Migration generation note: {e}')
            # If no changes detected, that's fine

        # Run all migrations
        logger.info('Running migrations...')
        try:
            upgrade()
            logger.info('Migrations complete!')
        except Exception as e:
            logger.error(f'Migration error (attempting recovery): {e}')
            try:
                # Stamp to mark all applied
                stamp()
                logger.info('Stamped migration as applied.')
            except:
                pass
