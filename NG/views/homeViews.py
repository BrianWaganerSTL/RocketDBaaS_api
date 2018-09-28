from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from ng.models import Cluster, Server

def homeView(request):

    clusters = Cluster.objects.filter(active_sw=True)
    servers = Server.objects.filter(active_sw=True)

    return render(request, 'home.html', {'clusters': clusters, 'servers': servers})

