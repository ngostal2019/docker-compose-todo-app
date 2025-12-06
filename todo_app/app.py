import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 30  # 30 days
# Expect a DATABASE_URL like: mysql+pymysql://user:pass@host/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'mysql+pymysql://root:password@localhost/todo_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Get list of all available timezones
TIMEZONES = pytz.all_timezones


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    timezone = db.Column(db.String(50), default='UTC', nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username!r}>'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.title!r}>'

    def created_at_user_tz(self):
        """Convert created_at to user's timezone"""
        if not self.user:
            return self.created_at
        tz = pytz.timezone(self.user.timezone)
        utc_time = pytz.utc.localize(self.created_at)
        return utc_time.astimezone(tz)

    def updated_at_user_tz(self):
        """Convert updated_at to user's timezone"""
        if not self.user:
            return self.updated_at
        tz = pytz.timezone(self.user.timezone)
        utc_time = pytz.utc.localize(self.updated_at)
        return utc_time.astimezone(tz)


def get_current_user():
    """Get current user from session, create default if needed"""
    session.permanent = True  # Make session permanent
    if 'user_id' not in session:
        # Create or get default user
        user = User.query.filter_by(username='default_user').first()
        if not user:
            user = User(username='default_user', timezone='UTC')
            db.session.add(user)
            db.session.commit()
            logger.info(f'Created default user with UTC timezone')
        session['user_id'] = user.id
    return User.query.get(session['user_id'])


@app.route('/')
def index():
    user = get_current_user()
    todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.id.desc()).all()
    return render_template('index.html', todos=todos, user=user, timezones=TIMEZONES)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user = get_current_user()
    if request.method == 'POST':
        new_tz = request.form.get('timezone', 'UTC').strip()
        if new_tz not in TIMEZONES:
            logger.warning(f'Invalid timezone: {new_tz}')
            flash('Invalid timezone selected', 'danger')
            return redirect(url_for('settings'))
        user.timezone = new_tz
        db.session.commit()
        logger.info(f'Updated user timezone: {user.username} -> {new_tz}')
        flash(f'Timezone updated to {new_tz}', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html', user=user, timezones=TIMEZONES)


@app.route('/create', methods=['GET', 'POST'])
def create():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip() or None
        if not title:
            logger.warning('Attempted to create todo without title')
            flash('Title is required', 'danger')
            return redirect(url_for('create'))
        todo = Todo(user_id=user.id, title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        logger.info(f'Created todo: {todo.id} - {todo.title} for user {user.username}')
        flash('Todo created', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    user = get_current_user()
    todo = Todo.query.get_or_404(todo_id)
    
    # Verify user owns this todo
    if todo.user_id != user.id:
        logger.warning(f'Unauthorized access attempt to todo {todo_id} by user {user.username}')
        flash('Unauthorized', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip() or None
        done = bool(request.form.get('done'))
        if not title:
            logger.warning(f'Attempted to edit todo {todo_id} without title')
            flash('Title is required', 'danger')
            return redirect(url_for('edit', todo_id=todo_id))
        todo.title = title
        todo.description = description
        todo.done = done
        db.session.commit()
        logger.info(f'Updated todo: {todo_id} - {todo.title} (done={done}) for user {user.username}')
        flash('Todo updated', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo, user=user)


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    user = get_current_user()
    todo = Todo.query.get_or_404(todo_id)
    
    # Verify user owns this todo
    if todo.user_id != user.id:
        logger.warning(f'Unauthorized delete attempt to todo {todo_id} by user {user.username}')
        flash('Unauthorized', 'danger')
        return redirect(url_for('index'))
    
    logger.info(f'Deleted todo: {todo_id} - {todo.title} for user {user.username}')
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted', 'info')
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    user = get_current_user()
    todo = Todo.query.get_or_404(todo_id)
    
    # Verify user owns this todo
    if todo.user_id != user.id:
        logger.warning(f'Unauthorized toggle attempt to todo {todo_id} by user {user.username}')
        flash('Unauthorized', 'danger')
        return redirect(url_for('index'))
    
    todo.done = not todo.done
    db.session.commit()
    logger.info(f'Toggled todo: {todo_id} - done={todo.done} for user {user.username}')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
