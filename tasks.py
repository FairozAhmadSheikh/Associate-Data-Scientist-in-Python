# Celery tasks and helpers
from celery_worker import celery
from models import db, ScanJob
import time
import socket

def is_allowed_target(host: str) -> bool:
    host_only = host.split(':')[0].lower()
    return host_only in ('localhost', '127.0.0.1', '::1')

@celery.task(bind=True)
def run_demo_port_scan(self, job_id: int, target: str):
    """A very small, safe port-scan demo running only on localhost.
    It scans a handful of well-known ports and writes results back to the DB.
    """
    job = ScanJob.query.get(job_id)
    job.status = 'running'
    db.session.commit()


    if not is_allowed_target(target):
        job.status = 'failed'
        job.result = 'target not allowed'
        db.session.commit()
        return {'error': 'target not allowed'}


    ports = [22, 80, 443, 8000, 8080]
    results = []
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            res = s.connect_ex((target if target else '127.0.0.1', p))
            open_ = res == 0
            results.append({'port': p, 'open': open_})
            s.close()
        except Exception as e:
            results.append({'port': p, 'error': str(e)})
        # small delay to avoid overload in demo
        time.sleep(0.2)


    job.status = 'finished'
    job.result = str(results)
    db.session.commit()
    return results