import sys

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from metrics.services.collectMetrics.callCollectors import Metrics_FastTick, Metrics_SlowTick
from monitor.services.incident_cleanup import IncidentCleanup


def StartMasterScheduler():
  if ('makemigrations' in sys.argv or 'migrate' in sys.argv or 'test' in sys.argv):
    print('Schedulers NOT started')
    return []
  else:
    print('This is the Start of all Good and Wonderful things...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(Metrics_FastTick, 'interval', seconds=30, max_instances=10, next_run_time=timezone.now())
    scheduler.add_job(Metrics_SlowTick, 'interval', minutes=10, max_instances=5, next_run_time=timezone.now())
    scheduler.add_job(IncidentCleanup, 'interval', minutes=10, max_instances=2, next_run_time=timezone.now())
    scheduler.start()
