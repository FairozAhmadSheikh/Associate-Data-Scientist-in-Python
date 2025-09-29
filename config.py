import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-please-change')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR/"reconapp.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')