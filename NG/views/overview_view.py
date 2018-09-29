from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from ng.models import Cluster, Server

def overview(request):

    clusters = Cluster.objects.filter(active_sw=True)
    servers = Server.objects.filter(active_sw=True)

    return render(request, 'overview.html', {'clusters': clusters, 'servers': servers})

