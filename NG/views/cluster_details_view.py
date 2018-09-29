from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from ng.models import Cluster, Server

def cluster_details(request, cluster_name):
    my_cluster_name = cluster_name

    cluster = Cluster.objects.filter(cluster_name__exact=my_cluster_name)
    # cluster = Cluster.objects.filter(cluster_name=my_cluster_name).values('id','cluster_name', 'application__application_name')
    servers = Server.objects.filter(cluster__cluster_name__exact=my_cluster_name)

    return render(request, 'cluster_details.html', {'cluster': cluster, 'servers': servers})

