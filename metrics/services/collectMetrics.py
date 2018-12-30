from dbaas.models import Server, PoolServer
from metrics.services import getMetrics_PingServer, getMetrics_MountPoints, getMetrics_PingDb, getMetrics_CpuLoad, getMetrics_Cpu


def Metrics_FastTick():
    print('\nMetrics_FastTick')

    servers = Server.objects.filter(active_sw=True, metrics_sw=True);
    for s in servers:
        getMetrics_PingServer.GetMetricsPingServer(s)
        getMetrics_PingDb.GetMetrics_PingDb(s)
        getMetrics_Cpu.GetMetrics_Cpu(s)
        getMetrics_CpuLoad.GetMetrics_Load(s)

    servers = PoolServer.objects.exclude(status_in_pool__iexact=PoolServer.StatusInPoolChoices.Used);
    for s in servers:
        getMetrics_PingServer.GetMetricsPingServer(s)
        getMetrics_PingDb.GetMetrics_hostdetails(s)

def Metrics_SlowTick():
    servers = Server.objects.filter(active_sw=True, metrics_sw=True);
    for s in servers:
        print('\nMetrics_SlowTick: ServerId=' + str(s.id))
        getMetrics_MountPoints.GetMetrics_MountPoints(s)
