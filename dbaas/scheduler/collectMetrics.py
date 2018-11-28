from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import get_object_or_404
from django.utils import timezone

from dbaas.models import Server
from dbaas.scheduler import getMetricsServerPing, getMetricsCpu


def Tick():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('start metrics again')
        getMetricsServerPing.GetServerMetricsPing(s)
        getMetricsCpu.GetMetricsCpu(s)


class StartSchedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Tick, 'interval', seconds=60, max_instances=10, next_run_time=timezone.now())
    scheduler.start()
