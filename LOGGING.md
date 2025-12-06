# Logging Integration Summary

The Flask + MySQL Todo app now uses Python's `logging` module instead of `print()` statements. This provides better visibility, filtering, and production-readiness.

## Changes Made

### 1. **wait_for_db.py**
- Added `logging` module with INFO level
- Replaced `print()` with `logger.info()`, `logger.error()`, and `logger.warning()`
- Database connection attempts are now logged with timestamps

### 2. **create_db.py**
- Added `logging` module
- Logs when tables are created with timestamp

### 3. **init_migrations.py**
- Added `logging` module
- Logs initialization of migrations folder
- Logs migration generation and execution steps
- Logs any migration errors encountered

### 4. **app.py**
- Added `logging` module at module level
- Creates logger instance for the Flask app
- **Logs CRUD operations:**
  - ✅ `logger.info()` when a todo is created
  - ✅ `logger.info()` when a todo is updated (with done status)
  - ✅ `logger.info()` when a todo is deleted
  - ✅ `logger.info()` when a todo is toggled
  - ⚠️ `logger.warning()` when operations fail (missing title, etc.)

## Log Format

All logs follow the format:
```
TIMESTAMP - LOGGER_NAME - LOG_LEVEL - MESSAGE
```

Example output:
```
2025-12-05 05:26:10,649 - INFO - Database is reachable
2025-12-05 05:26:11,646 - INFO - Initializing migrations folder...
2025-12-05 05:26:11,652 - INFO - Generating migration for model changes...
2025-12-05 05:26:12,752 - INFO - Created todo: 1 - My first task
2025-12-05 05:26:13,450 - INFO - Updated todo: 1 - My first task (done=True)
2025-12-05 05:26:14,200 - INFO - Deleted todo: 1 - My first task
```

## Benefits

- 📊 **Better observability** — All app actions are logged with timestamps
- 🔍 **Easier debugging** — Track what happened and when
- ⚠️ **Error tracking** — Failed operations are clearly marked
- 🚀 **Production-ready** — Logs can be sent to centralized logging systems
- 🎛️ **Configurable** — Log levels can be adjusted (INFO, WARNING, ERROR, DEBUG)

## Viewing Logs

To see logs in Docker:
```fish
docker compose logs web
docker compose logs web -f  # Follow mode
docker compose logs web --tail=50  # Last 50 lines
```

To filter by log level:
```fish
docker compose logs web | grep "ERROR"
docker compose logs web | grep "INFO"
```
