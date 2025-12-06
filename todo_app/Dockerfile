FROM python:3.11-slim

WORKDIR /app

# system deps needed by PyMySQL/SQLAlchemy, timezone support, and general tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY todo_app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the full context (workspace root is now build context)
COPY . /app/

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=todo_app/app.py
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["/bin/sh", "-c", "cd /app && python todo_app/wait_for_db.py && python todo_app/init_migrations.py && python -m todo_app.app"]
