from dbaas.models import Server
from metrics.services import getMetrics_PingServer, getMetrics_MountPoints, getMetrics_PingDb, getMetrics_CpuLoad, getMetrics_Cpu, getMetrics_HostDetails, getMetrics_CollectionErrors


def Metrics_FastTick():
    print('\nMetrics_FastTick')

    try:
        poolServers = Server.objects.filter(node_role=Server.NodeRoleChoices.PoolServer);
        for ps in poolServers:
            getMetrics_HostDetails.GetMetrics_HostDetails(ps)  #  This should be first incase cpu and stuff are not filled in yet.
            getMetrics_PingServer.GetMetricsPingServer(ps)
    except:
        pass

    try:
        servers = Server.objects.filter(active_sw=True, metrics_sw=True).exclude(node_role=Server.NodeRoleChoices.PoolServer).exclude(
            node_role=Server.NodeRoleChoices.PoolServerLocked);
        for s in servers:
            print('getMetrics_PingServer: ' + s.server_name)
            getMetrics_PingServer.GetMetricsPingServer(s)
            print('getMetrics_PingDb: ' + s.server_name)
            getMetrics_PingDb.GetMetrics_PingDb(s)
            print('getMetrics_Cpu: ' + s.server_name)
            getMetrics_Cpu.GetMetrics_Cpu(s)
            print('getMetrics_CpuLoad: ' + s.server_name)
            getMetrics_CpuLoad.GetMetrics_Load(s)
            print('getMetrics_CollectionErrors: ' + s.server_name)
            getMetrics_CollectionErrors.GetMetricsCollectionErrors(s)
    except:
        pass

def Metrics_SlowTick():
    try:
        servers = Server.objects.filter(active_sw=True, metrics_sw=True).exclude(node_role=Server.NodeRoleChoices.PoolServer).exclude(
            node_role=Server.NodeRoleChoices.PoolServerLocked);
        for s in servers:
            print('\nMetrics_SlowTick: ServerId=' + str(s.id))
            getMetrics_MountPoints.GetMetrics_MountPoints(s)
    except:
        pass
