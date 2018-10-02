from django.shortcuts import render

from dbaas.models import PoolServer
from dbaas.serializers.PoolServersSerializers import PoolServersSerializer


def pool_servers(request):
    pool_servers_serializer = PoolServersSerializer
    poolServers = PoolServer.objects.exclude(status_in_pool=PoolServer.StatusInPoolChoices.Used)

    return render(request,
                  'pool_servers.html',
                  {'poolServers': poolServers })

