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