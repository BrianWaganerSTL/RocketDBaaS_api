from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from dbaas.models import Server
from dbaas.scheduler import getMetricsPingServer, getMetricsCpu, getMetricsMountPoints, getMetricsPingDb, getMetricsLoad


def TickFast():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('start metrics again')
        getMetricsPingServer.GetMetricsPingServer(s)
        getMetricsPingDb.GetMetricsPingDb(s)
        getMetricsCpu.GetMetricsCpu(s)
        getMetricsLoad.GetMetricsLoad(s)


def TickSlow():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        getMetricsMountPoints.GetMetricsMountPoints(s)


# ======================================================================================================
class StartScheduleFast():
    scheduler = BackgroundScheduler()
    scheduler.add_job(TickFast, 'interval', seconds=45, max_instances=10, next_run_time=timezone.now())
    scheduler.start()


class StartScheduleSlow():
    scheduler = BackgroundScheduler()
    scheduler.add_job(TickSlow, 'interval', minutes=20, max_instances=10, next_run_time=timezone.now())
    scheduler.start()
