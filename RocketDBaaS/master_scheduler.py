from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import sys

from metrics.services.collectMetrics import Metrics_FastTick, Metrics_SlowTick
from monitor.services.issue_tracker_cleanup import IssueTrackerCleanup


def StartMasterScheduler():
    if "django_manage.py" not in sys.argv[0]:
        print('This is the Start of all Good and Wonderful things...')
        scheduler = BackgroundScheduler()
        scheduler.add_job(Metrics_FastTick, 'interval', seconds=30, max_instances=10, next_run_time=timezone.now())
        scheduler.add_job(Metrics_SlowTick, 'interval', minutes=10, max_instances=5, next_run_time=timezone.now())
        scheduler.add_job(IssueTrackerCleanup, 'interval', minutes=10, max_instances=2, next_run_time=timezone.now())
        scheduler.start()
    else:
        print('Schedulers NOT started')
