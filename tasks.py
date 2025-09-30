# Celery tasks and helpers
from celery_worker import celery
from models import db, ScanJob
import time
import socket

def is_allowed_target(host: str) -> bool:
    host_only = host.split(':')[0].lower()
    return host_only in ('localhost', '127.0.0.1', '::1')

