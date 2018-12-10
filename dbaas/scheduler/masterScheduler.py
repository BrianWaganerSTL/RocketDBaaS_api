from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from dbaas.metrics.collectMetrics import MetricsFastTick, MetricsSlowTick


def StartMasterScheduler():
    print('This is the Start of all Good and Wonderful things...')

    scheduler = BackgroundScheduler()
    scheduler.add_job(MetricsFastTick, 'interval', seconds=45, max_instances=10, next_run_time=timezone.now())
    scheduler.add_job(MetricsSlowTick, 'interval', seconds=120, max_instances=5, next_run_time=timezone.now())
    scheduler.start()
