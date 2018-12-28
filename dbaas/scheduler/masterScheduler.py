from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import sys
from dbaas.metrics.collectMetrics import MetricsFastTick, MetricsSlowTick
from dbaas.trackers.issue_tracker_cleanup import IssueTrackerCleanup


def StartMasterScheduler():
    if "manage.py" not in sys.argv[0]:
        print('This is the Start of all Good and Wonderful things...')
        scheduler = BackgroundScheduler()
        scheduler.add_job(MetricsFastTick, 'interval', seconds=30, max_instances=10, next_run_time=timezone.now())
        scheduler.add_job(MetricsSlowTick, 'interval', minutes=5, max_instances=5, next_run_time=timezone.now())
        scheduler.add_job(IssueTrackerCleanup, 'interval', minutes=10, max_instances=2, next_run_time=timezone.now())
        scheduler.start()
    else:
        print('Schedulers NOT started')
