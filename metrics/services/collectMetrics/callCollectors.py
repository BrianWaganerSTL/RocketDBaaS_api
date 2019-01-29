from dbaas.models import Server
from metrics.services.collectMetrics import pingServer, collectionErrors, pingDb, cpu, hostDetails, mountPoints, \
    cpuLoad


def Metrics_FastTick():
    print('\nMetrics_FastTick')

    try:
        poolServers = Server.objects.filter(node_role=Server.NodeRoleChoices.POOLSERVER);
        for ps in poolServers:
            hostDetails.HostDetails(ps)  #  This should be first incase cpu and stuff are not filled in yet.
            pingServer.PingServer(ps)
    except:
        pass

    try:
        servers = Server.objects.filter(active_sw=True, metrics_sw=True). \
                    exclude(node_role=Server.NodeRoleChoices.POOLSERVER). \
                    exclude(node_role=Server.NodeRoleChoices.POOLSERVERLOCKED)
        for s in servers:
            try:
                print('getMetrics_PingServer: ' + s.server_name)
                pingServer.PingServer(s)
            except:
                pass
            try:
                print('getMetrics_PingDb: ' + s.server_name)
                pingDb.PingDb(s)
            except:
                pass
            try:
                print('getMetrics_Cpu: ' + s.server_name)
                cpu.Cpu(s)
            except:
                pass
            try:
                print('getMetrics_CpuLoad: ' + s.server_name)
                cpuLoad.CpuLoad(s)
            except:
                pass
            try:
                print('getMetrics_CollectionErrors: ' + s.server_name)
                collectionErrors.CollectionErrors(s)
            except:
                pass
    except:
        pass

def Metrics_SlowTick():
    try:
        servers = Server.objects.filter(active_sw=True, metrics_sw=True). \
                    exclude(node_role=Server.NodeRoleChoices.POOLSERVER). \
                    exclude(node_role=Server.NodeRoleChoices.POOLSERVERLOCKED)
        for s in servers:
            print('\nMetrics_SlowTick: ServerId=' + str(s.id))
            mountPoints.MountPoints(s)
    except:
        pass
