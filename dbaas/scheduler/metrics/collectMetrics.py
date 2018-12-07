from dbaas.models import Server
from dbaas.scheduler.metrics import getMetricsCpu, getMetricsLoad, getMetricsMountPoints, getMetricsPingDb, getMetricsPingServer

def MetricsFastTick():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('MetricsFastTick')
        getMetricsPingServer.GetMetricsPingServer(s)
        getMetricsPingDb.GetMetricsPingDb(s)
        getMetricsCpu.GetMetricsCpu(s)
        getMetricsLoad.GetMetricsLoad(s)


def MetricsSlowTick():
    print('MetricsSlowTick')
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('in MetricsSlowTick: s.id=' + str(s.id))
        getMetricsMountPoints.GetMetricsMountPoints(s)
