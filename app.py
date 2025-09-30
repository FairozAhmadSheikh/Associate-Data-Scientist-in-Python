from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, ScanJob
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import uuid
from tasks import run_demo_port_scan

app = Flask(__name__)
app.config.from_object(Config)


# extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('username and password required', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('username taken', 'danger')
            return redirect(url_for('register'))
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash('registered! please login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('logged in', 'success')
            return redirect(url_for('index'))
        flash('invalid credentials', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out', 'info')
    return redirect(url_for('index'))

@app.route('/start-demo-scan', methods=['POST'])
@login_required
def start_demo_scan():
    # Demo: start a safe, localhost-only port-scan task via Celery
    target = request.form.get('target', 'localhost')
    # enforce allowed target
    if target.split(':')[0] not in ('localhost', '127.0.0.1', '::1'):
        flash('Only localhost targets allowed in this demo', 'danger')
        return redirect(url_for('index'))