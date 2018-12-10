from dbaas.models import Server
from dbaas.metrics import getMetrics_MountPoints, getMetrics_PingServer, getMetrics_PingDb, getMetrics_Cpu, getMetrics_Load


def MetricsFastTick():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('\nMetricsFastTick')
        getMetrics_PingServer.GetMetricsPingServer(s)
        getMetrics_PingDb.GetMetricsPingDb(s)
        getMetrics_Cpu.GetMetricsCpu(s)
        getMetrics_Load.GetMetricsLoad(s)


def MetricsSlowTick():
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    for s in servers:
        print('\nMetricsSlowTick: ServerId=' + str(s.id))
        getMetrics_MountPoints.GetMetrics_MountPoints(s)
