"""Wait for the database to be reachable using SQLAlchemy engine.

This script retries connecting to `DATABASE_URL` and exits non-zero after a timeout.
"""
import logging
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    logger.error("DATABASE_URL not set")
    raise SystemExit(1)

RETRIES = int(os.environ.get("DB_WAIT_RETRIES", "30"))
SLEEP = float(os.environ.get("DB_WAIT_SLEEP", "1"))

for i in range(RETRIES):
    try:
        engine = create_engine(DB_URL)
        conn = engine.connect()
        conn.close()
        logger.info("Database is reachable")
        raise SystemExit(0)
    except OperationalError as e:
        logger.warning(f"Waiting for DB ({i+1}/{RETRIES})... {e}")
        time.sleep(SLEEP)

logger.error("Timed out waiting for the database")
raise SystemExit(2)
