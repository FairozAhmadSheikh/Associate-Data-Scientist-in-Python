from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password: str):
        pw = raw_password.encode('utf-8')
        self.password_hash = bcrypt.hashpw(pw, bcrypt.gensalt()).decode('utf-8')


        def check_password(self, raw_password: str) -> bool:
         return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))




class ScanJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(128), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    params = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='pending')
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


user = db.relationship('User', backref='jobs')