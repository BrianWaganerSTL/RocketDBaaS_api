from django.shortcuts import render

from ng2.models2 import PoolServer
from ng2.serializers.PoolServersSerializers import PoolServersSerializer


def pool_servers(request):
    pool_servers_serializer = PoolServersSerializer
    poolServers = PoolServer.objects.exclude(status_in_pool=PoolServer.StatusInPoolChoices.Used)

    return render(request,
                  'pool_servers.html',
                  {'poolServers': poolServers })

