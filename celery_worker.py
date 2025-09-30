from celery import Celery
from config import Config


celery = Celery(__name__, broker=Config.REDIS_URL, backend=Config.REDIS_URL)


# optionally configure celery can be done fRom here
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']