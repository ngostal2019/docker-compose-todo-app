# Simple Flask + MySQL Todo App

This is a minimal example showing CRUD operations using Flask + SQLAlchemy with a MySQL backend.

Setup (fish shell):

1. Create virtualenv and activate (fish):

```fish
python3 -m venv venv
source venv/bin/activate.fish
pip install -r todo_app/requirements.txt
```

Install MySQL
----------------

Below are several common ways to install and run MySQL. Pick the one that fits your environment.

- Ubuntu / Debian (apt):

```fish
sudo apt update
sudo apt install -y mysql-server mysql-client
sudo systemctl enable --now mysql
sudo mysql_secure_installation
```

- RHEL / CentOS / Fedora (dnf / yum):

```fish
sudo dnf install -y @mysql    # or install mysql-server from the MySQL community repo
sudo systemctl enable --now mysqld
sudo mysql_secure_installation
```

- Docker (recommended for isolated dev):

```fish
docker run --name mysql-todo \
	-e MYSQL_ROOT_PASSWORD=strongrootpass \
	-e MYSQL_DATABASE=todo_db \
	-e MYSQL_USER=todo_user \
	-e MYSQL_PASSWORD=yourpass \
	-p 3306:3306 \
	-v $HOME/mysql-data:/var/lib/mysql \
	-d mysql:8.0
```

If you open access to port `3306`, prefer restricting it to specific hosts or using an SSH tunnel.

2. Create a MySQL database and user (example):

```sql
CREATE DATABASE todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'yourpass';
GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Set environment variables (fish):

```fish
set -x DATABASE_URL "mysql+pymysql://todo_user:yourpass@localhost/todo_db"
set -x SECRET_KEY "replace-with-secret"
set -x FLASK_APP todo_app/app.py
```

4. Create tables:

```fish
python todo_app/create_db.py
```

5. Run the app (local):

```fish
python -m todo_app.app
```

Or run both services with Docker Compose (recommended):

```fish
docker compose up --build
# or in detached mode
# docker compose up -d --build
```

Open http://localhost:5000 to view the app.

Database Migrations
-------------------

This app uses **Flask-Migrate** to manage schema changes. When you modify the Todo model:

1. The changes are automatically detected during app startup
2. A new migration file is created in `migrations/versions/`
3. The migration is applied automatically to the database

**For local development**, run migrations manually (after updating the model):

```fish
# Generate a new migration
flask --app todo_app.app db migrate -m "Your change description"

# Apply all pending migrations
flask --app todo_app.app db upgrade

# View migration history
flask --app todo_app.app db history
```

**With Docker Compose**, migrations run automatically on every container restart.

Migration files are tracked in version control (`migrations/versions/`), so schema changes are:
- Auditable
- Reversible (via `flask db downgrade`)
- Shareable across the team
